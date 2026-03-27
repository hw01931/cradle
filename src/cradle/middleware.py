import logging
import traceback
import json
import os
import datetime
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from src.cradle.diet import get_diet_traceback
from src.cradle.config import config
from src.cradle.git import GitManager

logger = logging.getLogger("cradle")

class CradleMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.git = GitManager(dry_run=True) # Default dry_run
        logger.info("🌌 [Cradle Middleware] Initialized with GitOps capabilities")

    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            # 1. Token Diet Traceback
            diet_json = get_diet_traceback(e)
            
            logger.error(f"🌌 [Cradle Hooked] Exception caught: {str(e)}")
            logger.info(f"Diet Traceback (JSON):\n{diet_json}")

            # 2. GitOps Flow (Branch -> Commit)
            if config.get("git.auto_pr"):
                await self._run_gitops(e, diet_json)
            
            # Re-raise to let the default handler work
            raise e from None

    async def _run_gitops(self, exc: Exception, diet_json: str):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        error_type = type(exc).__name__
        branch_name = f"cradle-fix/{error_type.lower()}_{timestamp}"
        
        try:
            # Create branch
            self.git.create_branch(branch_name)
            
            # Save error report to a new file
            log_dir = os.path.join(os.getcwd(), ".cradle", "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, f"{error_type.lower()}_report.json")
            
            with open(log_path, "w", encoding="utf-8") as f:
                f.write(diet_json)
            
            # Commit and Push
            self.git.commit_all(f"🌌 [Cradle] Auto-report for {error_type}: {str(exc)}")
            self.git.push(branch_name)
            
            # Open PR (Stub)
            self.git.open_pull_request(
                title=f"[Cradle] Fix requested for {error_type}",
                body=f"Cradle has detected an error:\n\n```json\n{diet_json}\n```"
            )
            
            logger.info(f"✅ [Cradle GitOps] Successfully initiated for {branch_name}")
        except Exception as ge:
            logger.error(f"❌ [Cradle GitOps] Failed: {str(ge)}")
