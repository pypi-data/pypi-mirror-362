# -*- coding: utf-8 -*-

"""
SeaVoice Speech SDK v2

Descriptions:
To connect to SeaVoice STT server to finish speech recognizing and synthesizing work.
"""

import asyncio
import functools
from typing import Any, Callable, Coroutine, Optional, TypeVar, Union

from typing_extensions import Awaitable, ParamSpec
from websockets.exceptions import ConnectionClosed, ConnectionClosedOK, WebSocketException
from websockets.legacy.client import WebSocketClientProtocol, connect

from seavoice_sdk_beta.exceptions import ClosedException, InternalError, UnExpectedClosedException

RT = TypeVar("RT")
Param = ParamSpec("Param")


def get_task_result(task: asyncio.Task) -> Optional[BaseException]:
    try:
        return task.result() if task.done() else None
    except BaseException as e:
        return e


async def wait_task_result(task: Awaitable[RT]) -> Union[BaseException, RT]:
    try:
        return await task
    except BaseException as e:
        return e


def _ws_wrapper(func: Callable[Param, Coroutine[Any, Any, RT]]) -> Callable[Param, Coroutine[Any, Any, RT]]:
    @functools.wraps(func)
    async def wrapped(*args: Param.args, **kwargs: Param.kwargs) -> RT:
        try:
            return await func(*args, **kwargs)
        except ConnectionClosedOK as e:
            raise ClosedException(exception=e)
        except ConnectionClosed as e:
            raise UnExpectedClosedException(exception=e)
        except WebSocketException as e:
            raise InternalError(exception=e)
        except Exception as e:
            raise e

    return wrapped


_connect = _ws_wrapper(connect)  # type: ignore


async def get_wrapped_ws(url: str) -> WebSocketClientProtocol:
    websocket: WebSocketClientProtocol = await _connect(url)
    websocket.send = _ws_wrapper(websocket.send)
    websocket.recv = _ws_wrapper(websocket.recv)
    websocket.close = _ws_wrapper(websocket.close)

    return websocket
