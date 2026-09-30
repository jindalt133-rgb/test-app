from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, field_validator


def non_blank(value: str) -> str:
    normalized = value.strip()

    if not normalized:
        raise ValueError("must not be blank")

    return normalized


BookText = Annotated[
    str,
    Field(min_length=1, max_length=255),
]


class BookInput(BaseModel):
    title: BookText
    author: BookText
    isbn: Annotated[
        str,
        Field(min_length=1, max_length=64),
    ]
    category: Annotated[
        str,
        Field(min_length=1, max_length=120),
    ]
    price: Annotated[
        Decimal,
        Field(ge=0),
    ]
    quantity: Annotated[
        int,
        Field(ge=0),
    ]

    @field_validator("title", "author", "isbn", "category")
    @classmethod
    def validate_text(cls, value: str) -> str:
        return non_blank(value)


class BookResponse(BookInput):
    model_config = ConfigDict(from_attributes=True)

    id: int
