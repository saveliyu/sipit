from redis.asyncio import Redis


class AuthRedisRepository:
    def __init__(self, redis: Redis) -> None:
        self._redis = redis

    async def set(self, key, value, ex=None) -> None:
        return await self._redis.set(key, value, ex=ex)
