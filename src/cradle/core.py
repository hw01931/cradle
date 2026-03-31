import logging
import traceback
import json
import os
import datetime
import httpx
import asyncio
from typing import Optional, Dict, Any, Callable
from functools import wraps

from cradle.diet import get_diet_traceback, get_diet_data
from cradle.config import config
from cradle.git import GitManager
from cradle.data import data_manager
from cradle.engine import get_engine
from cradle.action import action_manager
from cradle.metric import metric_manager

logger = logging.getLogger("cradle.core")

class CradleCore:
    def __init__(self):
        self.git = GitManager(dry_run=True)

    async def handle_exception(self, e: Exception, project_override: str = None):
        logger.info(f"🌌 [Cradle Hooked] Exception detected: {type(e).__name__}")
        traceback_data = json.loads(get_diet_traceback(e))
        try:
            db_context = get_diet_data(await data_manager.fetch_error_context())
        except Exception:
            db_context = "DB Context not available"
        
        final_report_data = {
            "agent": "Project Cradle",
            "version": "0.1.0-phase5",
            "timestamp": datetime.datetime.now().isoformat(),
            "project": project_override or config.get("project"),
            "trigger": "EXCEPTION",
            "error": {
                "type": traceback_data["type"],
                "msg": traceback_data["msg"],
            },
            "traceback": traceback_data["stack"],
            "db_context": db_context
        }
        
        await self.complete_reliability_loop(e, final_report_data)

    async def check_proactive_reliability(self, is_background: bool = False, project_override: str = None):
        anomaly = metric_manager.check_anomaly()
        if anomaly:
            trigger_type = "PROACTIVE_BACKGROUND" if is_background else "PROACTIVE_METRIC"
            logger.info(f"🧠 [Cradle {trigger_type}] Anomaly detected! Running diagnosis.")
            
            final_report_data = {
                "agent": "Project Cradle",
                "version": "0.1.0-phase5",
                "timestamp": datetime.datetime.now().isoformat(),
                "project": project_override or config.get("project"),
                "trigger": trigger_type,
                "anomaly": anomaly["details"],
                "metrics": anomaly["metrics"]
            }
            
            await self.complete_reliability_loop(None, final_report_data)

    async def complete_reliability_loop(self, exc: Optional[Exception], report_data: Dict[str, Any]):
        report_json = json.dumps(report_data, indent=2, ensure_ascii=False)
        logger.info(f"Report (JSON):\n{report_json}")

        engine = get_engine(config)
        diagnosis = await engine.diagnose(report_json)
        logger.info(f"🧠 [Cradle Diagnosis] Cause: {diagnosis['cause']}, Action: {diagnosis.get('recommended_action')}")

        if diagnosis.get("recommended_action"):
            action_result = await action_manager.execute(diagnosis["recommended_action"])
            report_data["action_result"] = action_result
            report_json = json.dumps(report_data, indent=2, ensure_ascii=False)

        if config.get("git.auto_pr"):
            await self._run_gitops(exc or Exception("Proactive Reliability Trigger"), report_json)
        
        webhook_url = config.get("alerts.slack_webhook")
        if webhook_url:
            await self._send_webhook(webhook_url, report_data)

    async def _send_webhook(self, url: str, data: Dict[str, Any]):
        try:
            async with httpx.AsyncClient() as client:
                error_type = data.get("error", {}).get("type", data.get("trigger"))
                msg = {
                    "text": f"🌌 *[Cradle Alert]* {error_type} in {data['project']}\n"
                            f"Timestamp: {data['timestamp']}\n"
                            f"Action Result: {data.get('action_result', {}).get('status', 'none')}"
                }
                await client.post(url, json=msg)
                logger.info("📡 [Cradle Webhook] Alert sent successfully.")
        except Exception as we:
            logger.error(f"❌ [Cradle Webhook] Failed to send alert: {str(we)}")

    async def _run_gitops(self, exc: Exception, diet_json: str):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        error_type = type(exc).__name__
        branch_name = f"cradle-fix/{error_type.lower()}_{timestamp}"
        
        try:
            self.git.create_branch(branch_name)
            log_dir = os.path.join(os.getcwd(), ".cradle", "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, f"{error_type.lower()}_report.json")
            
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(diet_json)
            
            self.git.commit_all(f"🌌 [Cradle] Auto-report for {error_type}: {str(exc)}")
            self.git.push(branch_name)
            self.git.open_pull_request(
                title=f"[Cradle] Fix requested for {error_type}",
                body=f"Cradle has detected an error:\n\n```json\n{diet_json}\n```"
            )
            logger.info(f"✅ [Cradle GitOps] Record committed to {branch_name}")
        except Exception as ge:
            logger.error(f"❌ [Cradle GitOps] Failed: {str(ge)}")

cradle_agent = CradleCore()

def cradle_watch(project: str = None, check_metrics: bool = True):
    """
    범용 에이전트 데코레이터. 
    웹 미들웨어를 통하지 않고도 어떠한 함수(데이터 파이프라인, AI 모델 학습 루프 등)도 감시합니다.
    """
    def decorator(func: Callable):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            if check_metrics:
                await cradle_agent.check_proactive_reliability(project_override=project)
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                await cradle_agent.handle_exception(e, project_override=project)
                raise e from None

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            if check_metrics:
                asyncio.run(cradle_agent.check_proactive_reliability(project_override=project))
            try:
                return func(*args, **kwargs)
            except Exception as e:
                asyncio.run(cradle_agent.handle_exception(e, project_override=project))
                raise e from None

        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator
