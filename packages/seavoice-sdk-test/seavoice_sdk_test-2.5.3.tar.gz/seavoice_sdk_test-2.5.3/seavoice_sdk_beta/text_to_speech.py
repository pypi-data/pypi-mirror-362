import asyncio
import contextlib
import json
import logging
from types import TracebackType
from typing import AsyncIterator, Optional, Type, TypeVar, Union

from typing_extensions import ParamSpec
from websockets.legacy.client import WebSocketClientProtocol

from seavoice_sdk_beta.commands import (
    BaseCommand,
    LanguageCode,
    MultiCommands,
    SpeechSynthesisAuthenticationCommand,
    SpeechSynthesisAuthenticationPayload,
    SpeechSynthesisSetting,
    StopCommand,
    SynthesisCommand,
    Voice,
)
from seavoice_sdk_beta.events import AudioDataEvent, BaseEvent, InfoEvent, SpeechStatus, raw_data_to_event
from seavoice_sdk_beta.exceptions import AuthenticationFail, ClosedException, UnExpectedClosedException
from seavoice_sdk_beta.logger import default_logger
from seavoice_sdk_beta.utils import get_task_result, get_wrapped_ws

RT = TypeVar("RT")
Param = ParamSpec("Param")

DEFAULT_TTS_ENDPOINT_URL = "wss://seavoice.seasalt.ai/api/v1/tts/ws"


class SpeechSynthesizer:
    def __init__(
        self,
        token: str,
        language: LanguageCode,
        sample_rate: int,
        voice: Voice,
        tts_endpoint_url: str = DEFAULT_TTS_ENDPOINT_URL,
        logger: Optional[logging.Logger] = None,
        tts_server_id: Optional[str] = None,
        retry_max: int = 3,
    ) -> None:
        self.token = token
        self.language = language
        self.sample_rate = sample_rate
        self.voice = voice
        self.tts_server_id = tts_server_id

        self.logger = logger or default_logger

        self.retry_max = retry_max
        self.retry_count = 0
        self.connection_count = 0

        self._last_exec: Exception
        self._error_raised = asyncio.Event()

        self.ws_endpoint_url = tts_endpoint_url
        self.websocket: WebSocketClientProtocol
        self._send_task: asyncio.Task[None]
        self._send_queue = asyncio.Queue()
        self._recv_task: asyncio.Task[None]
        self._recv_queue = asyncio.Queue()
        self._bg_handler: asyncio.Task[None]
        self._bg_command_queue = asyncio.Queue()

        self._segment_id_offset: int = 0
        self._last_segment_id: int = 0

        self._base_sleep_time = 2
        self._max_sleep_time = 30

    def update_recognition_status(self) -> None:
        self._segment_id_offset = self._last_segment_id + 1

    async def __aenter__(self) -> "SpeechSynthesizer":
        self._error_raised = asyncio.Event()
        self.retry_count = 0
        self.connection_count = 0
        self._segment_id_offset = 0
        self._last_segment_id = 0

        await self._init_connection()
        self._error_raised = asyncio.Event()
        self.retry_count = 0
        self.connection_count = 0
        if self._error_raised.is_set():
            del self._last_exec
        self._bg_handler = asyncio.create_task(self._handle_bg_and_ws())
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[Exception]],
        exc_value: Optional[Exception],
        traceback: Optional[TracebackType],
    ) -> bool:
        await self.close()
        return (exc_type == ClosedException) or (exc_type is None)

    async def close(self):
        self._bg_handler.cancel()
        await self._force_close_ws()

    @property
    def connection_name(self) -> str:
        return f"text-to-speech: {id(self)}-{self.connection_count}"

    async def _init_connection(self):
        base_sleep_time = self._base_sleep_time
        while True:
            try:
                self.connection_count += 1
                self.logger.info(f"{self.connection_name} start")
                self.websocket = await get_wrapped_ws(self.ws_endpoint_url)
                await self._authentication()
                self.logger.info(f"{self.connection_name} finish")
                return
            except UnExpectedClosedException as error:
                if self.retry_count > self.retry_max:
                    self.logger.error(
                        f"{self.connection_name} has too many UnExpectedClosedException"
                        f"retry_count: {self.retry_count}"
                    )
                    raise error

                self.retry_count += 1
                self.logger.info(f"{self.connection_name} should retry after {base_sleep_time} sec")
                await asyncio.sleep(base_sleep_time)
                base_sleep_time = min(base_sleep_time * 2, self._max_sleep_time)
            except Exception as error:
                self.logger.error(f"{self.connection_name} raise {error}")
                raise error

    async def _handle_bg_and_ws(self):
        self._send_task = asyncio.create_task(self._send_from_queue())
        self._recv_task = asyncio.create_task(self._recv_to_queue())
        try:
            while True:
                reconnect = asyncio.create_task(self._bg_command_queue.get())
                await asyncio.wait([self._send_task, self._recv_task, reconnect], return_when=asyncio.FIRST_COMPLETED)
                future = reconnect.result() if reconnect.done() else None
                try:
                    if future:
                        await self._soft_close_bg_when_working()
                    else:
                        reconnect.cancel()
                        await self._soft_close_bg_when_error()  # may raise error

                    await self._force_close_ws()
                    self.update_recognition_status()
                    await self._init_connection()  # may raise error
                except Exception as error:
                    self._last_exec = error
                    self._error_raised.set()

                if isinstance(future, asyncio.Future):
                    future.set_result(None)

                if self._error_raised.is_set():
                    self.logger.info(f"{self.connection_name} close because _init_connection raise {self._last_exec}")
                    return

                self._send_task = asyncio.create_task(self._send_from_queue())
                self._recv_task = asyncio.create_task(self._recv_to_queue())
        finally:
            # if _handle_bg_and_ws cancel, the below line is triggered
            self._send_task.cancel()
            self._recv_task.cancel()

    async def _soft_close_bg_when_error(self):
        send_exec = get_task_result(self._send_task)
        recv_exec = get_task_result(self._recv_task)

        self.logger.info(f"{self.connection_name} got send_task exception: {send_exec} recv_task exception: {recv_exec}")
        # stop if there is an non unexpected exception
        if not (isinstance(recv_exec, UnExpectedClosedException) or isinstance(send_exec, UnExpectedClosedException)):
            self.logger.info(f"{self.connection_name} close due to {recv_exec} or {send_exec}")
            last_exec = recv_exec or send_exec
            assert last_exec is not None
            raise last_exec

        await self._close_send_task()
        await self._close_recv_task()

    async def _close_send_task(self):
        self.logger.debug(f"{self.connection_name} starts to close send_task")
        if self._send_task.done():
            self.logger.debug(f"{self.connection_name} send_task is already closed")
            return

        send_queue = self._send_queue
        self._send_queue = asyncio.Queue()
        queue_done = asyncio.create_task(send_queue.join())
        await asyncio.wait([queue_done, self._send_task], return_when=asyncio.FIRST_COMPLETED)
        if queue_done.done():
            self.logger.debug(f"{self.connection_name} all data in send queue is sent")
            self._send_task.cancel()
        else:
            self.logger.debug(f"{self.connection_name} some error: {get_task_result(self._send_task)} raised during waiting")
            queue_done.cancel()

    async def _close_recv_task(self):
        self.logger.debug(f"{self.connection_name} starts to close recv_task")
        if self._recv_task.done():
            self.logger.debug(f"{self.connection_name} recv_task is already closed")
            return

        try:
            await asyncio.wait_for(self._recv_task, 10)
        except asyncio.TimeoutError:
            self._recv_task.cancel()
            self.logger.debug(f"{self.connection_name} cancel _recv_task for timeout")
        except Exception:
            self.logger.debug(f"{self.connection_name} _recv_task stops due to exception")

    async def _force_close_ws(self):
        with contextlib.suppress(Exception):
            await self.websocket.close()

    def _raise_if_error_set(self) -> None:
        if self._error_raised.is_set():
            raise self._last_exec

    async def _soft_close_bg_when_working(self):
        await self._close_send_task()
        with contextlib.suppress(Exception):
            await self.websocket.send(self._send_handler(StopCommand()))
        await self._close_recv_task()

    async def _authentication(self):
        try:
            await self.websocket.send(
                self._send_handler(
                    SpeechSynthesisAuthenticationCommand(
                        payload=SpeechSynthesisAuthenticationPayload(
                            token=self.token,
                            settings=SpeechSynthesisSetting(
                                language=self.language, voice=self.voice, tts_server_id=self.tts_server_id
                            ),
                        )
                    )
                )
            )
        except UnExpectedClosedException as e:
            raise e
        except Exception as e:
            raise AuthenticationFail(message=f"send auth command fails, error: {e}")

        try:
            event = self._recv_handler(await self.websocket.recv())
        except UnExpectedClosedException as e:
            raise e
        except Exception as e:
            raise AuthenticationFail(message=f"receive and parse event fails, error: {e}")

        if not isinstance(event, InfoEvent) or event.payload.status != SpeechStatus.BEGIN:
            raise AuthenticationFail(message=f"receive unexpected event: {event}")

        self._recv_queue.put_nowait(event)

    async def recv(self) -> BaseEvent:
        recv = asyncio.create_task(self._recv_queue.get())
        error = asyncio.create_task(self._error_raised.wait())
        await asyncio.wait([recv, error], return_when=asyncio.FIRST_COMPLETED)

        if recv.done():
            error.cancel()
            return recv.result()

        recv.cancel()
        raise self._last_exec

    async def send(self, synthesis_command: SynthesisCommand) -> None:
        self._raise_if_error_set()
        is_synthesis_done = asyncio.Event()
        self._send_queue.put_nowait(MultiCommands(commands=[synthesis_command], done=is_synthesis_done))
        await asyncio.wait(
            [
                asyncio.create_task(self._error_raised.wait()),
                asyncio.create_task(is_synthesis_done.wait())
            ],
            return_when=asyncio.FIRST_COMPLETED
        )
        self._raise_if_error_set()

    async def stream(self) -> AsyncIterator[BaseEvent]:
        while True:
            try:
                yield (await self.recv())
            except ClosedException:
                return
            except Exception as e:
                raise e

    async def _send_from_queue(self) -> None:
        send_queue = self._send_queue
        while True:
            data = await send_queue.get()
            assert isinstance(data, MultiCommands)
            try:
                for command in data.commands:
                    await self.websocket.send(self._send_handler(command))
            finally:
                send_queue.task_done()
                data.done.set()

    async def _recv_to_queue(self) -> None:
        while True:
            self._recv_queue.put_nowait(self._recv_handler(await self.websocket.recv()))

    def _recv_handler(self, data: Union[str, bytes]) -> BaseEvent:
        event = raw_data_to_event(**json.loads(data))
        if isinstance(event, AudioDataEvent):
            event.payload.sid += self._segment_id_offset
            self._last_segment_id = event.payload.sid
        return event

    def _send_handler(self, command: BaseCommand):
        return json.dumps(command.to_dict())
