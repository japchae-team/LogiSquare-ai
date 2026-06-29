from typing import Generic, TypeVar

from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")


class ApiResponse(GenericModel, Generic[T]):
    success: bool
    data: T | None = None
    message: str = ""


class ErrorResponse(BaseModel):
    success: bool = False
    data: None = None
    message: str

