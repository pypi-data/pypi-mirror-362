"""Common response schemas for API endpoints."""

from typing import Any, TypeVar, Generic

from pydantic import BaseModel


__all__ = (
    "ResponseBase",
    "SuccessResponse",
    "FailedResponse",
)


T = TypeVar("T")


class ResponseBase(BaseModel):
    """Base structure returned by every API endpoint."""

    success: bool


class SuccessResponse(ResponseBase, Generic[T]):
    """Successful API response wrapper."""

    success: bool = True
    data: Any


class FailedResponse(ResponseBase):
    """Error response wrapper."""

    success: bool = False
    message: str
