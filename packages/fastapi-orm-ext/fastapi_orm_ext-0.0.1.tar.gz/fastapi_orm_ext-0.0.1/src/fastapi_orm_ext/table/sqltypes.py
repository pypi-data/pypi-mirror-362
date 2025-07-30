import uuid
from typing import TYPE_CHECKING, Any, override

from pydantic import UUID4
from sqlalchemy import CHAR, TypeDecorator
from sqlalchemy.types import UUID

if TYPE_CHECKING:
    from sqlalchemy import Dialect
    from sqlalchemy.sql.type_api import TypeEngine

__all__ = ("UUIDIndependent",)


class UUIDIndependent(TypeDecorator[UUID4]):
    """DB independent UUID type. Uses PostgreSQL's UUID type,
    otherwise uses CHAR(36), storing as regular strings.
    """

    class __UUIDChar(CHAR):
        """UUID type for CHAR."""

        @property
        def python_type(self) -> type[UUID4]:
            """Return python type for UUID4."""

            return UUID4

    impl: type[__UUIDChar] = __UUIDChar
    cache_ok: bool | None = True

    @override
    def load_dialect_impl(self, dialect: "Dialect") -> "TypeEngine[Any]":
        """Load dialect implementation."""

        if dialect.name == "postgresql":
            return dialect.type_descriptor(typeobj=UUID())
        return dialect.type_descriptor(typeobj=CHAR(36))

    @override
    def process_bind_param(self, value: UUID4 | str | None, dialect: "Dialect") -> str | None:
        """Process bind param."""

        if value is None:
            return value
        if dialect.name == "postgresql":
            return str(value)
        if not isinstance(value, uuid.UUID):
            return str(uuid.UUID(hex=value))
        return str(value)

    @override
    def process_result_value(self, value: UUID4 | None, dialect: "Dialect") -> UUID4 | None:
        """Process result value."""

        if value is None:
            return value
        if not isinstance(value, uuid.UUID):
            value = uuid.UUID(hex=value)
        return value
