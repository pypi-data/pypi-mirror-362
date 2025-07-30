# -*- coding: utf-8 -*-

"""
The commands of seavoice-sdk
"""
import asyncio
import base64
from abc import ABC
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, ClassVar, List, Optional


class SpeechCommand(str, Enum):
    STOP = "stop"
    AUTHENTICATION = "authentication"
    AUDIO_DATA = "audio_data"
    SYNTHESIS = "synthesis"


class Voice(str, Enum):
    TONGTONG = "Tongtong"
    VIVIAN = "Vivian"
    MIKE = "Mike"
    MOXIE = "Moxie"
    LISSA = "Lissa"
    TOM = "Tom"
    ROBERT = "Robert"
    DAVID = "David"
    ANNE = "Anne"
    REESE = "Reese"


class LanguageCode(str, Enum):
    AUTO = "auto"
    AF_ZA = "af-ZA"  # Afrikaans (South Africa)
    SQ_AL = "sq-AL"  # Albanian (Albania)
    AR_DZ = "ar-DZ"  # Arabic (Algeria)
    AR_BH = "ar-BH"  # Arabic (Bahrain)
    AR_EG = "ar-EG"  # Arabic (Egypt)
    AR_IQ = "ar-IQ"  # Arabic (Iraq)
    AR_JO = "ar-JO"  # Arabic (Jordan)
    AR_KW = "ar-KW"  # Arabic (Kuwait)
    AR_LB = "ar-LB"  # Arabic (Lebanon)
    AR_LY = "ar-LY"  # Arabic (Libya)
    AR_MA = "ar-MA"  # Arabic (Morocco)
    AR_OM = "ar-OM"  # Arabic (Oman)
    AR_QA = "ar-QA"  # Arabic (Qatar)
    AR_SA = "ar-SA"  # Arabic (Saudi Arabia)
    AR_SY = "ar-SY"  # Arabic (Syria)
    AR_TN = "ar-TN"  # Arabic (Tunisia)
    AR_AE = "ar-AE"  # Arabic (U.A.E.)
    AR_YE = "ar-YE"  # Arabic (Yemen)
    EU_ES = "eu-ES"  # Basque (Spain)
    BE_BY = "be-BY"  # Belarusian (Belarus)
    BG_BG = "bg-BG"  # Bulgarian (Bulgaria)
    CA_ES = "ca-ES"  # Catalan (Spain)
    ZH_HK = "zh-HK"  # Chinese (Hong Kong SAR)
    ZH_CN = "zh-CN"  # Chinese (Mandarin, Simplified)
    ZH_SG = "zh-SG"  # Chinese (Singapore)
    ZH_TW = "zh-TW"  # Chinese (Taiwan)
    HR_HR = "hr-HR"  # Croatian (Croatia)
    CS_CZ = "cs-CZ"  # Czech (Czech Republic)
    DA_DK = "da-DK"  # Danish (Denmark)
    NL_BE = "nl-BE"  # Dutch (Belgium)
    NL_NL = "nl-NL"  # Dutch (Netherlands)
    EN_AU = "en-AU"  # English (Australia)
    EN_CA = "en-CA"  # English (Canada)
    EN_GH = "en-GH"  # English (Ghana)
    EN_HK = "en-HK"  # English (Hong Kong SAR)
    EN_IN = "en-IN"  # English (India)
    EN_IE = "en-IE"  # English (Ireland)
    EN_KE = "en-KE"  # English (Kenya)
    EN_NZ = "en-NZ"  # English (New Zealand)
    EN_NG = "en-NG"  # English (Nigeria)
    EN_PH = "en-PH"  # English (Philippines)
    EN_SG = "en-SG"  # English (Singapore)
    EN_ZA = "en-ZA"  # English (South Africa)
    EN_TZ = "en-TZ"  # English (Tanzania)
    EN_GB = "en-GB"  # English (United Kingdom)
    EN_US = "en-US"  # English (United States)
    ET_EE = "et-EE"  # Estonian (Estonia)
    FIL_PH = "fil-PH"  # Filipino (Philippines)
    FI_FI = "fi-FI"  # Finnish (Finland)
    FR_BE = "fr-BE"  # French (Belgium)
    FR_CA = "fr-CA"  # French (Canada)
    FR_FR = "fr-FR"  # French (France)
    FR_CH = "fr-CH"  # French (Switzerland)
    GL_ES = "gl-ES"  # Galician (Spain)
    DE_AT = "de-AT"  # German (Austria)
    DE_DE = "de-DE"  # German (Germany)
    DE_CH = "de-CH"  # German (Switzerland)
    EL_GR = "el-GR"  # Greek (Greece)
    HE_IL = "he-IL"  # Hebrew (Israel)
    HI_IN = "hi-IN"  # Hindi (India)
    HU_HU = "hu-HU"  # Hungarian (Hungary)
    IS_IS = "is-IS"  # Icelandic (Iceland)
    ID_ID = "id-ID"  # Indonesian (Indonesia)
    GA_IE = "ga-IE"  # Irish (Ireland)
    IT_IT = "it-IT"  # Italian (Italy)
    IT_CH = "it-CH"  # Italian (Switzerland)
    JA_JP = "ja-JP"  # Japanese (Japan)
    KO_KR = "ko-KR"  # Korean (Korea)
    LV_LV = "lv-LV"  # Latvian (Latvia)
    LT_LT = "lt-LT"  # Lithuanian (Lithuania)
    MK_MK = "mk-MK"  # Macedonian (North Macedonia)
    MS_MY = "ms-MY"  # Malay (Malaysia)
    MT_MT = "mt-MT"  # Maltese (Malta)
    NO_NO = "no-NO"  # Norwegian (Norway)
    NB_NO = "nb-NO"  # Norwegian Bokmål (Norway)
    PL_PL = "pl-PL"  # Polish (Poland)
    PT_BR = "pt-BR"  # Portuguese (Brazil)
    PT_PT = "pt-PT"  # Portuguese (Portugal)
    RO_RO = "ro-RO"  # Romanian (Romania)
    RU_RU = "ru-RU"  # Russian (Russia)
    SR_RS = "sr-RS"  # Serbian (Serbia)
    SK_SK = "sk-SK"  # Slovak (Slovakia)
    SL_SI = "sl-SI"  # Slovenian (Slovenia)
    ES_AR = "es-AR"  # Spanish (Argentina)
    ES_BO = "es-BO"  # Spanish (Bolivia)
    ES_CL = "es-CL"  # Spanish (Chile)
    ES_CO = "es-CO"  # Spanish (Colombia)
    ES_CR = "es-CR"  # Spanish (Costa Rica)
    ES_DO = "es-DO"  # Spanish (Dominican Republic)
    ES_EC = "es-EC"  # Spanish (Ecuador)
    ES_SV = "es-SV"  # Spanish (El Salvador)
    ES_GT = "es-GT"  # Spanish (Guatemala)
    ES_HN = "es-HN"  # Spanish (Honduras)
    ES_MX = "es-MX"  # Spanish (Mexico)
    ES_NI = "es-NI"  # Spanish (Nicaragua)
    ES_PA = "es-PA"  # Spanish (Panama)
    ES_PY = "es-PY"  # Spanish (Paraguay)
    ES_PE = "es-PE"  # Spanish (Peru)
    ES_PR = "es-PR"  # Spanish (Puerto Rico)
    ES_ES = "es-ES"  # Spanish (Spain)
    ES_US = "es-US"  # Spanish (United States)
    ES_UY = "es-UY"  # Spanish (Uruguay)
    ES_VE = "es-VE"  # Spanish (Venezuela)
    SV_SE = "sv-SE"  # Swedish (Sweden)
    TH_TH = "th-TH"  # Thai (Thailand)
    TR_TR = "tr-TR"  # Turkish (Turkey)
    UK_UA = "uk-UA"  # Ukrainian (Ukraine)
    VI_VN = "vi-VN"  # Vietnamese (Vietnam)
    CY_GB = "cy-GB"  # Welsh (United Kingdom)


VOICE_LANGUAGES_MAPPING = {
    Voice.TONGTONG: [LanguageCode.ZH_TW],
    Voice.VIVIAN: [LanguageCode.ZH_TW],
    Voice.MIKE: [LanguageCode.EN_US],
    Voice.MOXIE: [LanguageCode.EN_US],
    Voice.LISSA: [LanguageCode.EN_US],
    Voice.TOM: [LanguageCode.EN_US],
    Voice.ROBERT: [LanguageCode.EN_US],
    Voice.DAVID: [LanguageCode.EN_GB],
    Voice.ANNE: [LanguageCode.EN_US],
    Voice.REESE: [LanguageCode.EN_US],
}


class STTAudioFormat(str, Enum):
    WAV = "wav"
    FLAC = "flac"
    AAC = "aac"
    OPUS = "opus"
    MP3 = "mp3"
    OGG = "ogg"
    M4A = "m4a"


class STTAudioEncoding(str, Enum):
    PCM_S16 = "pcm_s16"
    PCM_S24 = "pcm_s24"
    PCM_S32 = "pcm_s32"
    PCM_F32 = "pcm_f32"
    PCM_U8 = "pcm_u8"
    PCM_ALAW = "pcm_alaw"
    PCM_MULAW = "pcm_mulaw"


@dataclass
class AbstractDataclass(ABC):
    def __new__(cls, *args, **kwargs):
        if cls == AbstractDataclass or cls.__bases__[0] == AbstractDataclass:
            raise TypeError("Cannot instantiate abstract class.")
        return super().__new__(cls)


@dataclass
class BaseCommand(AbstractDataclass):
    command: ClassVar[SpeechCommand]
    payload: Any

    def to_dict(self) -> dict:
        return {"command": self.command, "payload": asdict(self.payload)}


@dataclass
class StopCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.STOP
    payload: Any = None

    def to_dict(self) -> dict:
        return {"command": self.command}


@dataclass
class BaseAuthenticationPayload(AbstractDataclass):
    token: str
    settings: Any


@dataclass
class SpeechRecognitionSetting:
    language: str
    sample_rate: int
    itn: bool
    punctuation: bool
    contexts: dict
    context_score: float
    stt_server_id: Optional[str]
    audio_format: STTAudioFormat
    # This is only considered when audio_format is provided as wav.
    encoding: STTAudioEncoding


@dataclass
class SpeechRecognitionAuthenticationPayload(BaseAuthenticationPayload):
    token: str
    settings: SpeechRecognitionSetting


@dataclass
class SpeechRecognitionAuthenticationCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.AUTHENTICATION
    payload: SpeechRecognitionAuthenticationPayload


@dataclass
class SpeechSynthesisSetting:
    language: LanguageCode
    voice: Voice
    tts_server_id: Optional[str]


@dataclass
class SpeechSynthesisAuthenticationPayload(BaseAuthenticationPayload):
    token: str
    settings: SpeechSynthesisSetting


@dataclass
class SpeechSynthesisAuthenticationCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.AUTHENTICATION
    payload: SpeechSynthesisAuthenticationPayload


@dataclass
class AudioDataCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.AUDIO_DATA
    payload: bytes

    def to_dict(self) -> dict:
        return {
            "command": self.command,
            "payload": base64.b64encode(self.payload).decode(),
        }


@dataclass
class MultiCommands:
    commands: List[BaseCommand]
    done: asyncio.Event


@dataclass
class SynthesisSettings:
    pitch: float
    speed: float
    volume: float
    rules: str
    sample_rate: int


@dataclass
class SynthesisData:
    text: str
    ssml: bool


@dataclass
class SynthesisPayload:
    settings: SynthesisSettings
    data: SynthesisData


@dataclass
class SynthesisCommand(BaseCommand):
    command: ClassVar[SpeechCommand] = SpeechCommand.SYNTHESIS
    payload: SynthesisPayload
