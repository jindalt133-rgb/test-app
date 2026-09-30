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


class BookFields(BaseModel):
    title: NonBlankString
    author: NonBlankString
    isbn: Annotated[str, Field(min_length=1, max_length=32)]
    publication_year: StrictInt
    genre: Annotated[str, Field(min_length=1, max_length=100)]
    available: StrictBool

    @field_validator("title", "author", "isbn", "category")
    @classmethod
    def validate_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field must not be blank")
        return value


class BookCreate(BookFields):
    pass


class BookUpdate(BookFields):
    pass


class BookRead(BookFields):
    model_config = ConfigDict(from_attributes=True)

    id: int
    model_config = ConfigDict(from_attributes=True)
