from __future__ import annotations

import typing as t

from sqlalchemy.orm import (
    DeclarativeBase,
    InstrumentedAttribute,
)

from ..types import ColumnKey


class BaseModel(DeclarativeBase):
    __repr_cols__: tuple[str, ...] = ()
    __repr_cols_num__: int = 10

    def __repr__(self) -> str:
        cols = ", ".join(
            f"{col}={getattr(self, col)!r}"
            for idx, col in enumerate(self.__table__.columns.keys())
            if col in self.__repr_cols__ or idx < self.__repr_cols_num__
        )
        return f"<{self.__class__.__name__} {cols}>"

    @classmethod
    def get_pk_column(cls) -> InstrumentedAttribute:  # noqa
        pk_cols = cls.__mapper__.primary_key
        if len(pk_cols) != 1:
            raise ValueError(f"{cls.__name__} has composite or missing PK")
        return getattr(cls, pk_cols[0].key)

    @property
    def pk(self) -> int:
        return getattr(self, self.get_pk_column().key)

    def model_dump(
            self,
            *,
            exclude_none: bool = True,
            exclude: t.Optional[t.Iterable[ColumnKey]] = None,
    ) -> dict[str, t.Any]:
        exclude_set = {
            item.key if isinstance(item, InstrumentedAttribute) else str(item)
            for item in exclude or ()
        }

        result = {
            col: getattr(self, col)
            for col in self.__table__.columns.keys()
            if col not in exclude_set
        }

        if exclude_none:
            result = {k: v for k, v in result.items() if v is not None}

        return result
