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

    async def diagnose(self, report_json: str) -> Dict[str, Any]:
        if not self.api_key:
            logger.warning("No OpenAI API Key. Mocking results.")
            return self._mock_diagnosis(report_json)
        
        logger.info(f"🌌 [Cradle] Calling OpenAI ({self.model})...")
        # Placeholder for real API call
        return {"cause": "Identified by OpenAI", "recommended_action": "restart"}

    def _mock_diagnosis(self, report_json: str) -> Dict[str, Any]:
        data = json.loads(report_json)
        err = data.get("error", {}).get("type", "")
        return {
            "cause": f"Mock cause for {err}",
            "recommended_action": "restart" if "Value" in err else None
        }

class AnthropicEngine(BaseEngine):
    def __init__(self, api_key: str, model: str = "claude-3-opus-20240229"):
        self.api_key = api_key
        self.model = model

    async def diagnose(self, report_json: str) -> Dict[str, Any]:
        if not self.api_key:
            logger.warning("No Anthropic API Key. Mocking results.")
            return {"cause": "Mock Anthropic", "recommended_action": "scale_up"}
        
        logger.info(f"🌌 [Cradle] Calling Anthropic ({self.model})...")
        return {"cause": "Identified by Anthropic", "recommended_action": "scale_up"}

def get_engine(config_obj: Any) -> BaseEngine:
    provider = config_obj.get("provider", "openai").lower()
    api_key = config_obj.get("api_key")
    model = config_obj.get("model")

    if provider == "anthropic":
        return AnthropicEngine(api_key=api_key, model=model or "claude-3-sonnet-20240229")
    
    # Default to OpenAI
    return OpenAIEngine(api_key=api_key, model=model or "gpt-4-turbo-preview")
