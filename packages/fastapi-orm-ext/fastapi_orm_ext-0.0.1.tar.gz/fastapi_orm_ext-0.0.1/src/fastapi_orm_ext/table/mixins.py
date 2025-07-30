import re
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import TIMESTAMP, MetaData
from sqlalchemy.orm import Mapped, declarative_mixin, declared_attr, mapped_column

from fastapi_orm_ext.table.sqltypes import UUIDIndependent

if TYPE_CHECKING:
    from pydantic import UUID4


__all__ = (
    "NameConventionMixin",
    "TableNameMixin",
    "TimestampsMixin",
    "UUIDPrimaryKeyMixin",
)


def __camel_to_snake(s: str) -> str:
    """Make camel case string to snake case string."""

    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    s = re.sub(r"__([A-Z])", r"_\1", s)
    s = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s)
    s = s.lower()
    if s.endswith("y"):
        s = s[:-1] + "ie"
    return s


def __utc_now() -> datetime:
    """Return now UTC datetime."""

    return datetime.now(tz=UTC)


@declarative_mixin
class TableNameMixin:
    """Mixin to automatically have pretty table name."""

    __abstract__: bool = True

    @declared_attr.directive
    def __tablename__(self) -> str:
        """Return name of table as class name in snake case."""

        return f"{__camel_to_snake(s=self.__name__)}s"


@declarative_mixin
class TimestampsMixin:
    """Mixin to have created_at and updated_at fields."""

    __abstract__: bool = True

    created_at: Mapped[datetime] = mapped_column(
        "created_at",
        TIMESTAMP(timezone=True),
        default=__utc_now,
        nullable=False,
        sort_order=-99,
    )

    updated_at: Mapped[datetime] = mapped_column(
        "updated_at",
        TIMESTAMP(timezone=True),
        default=__utc_now,
        onupdate=__utc_now,
        nullable=False,
        sort_order=-97,
    )


@declarative_mixin
class UUIDPrimaryKeyMixin:
    """Mixin to have UUID as PK."""

    __abstract__: bool = True

    id: Mapped["UUID4"] = mapped_column(
        UUIDIndependent,
        primary_key=True,
        index=True,
        default=uuid4,
        sort_order=-100,
    )


@declarative_mixin
class NameConventionMixin:
    """Mixin to have nice name convention."""

    __abstract__: bool = True

    metadata: MetaData = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )
