import json
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import httpx
import logging

logger = logging.getLogger("cradle.engine")

class BaseEngine(ABC):
    @abstractmethod
    async def diagnose(self, diet_json: str) -> Dict[str, Any]:
        """
        에러 정보를 분석하여 문제 원인과 해결 방안(Patch)을 제안합니다.
        """
        pass

class OpenAIEngine(BaseEngine):
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"

    async def diagnose(self, diet_json: str) -> Dict[str, Any]:
        if not self.api_key:
            logger.warning("No API Key provided. Mocking diagnosis.")
            return {
                "cause": "Unknown (No API Key)",
                "fix": "Please set CRADLE_API_KEY",
                "confidence": 0.0
            }

        # prompt = f"You are an SRE agent 'Project Cradle'. Analyze this error and suggest a fix:\n{diet_json}"
        # ... 실구현은 Milestone 4 이후에 더 구체화 가능 ...
        
        logger.info(f"🌌 [Cradle Engine] Sending request to {self.model}...")
        
        # 실제 호출부 (Stub)
        return {
            "cause": "Demo Cause",
            "fix": "Demo Fix",
            "confidence": 0.8
        }

def get_engine(config: Any) -> BaseEngine:
    provider = config.get("provider")
    api_key = config.get("api_key")
    model = config.get("model")

    if provider == "openai":
        return OpenAIEngine(api_key=api_key, model=model)
    
    # 기본값으로 OpenAI 리턴 또는 다른 엔진 추가 가능
    return OpenAIEngine(api_key=api_key, model=model)
