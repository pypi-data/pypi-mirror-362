from __future__ import annotations

from typing import Union

from aiogram.enums import ChatMemberStatus
from sqlalchemy import (
    BigInteger,
    VARCHAR,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import BaseModel
from .mixins import ModelTimestampMixin


class UserModel(BaseModel, ModelTimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
    )
    state: Mapped[str] = mapped_column(
        VARCHAR(length=64),
        nullable=False,
        default=ChatMemberStatus.MEMBER,
    )
    language_code: Mapped[str] = mapped_column(
        VARCHAR(length=64),
        nullable=False,
    )
    full_name: Mapped[str] = mapped_column(
        VARCHAR(length=128),
        nullable=False,
    )
    username: Mapped[Union[str, None]] = mapped_column(
        VARCHAR(length=65),
        nullable=True,
    )
