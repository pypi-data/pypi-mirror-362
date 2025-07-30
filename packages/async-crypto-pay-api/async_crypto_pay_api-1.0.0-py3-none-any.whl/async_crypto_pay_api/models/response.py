from typing import Generic, TypeVar

from pydantic import BaseModel

R = TypeVar("R")


class Error(BaseModel, frozen=True):
    code: int
    name: str


class Response(BaseModel, Generic[R], frozen=True):
    ok: bool
    result: R | None = None
    error: Error | None = None


__all__ = [
    "Error",
    "Response",
]
