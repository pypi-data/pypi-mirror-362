from __future__ import annotations

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from .models import BaseModel
from ..abstract import AbstractService
from ...config import DB_URL


class DBService(AbstractService):
    __slots__ = ["engine", "session_factory"]

    def __init__(self) -> None:
        self.engine: AsyncEngine = create_async_engine(
            url=DB_URL,
            pool_pre_ping=True,
        )
        self.session_factory: async_sessionmaker = async_sessionmaker(
            bind=self.engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )

    async def start(self) -> None:
        async with self.engine.begin() as conn:
            await conn.run_sync(BaseModel.metadata.create_all)

    async def shutdown(self) -> None:
        await self.engine.dispose()
