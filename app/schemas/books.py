"""Book API schemas and validation."""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookPayload(BaseModel):
    """Shared create and update payload."""

    title: str = Field(..., max_length=255)
    author: str = Field(..., max_length=255)
    isbn: str = Field(..., max_length=50)
    category: str = Field(..., max_length=100)
    price: Decimal = Field(..., ge=0)
    quantity: int = Field(..., ge=0)

    @field_validator("title", "author", "isbn", "category")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        """Reject blank strings and normalize surrounding whitespace."""
        normalized = value.strip()
        if not normalized:
            raise ValueError("This field must not be blank.")
        return normalized


class BookCreate(BookPayload):
    """Create-book request."""


class BookUpdate(BookPayload):
    """Replace-book request."""


class BookResponse(BookPayload):
    """Book response."""

    model_config = ConfigDict(from_attributes=True)
    id: int


class HealthResponse(BaseModel):
    """Health response."""

    status: str
