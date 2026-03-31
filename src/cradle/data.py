import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Dict, Any
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from cradle.config import config

logger = logging.getLogger("cradle.data")

class DataManager:
    def __init__(self, db_url: str = None, pool_size: int = 5):
        self.db_url = db_url or config.get("db.url")
        self.pool_size = pool_size or config.get("db.pool_size")
        
        logger.info(f"🗄️ [DataManager] Connecting to {self.db_url} (pool_size={self.pool_size})")
        
        engine_kwargs = {
            "future": True,
            "echo": False
        }
        if "sqlite" not in self.db_url:
            engine_kwargs["pool_size"] = self.pool_size
            
        self.engine = create_async_engine(self.db_url, **engine_kwargs)
        
        self.SessionLocal = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.SessionLocal() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                await session.rollback()
                raise e
            finally:
                await session.close()

    async def fetch_error_context(self) -> Dict[str, Any]:
        """
        에러 발생 시점의 데이터베이스 문맥 정보를 추출합니다.
        (예: 최근 Audit 로그, 시스템 설정값, 트랜잭션 현황 등)
        """
        context = {
            "db_stats": {},
            "recent_logs": []
        }
        
        try:
            async with self.get_session() as session:
                # 1. 시뮬레이션: 최근 로그 조회 (실제 테이블이 있는 경우 쿼리 수행)
                # result = await session.execute(text("SELECT message FROM audit_logs ORDER BY id DESC LIMIT 5"))
                # context["recent_logs"] = [row[0] for row in result.fetchall()]
                
                # 2. DB 기본 상태 수집
                # context["db_stats"]["connection_url"] = self.db_url
                context["db_stats"]["status"] = "connected"
                
                # Mock context for now
                context["recent_logs"] = [
                    {"t": "2026-03-27 18:00:01", "m": "User login success"},
                    {"t": "2026-03-27 18:05:22", "m": "DB Query executed"},
                ]
                
        except Exception as e:
            logger.error(f"❌ [DataManager] Context fetch failed: {str(e)}")
            context["error"] = f"Failed to fetch context: {str(e)}"
            
        return context

    async def close(self):
        await self.engine.dispose()

# Global instance
data_manager = DataManager()
