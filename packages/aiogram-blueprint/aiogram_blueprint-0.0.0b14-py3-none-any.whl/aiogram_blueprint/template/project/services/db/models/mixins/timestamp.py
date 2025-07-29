from datetime import (
    datetime,
    timezone,
)

from sqlalchemy import DateTime
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class ModelCreatedAtMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class ModelUpdatedAtMixin:
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class ModelTimestampMixin(ModelCreatedAtMixin, ModelUpdatedAtMixin): ...
