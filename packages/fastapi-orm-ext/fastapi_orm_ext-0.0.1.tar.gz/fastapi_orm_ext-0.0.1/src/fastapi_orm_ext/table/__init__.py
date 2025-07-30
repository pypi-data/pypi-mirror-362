from fastapi_orm_ext.table.mixins import (
    NameConventionMixin,
    TableNameMixin,
    TimestampsMixin,
    UUIDPrimaryKeyMixin,
)

__all__ = ("TableBase",)


class TableBase(
    NameConventionMixin,
    TableNameMixin,
    TimestampsMixin,
    UUIDPrimaryKeyMixin,
):
    """Base class for SQLAlchemy tables.

    This class combines several mixins to provide a consistent table structure.
    It includes automatic table naming, UUID primary key, and timestamp fields.
    """

    __abstract__: bool = True
