import logging
import traceback
import json
import os
import datetime
from typing import Optional, Dict, Any
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
from cradle.diet import get_diet_traceback, get_diet_data
from cradle.config import config
from cradle.git import GitManager
from cradle.data import data_manager
from cradle.engine import get_engine
from cradle.action import action_manager
from cradle.metric import metric_manager
import httpx
import asyncio

from cradle.core import cradle_agent

logger = logging.getLogger("cradle")

class CradleMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self._bg_task = None
        self._start_background_monitor()
        logger.info("🌌 [Cradle Middleware] Initialized with Universal Foundation Core")

    def _start_background_monitor(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                self._bg_task = asyncio.create_task(self._background_monitoring_loop())
        except Exception as e:
            logger.warning(f"⚠️ [Cradle] Could not start background monitor: {e}")

    async def _background_monitoring_loop(self):
        interval = config.get("metrics.interval", 60)
        logger.info(f"🛰️ [Cradle Sentinel] Background loop started (Interval: {interval}s)")
        
        while True:
            try:
                await asyncio.sleep(interval)
                await cradle_agent.check_proactive_reliability(is_background=True)
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"❌ [Cradle Sentinel] Error in background loop: {e}")

    async def dispatch(self, request: Request, call_next) -> Response:
        await cradle_agent.check_proactive_reliability()
        
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            await cradle_agent.handle_exception(e)
            raise e from None
