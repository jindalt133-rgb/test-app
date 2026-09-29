from decimal import Decimal
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, field_validator

class BookFields(BaseModel):
    title: str = Field(..., max_length=255)
    author: str = Field(..., max_length=255)
    isbn: str = Field(..., max_length=32)
    category: str = Field(..., max_length=255)
    price: Decimal = Field(..., ge=0)
    quantity: int = Field(..., ge=0)

    @field_validator("title", "author", "isbn", "category", mode="before")
    @classmethod
    def validate_non_blank(cls, value: Any) -> Any:
        if isinstance(value, str):
            value = value.strip()
            if not value:
                raise ValueError("Field must not be blank")
        return value

class BookCreate(BookFields): pass
class BookUpdate(BookFields): pass

class BookResponse(BookFields):
    model_config = ConfigDict(from_attributes=True)
    id: int

class ErrorDetail(BaseModel):
    field: str
    message: str

class ErrorResponse(BaseModel):
    status: int
    code: str
    message: str
    errors: list[ErrorDetail] = Field(default_factory=list)

class HealthResponse(BaseModel):
    status: str