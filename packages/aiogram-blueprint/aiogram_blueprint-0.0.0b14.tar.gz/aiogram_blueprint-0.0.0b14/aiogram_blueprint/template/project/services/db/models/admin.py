from __future__ import annotations

from sqlalchemy import (
    BigInteger,
    ForeignKey,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from .base import BaseModel
from .mixins import ModelCreatedAtMixin
from .user import UserModel


class AdminModel(BaseModel, ModelCreatedAtMixin):
    __tablename__ = "admins"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        nullable=False,
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey(UserModel.id),
        nullable=False,
    )
