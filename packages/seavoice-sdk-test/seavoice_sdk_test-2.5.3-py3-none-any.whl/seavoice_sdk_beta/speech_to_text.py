# -*- coding: utf-8 -*-

"""
SeaVoice Speech SDK v2

Descriptions:
To connect to SeaVoice STT server to finish speech recognizing and synthesizing work.
"""

import asyncio
import contextlib
import json
import logging
from types import TracebackType
from typing import AsyncIterator, Optional, Type, TypeVar, Union
from uuid import uuid4

from typing_extensions import ParamSpec
from websockets.legacy.client import WebSocketClientProtocol

from seavoice_sdk_beta.commands import (
    AudioDataCommand,
    BaseCommand,
    LanguageCode,
    MultiCommands,
    SpeechRecognitionAuthenticationCommand,
    SpeechRecognitionAuthenticationPayload,
    SpeechRecognitionSetting,
    StopCommand,
    STTAudioEncoding,
    STTAudioFormat,
)
from seavoice_sdk_beta.events import (
    BaseEvent,
    InfoEvent,
    RecognizedEvent,
    RecognizingEvent,
    SpeechStatus,
    raw_data_to_event,
)
from seavoice_sdk_beta.exceptions import AuthenticationFail, ClosedException, UnExpectedClosedException
from seavoice_sdk_beta.logger import default_logger
from seavoice_sdk_beta.utils import get_task_result, get_wrapped_ws

RT = TypeVar("RT")
Param = ParamSpec("Param")

DEFAULT_STT_ENDPOINT_URL = "wss://seavoice.seasalt.ai/api/v1/stt/ws"
RECEIVE_EVENT_TIMEOUT = 1800
FINISH_TIMEOUT = 20
DEFAULT_AUDIO_FORMAT = STTAudioFormat.WAV
DEFAULT_AUDIO_ENCODING = STTAudioEncoding.PCM_S16


class SpeechRecognizer:
    def __init__(
        self,
        token: str,
        language: LanguageCode,
        sample_rate: int,
        sample_width: int,
        contexts: Optional[dict] = None,
        context_score: int = 0,
        audio_format: STTAudioFormat = DEFAULT_AUDIO_FORMAT,
        audio_encoding: STTAudioEncoding = DEFAULT_AUDIO_ENCODING,
        enable_itn: bool = True,
        enable_punctuation: bool = True,
        stt_endpoint_url: str = DEFAULT_STT_ENDPOINT_URL,
        logger: Optional[logging.Logger] = None,
        stt_server_id: Optional[str] = None,
        # unused, deprecated
        send_chunk_interval: float = 0.1,
        retry_max: int = 3,
        connection_id: Optional[str] = None,
        send_queue_size: int = 0,
    ) -> None:
        self.token = token
        self.language = language
        self.sample_rate = sample_rate
        self.sample_width = sample_width
        self.channel = 1
        self.enable_itn = enable_itn
        self.enable_punctuation = enable_punctuation
        self.contexts = contexts
        self.context_score = context_score
        self.audio_format = audio_format
        self.audio_encoding = audio_encoding
        self.stt_server_id = stt_server_id
        self.logger = logger or default_logger

        self.send_chunk_interval = send_chunk_interval
        self.retry_max = retry_max
        self.retry_count = 0
        self.connection_count = 0

        self._last_exec: Exception
        self._error_raised = asyncio.Event()

        self.ws_endpoint_url = stt_endpoint_url
        self.websocket: WebSocketClientProtocol
        self._send_task: asyncio.Task[None]
        self._send_queue = asyncio.Queue(maxsize=send_queue_size)
        self._recv_task: asyncio.Task[None]
        self._recv_queue = asyncio.Queue()
        self._bg_handler: asyncio.Task[None]
        self._bg_command_queue = asyncio.Queue()

        self._segment_id_offset: int = 0
        self._sent_bytes: int = 0
        self._voice_start_offset: float = 0
        self._last_segment_id: int = 0

        self._base_sleep_time = 2
        self._max_sleep_time = 30

        self.connection_id = connection_id if connection_id else uuid4().hex

    def update_recognition_status(self) -> None:
        self._voice_start_offset = self._sent_bytes / (self.sample_rate * self.sample_width * self.channel)
        self._segment_id_offset = self._last_segment_id + 1

    async def __aenter__(self) -> "SpeechRecognizer":
        await self._init_connection()
        self._error_raised = asyncio.Event()
        self.retry_count = 0
        self.connection_count = 0

        self._segment_id_offset = 0
        self._sent_bytes = 0
        self._voice_start_offset = 0
        self._raise_if_error_set()
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
        return f"speech-to-text: {self.connection_id}-{str(uuid4().hex)}-{self.connection_count}"

    async def _init_connection(self):
        base_sleep_time = self._base_sleep_time
        while True:
            try:
                self.connection_count += 1
                self.logger.info(f"{self.connection_name} init start")
                self.websocket = await get_wrapped_ws(f"{self.ws_endpoint_url}?connection_id={self.connection_id}")
                await self._authentication()
                self.logger.info(f"{self.connection_name} init finish")
                return
            except Exception as error:
                if self.retry_count > self.retry_max:
                    self.logger.error(
                        f"{self.connection_name} has too many Exception: {error.__class__.__name__} {error} "
                        f"retry_count: {self.retry_count}"
                    )
                    raise error

                self.retry_count += 1
                self.logger.warning(
                    f"{self.connection_name} will retry after {base_sleep_time} sec, encounter error: "
                    f"{error.__class__.__name__} {error}"
                )
                await asyncio.sleep(base_sleep_time)
                base_sleep_time = min(base_sleep_time * 2, self._max_sleep_time)

    async def _handle_bg_and_ws(self):
        self._send_task = asyncio.create_task(self._send_from_queue())
        self._recv_task = asyncio.create_task(self._recv_to_queue())
        try:
            while True:
                reconnect = asyncio.create_task(self._bg_command_queue.get())
                await asyncio.wait([self._send_task, self._recv_task, reconnect], return_when=asyncio.FIRST_COMPLETED)
                reconnect_done = reconnect.result() if reconnect.done() else None
                try:
                    if reconnect_done:
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

                if isinstance(reconnect_done, asyncio.Event):
                    reconnect_done.set()

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
        except Exception as e:
            self.logger.debug(f"{self.connection_name} _recv_task stops due to exception: {e.__class__.__name__}:{e}")

    async def _force_close_ws(self):
        with contextlib.suppress(Exception):
            await self.websocket.close()

    async def change_language(self, language: LanguageCode) -> None:
        self.logger.debug(f"{self.connection_name} start change_language")
        if self.language == language:
            self.logger.warning(f"{self.connection_name} passed if the language is the same")
            return
        self.language = language
        await self._reconnection()
        self.logger.debug(f"{self.connection_name} create new connection successfully")

    async def _reconnection(self) -> None:
        self._raise_if_error_set()
        reconnect_done = asyncio.Event()
        self._bg_command_queue.put_nowait(reconnect_done)
        await asyncio.wait(
            [asyncio.create_task(self._error_raised.wait()), asyncio.create_task(reconnect_done.wait())],
            return_when=asyncio.FIRST_COMPLETED,
        )
        self._raise_if_error_set()

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
                    SpeechRecognitionAuthenticationCommand(
                        payload=SpeechRecognitionAuthenticationPayload(
                            token=self.token,
                            settings=SpeechRecognitionSetting(
                                language=self.language,
                                sample_rate=self.sample_rate,
                                itn=self.enable_itn,
                                punctuation=self.enable_punctuation,
                                contexts=self.contexts or {},
                                context_score=self.context_score,
                                audio_format=self.audio_format,
                                encoding=self.audio_encoding,
                                stt_server_id=self.stt_server_id,
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
        else:
            self.logger.debug(
                f"{self.connection_name} authentication successfully, connection id: {event.payload.connection_id}"
            )

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

    async def send(self, audio_data: bytes) -> None:
        self._raise_if_error_set()
        is_audio_done = asyncio.Event()
        await self._send_queue.put(
            MultiCommands(
                commands=[AudioDataCommand(payload=audio_data)],
                done=is_audio_done,
            )
        )
        await asyncio.wait(
            [asyncio.create_task(self._error_raised.wait()), asyncio.create_task(is_audio_done.wait())],
            return_when=asyncio.FIRST_COMPLETED,
        )
        self._raise_if_error_set()

    async def finish(self) -> None:
        is_finish_done = asyncio.Event()
        await self._send_queue.put(MultiCommands(commands=[StopCommand()], done=is_finish_done))
        await asyncio.wait_for(is_finish_done.wait(), FINISH_TIMEOUT)

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
        if isinstance(event, RecognizingEvent) or isinstance(event, RecognizedEvent):
            event.payload.segment_id += self._segment_id_offset
            self._last_segment_id = event.payload.segment_id
            event.payload.voice_start_time += self._voice_start_offset
            for word_aliment in event.payload.word_alignments:
                word_aliment.start += self._voice_start_offset
        return event

    def _send_handler(self, data: BaseCommand):
        if isinstance(data, AudioDataCommand):
            self._sent_bytes += len(data.payload)
        return json.dumps(data.to_dict(), ensure_ascii=False)
