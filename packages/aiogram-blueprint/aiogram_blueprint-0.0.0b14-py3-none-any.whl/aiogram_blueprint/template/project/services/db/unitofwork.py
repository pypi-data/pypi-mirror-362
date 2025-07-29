from __future__ import annotations

import abc
import typing as t

from sqlalchemy.ext.asyncio.session import (
    AsyncSession,
    AsyncSessionTransaction,
    async_sessionmaker,
)

from .repositories import (
    AdminRepository,
    UserRepository,
)


class AbstractUnitOfWork(abc.ABC):

    @abc.abstractmethod
    async def __aenter__(self) -> AbstractUnitOfWork: ...

    @abc.abstractmethod
    async def __aexit__(
            self,
            exc_type: t.Optional[t.Type[BaseException]],
            exc: t.Optional[BaseException],
            tb: t.Optional[t.Any],
    ) -> None: ...

    @abc.abstractmethod
    async def commit(self) -> None: ...

    @abc.abstractmethod
    async def rollback(self) -> None: ...


class UnitOfWork(AbstractUnitOfWork):
    session: AsyncSession
    transaction: AsyncSessionTransaction

    def __init__(self, session_factory: async_sessionmaker) -> None:
        self.session_factory: async_sessionmaker = session_factory

    async def __aenter__(self) -> UnitOfWork:
        self.session = self.session_factory()
        self.transaction = await self.session.begin()

        self.admin_repo = AdminRepository(self.session)
        self.user_repo = UserRepository(self.session)

        return self

    async def __aexit__(
            self,
            exc_type: t.Optional[t.Type[BaseException]],
            exc: t.Optional[BaseException],
            tb: t.Optional[t.Any],
    ) -> None:
        if exc_type:
            await self.rollback()
        else:
            await self.commit()
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
