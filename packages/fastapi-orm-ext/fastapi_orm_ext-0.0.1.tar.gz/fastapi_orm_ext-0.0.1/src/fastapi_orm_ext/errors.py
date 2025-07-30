from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pydantic import UUID4

__all__ = (
    "ObjectNotFoundError",
    "RepositoryConsistentError",
)


class ObjectNotFoundError(Exception):
    def __init__(self, id_: "str | UUID4") -> None:
        msg: str = f"Object with id {id_} not found."
        super().__init__(msg)


class RepositoryConsistentError(Exception):
    pass
