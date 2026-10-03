"""Pydantic request and response models."""

from typing import Any

from pydantic import BaseModel, ConfigDict, field_validator


class TaskCreate(BaseModel):
    """Payload used to create a task."""

    title: str
    completed: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        """Reject blank titles and normalize surrounding whitespace."""
        normalized = value.strip()
        if not normalized:
            raise ValueError("title must not be blank")
        return normalized


class TaskResponse(BaseModel):
    """Task returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool


class ValidationErrorResponse(BaseModel):
    """Structured validation error response."""

    code: str
    detail: list[dict[str, Any]]


class ErrorDetail(BaseModel):
    """Structured task error detail."""

    code: str
    message: str


class ErrorResponse(BaseModel):
    """Structured API error response."""

    detail: ErrorDetail
