"""
음성 처리 유틸리티 - 노인 친화적
STT: Google Speech Recognition
TTS: Google Text-to-Speech (gTTS)
"""
import speech_recognition as sr
from gtts import gTTS
import io
from typing import Optional
from enum import Enum


class TranscriptionResult(Enum):
    """음성 인식 결과 상태"""
    SUCCESS = "success"
    EMPTY = "empty"
    API_ERROR = "api_error"
    UNKNOWN_ERROR = "unknown_error"


def transcribe_audio(audio_bytes: dict) -> Optional[str]:
    """
    음성 바이트를 텍스트로 변환
    Google Speech-to-Text API 사용

    Args:
        audio_bytes: mic_recorder에서 반환된 딕셔너리 {'bytes': bytes, ...}

    Returns:
        인식된 텍스트 문자열
        None: 입력 없음 또는 인식 실패
        "API_ERROR": API 연결 실패
    """
    # 입력 검증
    if not audio_bytes:
        return None

    # mic_recorder 반환 형식 처리
    if isinstance(audio_bytes, dict):
        audio_data_bytes = audio_bytes.get('bytes')
        if not audio_data_bytes:
            return None
    else:
        audio_data_bytes = audio_bytes

    try:
        recognizer = sr.Recognizer()

        # WAV 바이트를 AudioData로 변환
        audio_data = sr.AudioData(
            audio_data_bytes, 
            sample_rate=16000, 
            sample_width=2
        )

        # Google Speech-to-Text API 호출
        text = recognizer.recognize_google(audio_data, language="ko-KR")

        # 빈 문자열 체크
        if text and text.strip():
            return text.strip()
        return None

    except sr.UnknownValueError:
        # 음성이 인식되지 않음
        return None
    except sr.RequestError as e:
        # API 연결 실패
        print(f"Google STT API 에러: {e}")
        return "API_ERROR"
    except Exception as e:
        # 기타 에러
        print(f"음성 변환 에러: {e}")
        return "API_ERROR"


def text_to_speech(text: str, lang: str = 'ko', slow: bool = False) -> Optional[bytes]:
    """
    텍스트를 음성으로 변환
    gTTS (Google Text-to-Speech) 사용

    Args:
        text: 변환할 텍스트
        lang: 언어 코드 (기본값: 한국어)
        slow: 느린 발음 여부

    Returns:
        MP3 오디오 바이트 또는 None
    """
    # 입력 검증
    if not text or not text.strip():
        return None

    try:
        # gTTS로 음성 생성
        tts = gTTS(text=text.strip(), lang=lang, slow=slow)

        # 바이트 버퍼에 저장
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        return audio_buffer.read()

    except Exception as e:
        print(f"TTS 에러: {e}")
        return None


def is_api_error(result: Optional[str]) -> bool:
    """API 에러 여부 확인 헬퍼 함수"""
    return result == "API_ERROR"


def is_valid_transcription(result: Optional[str]) -> bool:
    """유효한 음성 인식 결과인지 확인"""
    return result is not None and result != "API_ERROR" and len(result.strip()) > 0