from redis.asyncio import Redis
from typing import Any, AsyncGenerator

from app.core.config import settings


async def get_redis_client() -> AsyncGenerator[Redis, Any]:
    async with Redis(
        host=settings.redis.host,
        port=settings.redis.port,
        db=settings.redis.db,
        password=settings.redis.password,
    ) as client:
        yield client
