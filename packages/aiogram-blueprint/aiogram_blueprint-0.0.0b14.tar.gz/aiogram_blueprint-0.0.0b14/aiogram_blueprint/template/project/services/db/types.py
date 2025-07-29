import typing as t

from pydantic import BaseModel
from sqlalchemy.orm import InstrumentedAttribute

_T = t.TypeVar("_T")

ColumnKey = t.Union[str, InstrumentedAttribute]


class PaginatedResult(BaseModel, t.Generic[_T]):
    items: t.List[_T]
    page: int
    page_size: int
    total_items: int
    total_pages: int
