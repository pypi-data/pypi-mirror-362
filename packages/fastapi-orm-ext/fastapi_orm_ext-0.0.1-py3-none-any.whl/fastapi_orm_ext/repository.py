from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, override

from sqlalchemy import select

from fastapi_orm_ext.errors import ObjectNotFoundError, RepositoryConsistentError

if TYPE_CHECKING:
    from collections.abc import Iterable, Sequence

    from pydantic import UUID4, BaseModel
    from sqlalchemy.ext.asyncio import AsyncSession
    from sqlalchemy.sql.selectable import ForUpdateParameter


class IBaseRepository[Model: BaseModel](ABC):
    """Interface for any repositories."""

    @abstractmethod
    async def refresh(
        self,
        instance: Model,
        attribute_names: "Iterable[str] | None" = None,
        with_for_update: "ForUpdateParameter" = None,
    ) -> None:
        """Refresh instance from database."""

    @abstractmethod
    async def get(self, id_: "str | UUID4") -> Model | None:
        """Get instance by ID."""

    @abstractmethod
    async def all(self) -> "Sequence[Model] | None":
        """Get all instances from table."""

    @abstractmethod
    async def create(self, model: Model) -> Model:
        """Create new instance in table."""

    @abstractmethod
    async def bulk_create(self, models: "Sequence[Model]") -> "Sequence[Model]":
        """Create new instances in table."""

    @abstractmethod
    async def update(self, id_: "str | UUID4", model: Model) -> Model:
        """Update instance in table by ID."""

    @abstractmethod
    async def delete(self, id_: "str | UUID4") -> None:
        """Delete instance from table by ID."""


class BaseRepository[Model: BaseModel](IBaseRepository[Model], ABC):
    """Base class for SQLAlchemy repository."""

    model: Model
    auto_commit: bool
    auto_flush: bool

    def _check_consistent(self) -> None:
        """Check if repository is consistent."""

        msg: str = ""
        if self.auto_commit is False and self.auto_flush is False:
            msg = "You should specify 'auto_commit' or 'auto_flush parameter."
            raise RepositoryConsistentError(msg)
        if self.auto_commit is True and self.auto_flush is True:
            msg = "You should set in 'True' only one parameter: 'auto_commit' or 'auto_flush', not both of them."
            raise RepositoryConsistentError(msg)
        if not self.model:
            msg = "You should specify 'model' parameter."
            raise RepositoryConsistentError(msg)


class Repository[Model: BaseModel](BaseRepository[Model], ABC):
    """Base class for all SQLAlchemy repositories."""

    model: Model
    auto_commit: bool = False
    auto_flush: bool = True

    def __init__(self, session: "AsyncSession") -> None:
        self.session: AsyncSession = session
        self._check_consistent()

    @staticmethod
    def _get_create_data(model: Model) -> dict[str, Any]:
        """Return dict data a for creating new instance."""

        return model.model_dump()

    @staticmethod
    def _get_update_data(model: Model) -> dict[str, Any]:
        """Return dict data a for updating new instance."""

        return model.model_dump(exclude_unset=True)

    async def commit(self) -> None:
        if self.auto_commit:
            await self.session.commit()
        else:
            await self.session.flush()

    @override
    async def refresh(
        self,
        instance: Model,
        attribute_names: "Iterable[str] | None" = None,
        with_for_update: "ForUpdateParameter" = None,
    ) -> None:
        if self.auto_commit:
            await self.session.refresh(
                instance=instance,
                attribute_names=attribute_names,
                with_for_update=with_for_update,
            )

    @override
    async def get(self, id_: "str | UUID4") -> Model | None:
        """Get instance by ID."""

        return (
            await self.session.execute(
                statement=select(self.model).where(self.model.id == id_),
            )
        ).scalar()

    @override
    async def all(self) -> "Sequence[Model] | None":
        return (
            (
                await self.session.execute(
                    statement=select(self.model),
                )
            )
            .scalars()
            .all()
        )

    @override
    async def create(self, model: Model) -> Model:
        data: dict[str, Any] = self._get_create_data(model=model)
        instance: Model = self.model(**data)
        self.session.add(instance)
        await self.commit()
        await self.refresh(instance)
        return instance

    @override
    async def bulk_create(self, models: "Sequence[Model]") -> "Sequence[Model]":
        instances: list[Model] = [self.model(**self._get_create_data(model=model)) for model in models]
        self.session.add_all(instances=instances)

        await self.commit()

        for instance in instances:
            await self.refresh(instance=instance)

        return instances

    @override
    async def update(self, id_: "str | UUID4", model: Model) -> Model:
        instance: Model | None = await self.get(id_=id_)
        if not instance:
            raise ObjectNotFoundError(id_=id_) from None

        data: dict[str, Any] = self._get_update_data(model=model)
        for k, v in data:
            setattr(instance, k, v)

        await self.commit()
        await self.refresh(instance)

        return instance

    @override
    async def delete(self, id_: "str | UUID4") -> None:
        instance: Model | None = await self.get(id_=id_)
        if instance is None:
            raise ObjectNotFoundError(id_=id_) from None

        await self.session.delete(instance=instance)
        await self.commit()
