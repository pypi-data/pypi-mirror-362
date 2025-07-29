from __future__ import annotations

from redis.asyncio import Redis

from ..abstract import AbstractService
from ...config import REDIS_URL


class RedisService(AbstractService):
    __slots__ = ["redis"]

    def __init__(self) -> None:
        self.redis = Redis.from_url(url=REDIS_URL)

    async def start(self) -> None:
        await self.redis.ping()

    async def shutdown(self) -> None:
        await self.redis.aclose()
