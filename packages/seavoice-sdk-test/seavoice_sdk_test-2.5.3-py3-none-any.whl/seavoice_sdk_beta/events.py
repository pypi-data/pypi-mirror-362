# -*- coding: utf-8 -*-

"""
The events of seavoice-sdk
"""
import base64
from abc import ABC
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, ClassVar, List

from seavoice_sdk_beta.exceptions import InvalidEvent


class SpeechEvent(str, Enum):
    INFO = "info"
    RECOGNIZING = "recognizing"
    RECOGNIZED = "recognized"
    AUDIO_DATA = "audio_data"


class SpeechStatus(str, Enum):
    BEGIN = "begin"
    END = "end"
    ERROR = "error"


@dataclass
class AbstractDataclass(ABC):
    def __new__(cls, *args, **kwargs):
        if cls == AbstractDataclass or cls.__bases__[0] == AbstractDataclass:
            raise TypeError("Cannot instantiate abstract class.")
        return super().__new__(cls)


@dataclass
class BaseEvent(AbstractDataclass):
    event: ClassVar[SpeechEvent]
    payload: Any


@dataclass
class InfoEventPayload:
    status: SpeechStatus = SpeechStatus.BEGIN
    connection_id: str = ""


@dataclass
class InfoEvent(BaseEvent):
    event: ClassVar[SpeechEvent] = SpeechEvent.INFO
    payload: InfoEventPayload

    def __post_init__(self):
        self.payload = InfoEventPayload(**self.payload)  # type: ignore


@dataclass
class InfoErrorEventPayload(InfoEventPayload):
    status: SpeechStatus = SpeechStatus.ERROR
    error: dict = field(default_factory=dict)


@dataclass
class InfoErrorEvent(BaseEvent):
    event: ClassVar[SpeechEvent] = SpeechEvent.INFO
    payload: InfoErrorEventPayload

    def __post_init__(self):
        self.payload = InfoErrorEventPayload(**self.payload)  # type: ignore


@dataclass
class WordAlignment:
    word: str
    start: float
    length: float = 1


@dataclass
class RecognizingEventPayload:
    segment_id: int
    text: str
    voice_start_time: float
    word_alignments: List[WordAlignment]

    def __post_init__(self):
        self.word_alignments = [WordAlignment(**word_alignment) for word_alignment in self.word_alignments]  # type: ignore


@dataclass
class RecognizingEvent(BaseEvent):
    event: ClassVar[SpeechEvent] = SpeechEvent.RECOGNIZING
    payload: RecognizingEventPayload

    def __post_init__(self):
        self.payload = RecognizingEventPayload(**self.payload)  # type: ignore


@dataclass
class RecognizedEventPayload(RecognizingEventPayload):
    duration: float


@dataclass
class RecognizedEvent(BaseEvent):
    event: ClassVar[SpeechEvent] = SpeechEvent.RECOGNIZED
    payload: RecognizedEventPayload

    def __post_init__(self):
        self.payload = RecognizedEventPayload(**self.payload)  # type: ignore


@dataclass
class AudioDataEventPayload:
    sid: int
    status: str
    audio: bytes = field(repr=False)

    def __post_init__(self):
        self.audio = base64.b64decode(self.audio)  # type: ignore


@dataclass
class AudioDataEvent(BaseEvent):
    event: ClassVar[SpeechEvent] = SpeechEvent.AUDIO_DATA
    payload: AudioDataEventPayload

    def __post_init__(self):
        self.payload = AudioDataEventPayload(**self.payload)  # type: ignore


def raw_data_to_event(event: str, payload: Any) -> BaseEvent:
    try:
        if event == SpeechEvent.INFO:
            return InfoErrorEvent(payload=payload) if "error" in payload else InfoEvent(payload=payload)
        elif event == SpeechEvent.RECOGNIZING:
            return RecognizingEvent(payload=payload)
        elif event == SpeechEvent.RECOGNIZED:
            return RecognizedEvent(payload=payload)
        elif event == SpeechEvent.AUDIO_DATA:
            return AudioDataEvent(payload=payload)
        raise InvalidEvent(message=f"event: {event} is invalid.")
    except BaseException as e:
        raise InvalidEvent(message=f"event: {event} with payload: {payload} is invalid due to {e}.")
