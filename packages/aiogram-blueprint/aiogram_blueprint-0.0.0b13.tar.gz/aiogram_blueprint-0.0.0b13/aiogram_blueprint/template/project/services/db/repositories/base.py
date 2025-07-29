from __future__ import annotations

import abc
import typing as t
from typing import TypeVar

from sqlalchemy import (
    delete,
    select,
    update,
    func,
)
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import BaseModel
from ..types import PaginatedResult

_TBaseModel = TypeVar("_TBaseModel", bound=BaseModel)


class AbstractRepository(abc.ABC, t.Generic[_TBaseModel]):

    @abc.abstractmethod
    async def create(self, **kwargs: t.Any) -> _TBaseModel: ...

    @abc.abstractmethod
    async def get(self, **filters: t.Any) -> t.Optional[_TBaseModel]: ...

    @abc.abstractmethod
    async def list(
            self,
            order_by: t.Optional[t.Any] = None,
            **filters: t.Any,
    ) -> t.List[_TBaseModel]: ...

    @abc.abstractmethod
    async def update(self, pk: t.Any, **kwargs: t.Any) -> t.Optional[_TBaseModel]: ...

    @abc.abstractmethod
    async def delete(self, pk: t.Any) -> None: ...


class BaseRepository(AbstractRepository[_TBaseModel]):
    model: t.Type[_TBaseModel]

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, **kwargs: t.Any) -> _TBaseModel:
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.flush()
        return obj

    async def get(self, **filters: t.Any) -> t.Optional[_TBaseModel]:
        stmt = select(self.model).filter_by(**filters).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list(
            self,
            order_by: t.Optional[t.Any] = None,
            **filters: t.Any,
    ) -> t.List[_TBaseModel]:
        stmt = select(self.model).filter_by(**filters)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def update(self, pk: t.Any, **kwargs: t.Any) -> t.Optional[_TBaseModel]:
        stmt = (
            update(self.model)
            .where(self.model.get_pk_column() == pk)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete(self, pk: t.Any) -> None:
        stmt = delete(self.model).where(self.model.get_pk_column() == pk)
        await self.session.execute(stmt)

    async def count(self, **filters: t.Any) -> int:
        stmt = select(func.count()).select_from(self.model).filter_by(**filters)
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def exists(self, **filters: t.Any) -> bool:
        stmt = select(self.model).filter_by(**filters).limit(1)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() is not None

    async def paginate(
            self,
            page: int,
            page_size: int,
            order_by: t.Optional[t.Any] = None,
            **filters: t.Any,
    ) -> PaginatedResult[_TBaseModel]:
        stmt = select(self.model).filter_by(**filters)
        if order_by is not None:
            stmt = stmt.order_by(order_by)

        result = await self.session.execute(
            stmt.limit(page_size).offset((page - 1) * page_size)
        )
        items = list(result.scalars().all())

        total_items = await self.count(**filters)
        total_pages = (total_items + page_size - 1) // page_size

        return PaginatedResult(
            items=items,
            page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
        )
