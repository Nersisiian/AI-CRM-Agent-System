import json
from typing import List, Dict
import redis.asyncio as aioredis
from config import settings
import structlog

logger = structlog.get_logger(__name__)

class MemoryManager:
    def __init__(self):
        self.redis = aioredis.from_url(settings.REDIS_URL, decode_responses=True)
        self.ttl = 3600

    async def get_history(self, session_id: str) -> List[Dict[str, str]]:
        try:
            data = await self.redis.get(f"session:{session_id}")
            if data:
                return json.loads(data)
            return []
        except Exception as e:
            logger.error("redis get error", error=str(e))
            return []

    async def add_message(self, session_id: str, role: str, content: str):
        try:
            history = await self.get_history(session_id)
            history.append({"role": role, "content": content})
            await self.redis.setex(
                f"session:{session_id}",
                self.ttl,
                json.dumps(history),
            )
        except Exception as e:
            logger.error("redis set error", error=str(e))

    async def clear_history(self, session_id: str):
        await self.redis.delete(f"session:{session_id}")