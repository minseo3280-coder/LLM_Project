"""
LLM Engine - Ollama 기반 로컬 LLM 엔진
"""
import requests
import json
from typing import Optional

class OllamaEngine:
    """Ollama (로컬 LLM) 엔진"""

    def __init__(
        self,
        model: str = "gemma2:latest",
        base_url: str = "http://localhost:11434",
        timeout: int = 300
    ):
        self.model = model
        self.base_url = base_url
        self.timeout = timeout
        self.is_available = self._check_connection()

    def _check_connection(self) -> bool:
        """Ollama 서버 연결 확인"""
        try:
            response = requests.get(f"{self.base_url}", timeout=3)
            return response.status_code == 200
        except requests.RequestException:
            return False

    def generate_response(self, prompt: str, json_mode: bool = True) -> Optional[str]:
        """
        LLM 응답 생성

        Args:
            prompt: 입력 프롬프트
            json_mode: JSON 형식 강제 여부

        Returns:
            생성된 응답 텍스트 또는 None
        """
        if not self.is_available:
            return None

        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3 if json_mode else 0.7,
                    "num_ctx": 4096
                }
            }

            # JSON 모드일 때만 포맷 강제
            if json_mode:
                payload["format"] = "json"

            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=self.timeout
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()

            print(f"Ollama API Error: {response.status_code}")
            return None

        except requests.Timeout:
            print("Ollama 타임아웃 에러")
            return None
        except requests.RequestException as e:
            print(f"Ollama 연결 에러: {e}")
            return None
        except Exception as e:
            print(f"Ollama 에러: {e}")
            return None


# 싱글톤 인스턴스 관리
_engine: Optional[OllamaEngine] = None

def get_engine(engine_type: str = "ollama", **kwargs) -> Optional[OllamaEngine]:
    """
    LLM 엔진 싱글톤 인스턴스 반환

    Args:
        engine_type: 엔진 타입 (현재 ollama만 지원)
        **kwargs: 엔진 초기화 파라미터

    Returns:
        OllamaEngine 인스턴스 또는 None
    """
    global _engine
    if _engine is None:
        if engine_type == "ollama":
            _engine = OllamaEngine(**kwargs)
    return _engine