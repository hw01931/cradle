import logging
import asyncio
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from cradle.config import config

logger = logging.getLogger("cradle.action")

class BaseAction(ABC):
    @abstractmethod
    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        액션을 실행하고 결과를 반환합니다.
        """
        pass

class MockCloudAction(BaseAction):
    def __init__(self, action_type: str):
        self.action_type = action_type

    async def run(self, params: Dict[str, Any]) -> Dict[str, Any]:
        logger.info(f"☁️ [MockCloud] Simulating {self.action_type} with params: {params}")
        await asyncio.sleep(1) # Simulate network latency
        return {
            "status": "success",
            "action": self.action_type,
            "message": f"Successfully simulated {self.action_type}"
        }

class ActionManager:
    def __init__(self, dry_run: bool = None):
        cfg_dry_run = config.get("action.dry_run", True)
        self.dry_run = dry_run if dry_run is not None else cfg_dry_run
        self.allowed_actions = config.get("action.allowed_actions", [])
        self.require_approval = config.get("action.require_approval", [])
        self.pending_actions: Dict[str, Dict[str, Any]] = {}

    async def execute(self, action_type: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        지정된 액션을 안전하게 실행합니다. (승인 로직 포함)
        """
        params = params or {}
        
        # 1. 권한 체크
        if action_type not in self.allowed_actions:
            logger.warning(f"🚫 [ActionManager] Action '{action_type}' is NOT allowed.")
            return {"status": "denied", "reason": f"Action '{action_type}' is not in allowed_actions"}

        # 2. 승인 체크
        if action_type in self.require_approval:
            import uuid
            action_id = str(uuid.uuid4())[:8]
            self.pending_actions[action_id] = {"type": action_type, "params": params}
            
            logger.info(f"⏳ [ActionManager] Action '{action_type}' is pending approval (ID: {action_id}).")
            return {
                "status": "pending_approval",
                "action_id": action_id,
                "msg": f"Action '{action_type}' requires human approval. Run `cradle approve {action_id}`"
            }

        # 3. Dry Run 체크
        if self.dry_run:
            logger.info(f"🌵 [ActionManager] Dry Run: {action_type} with {params}")
            return {
                "status": "dry_run",
                "action": action_type,
                "msg": f"Action {action_type} would have been executed (Dry Run)"
            }

        # 4. 실제 실행 (Stub/Mock)
        return await self._perform_real_action(action_type, params)

    async def approve(self, action_id: str) -> Dict[str, Any]:
        """
        대기 중인 액션을 승인하고 실행합니다.
        """
        if action_id not in self.pending_actions:
            return {"status": "error", "msg": f"Action ID {action_id} not found."}
        
        pending = self.pending_actions.pop(action_id)
        logger.info(f"✅ [ActionManager] Action {action_id} ({pending['type']}) approved by human.")
        
        # 승인 시에는 Dry Run 설정을 무시하고 실행하는 것이 보통이지만, 
        # 안전을 위해 config 설정을 따르거나 강제 실행할 수 있음.
        return await self._perform_real_action(pending["type"], pending["params"])

    async def _perform_real_action(self, action_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        action = MockCloudAction(action_type)
        try:
            result = await action.run(params)
            logger.info(f"🚀 [ActionManager] Action {action_type} executed: {result['status']}")
            return result
        except Exception as e:
            logger.error(f"❌ [ActionManager] Action {action_type} failed: {str(e)}")
            return {"status": "failed", "error": str(e)}

# Global instance
action_manager = ActionManager()
