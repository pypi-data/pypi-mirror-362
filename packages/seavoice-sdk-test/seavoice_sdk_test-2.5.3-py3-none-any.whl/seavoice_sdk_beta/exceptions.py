# -*- coding: utf-8 -*-

"""
Exception class of SeaVoice Speech SDK v2
"""

from typing import Optional


class SeavoiceException(Exception):
    def __init__(self, exception: Optional[Exception] = None, message: Optional[str] = None) -> None:
        self._exception = exception
        self._message = message

    def __str__(self) -> str:
        return f"{type(self)}: {self._message if self._message else self._exception}"


class ClosedException(SeavoiceException):
    pass


class UnExpectedClosedException(SeavoiceException):
    pass


class InternalError(SeavoiceException):
    pass


class InvalidURI(SeavoiceException):
    pass


class AuthenticationFail(SeavoiceException):
    pass


class InvalidEvent(SeavoiceException):
    pass
