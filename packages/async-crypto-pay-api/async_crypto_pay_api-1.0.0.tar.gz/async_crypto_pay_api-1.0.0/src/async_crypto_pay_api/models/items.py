from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class Items(BaseModel, Generic[T], frozen=True):
    items: list[T]


__all__ = [
    "Items",
]
