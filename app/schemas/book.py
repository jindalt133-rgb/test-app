from pydantic import BaseModel, ConfigDict, Field, field_validator


class BookFields(BaseModel):
    title: str = Field(..., max_length=255)
    author: str = Field(..., max_length=255)
    isbn: str = Field(..., max_length=50)
    publication_year: int = Field(..., ge=1, le=9999)
    genre: str = Field(..., max_length=255)
    available: bool = True

    @field_validator("title", "author", "isbn", "genre")
    @classmethod
    def validate_text_field(cls, value: str) -> str:
        normalized = value.strip()

        if not normalized:
            raise ValueError("Field must not be blank")

        return normalized


class BookCreate(BookFields):
    pass


class BookUpdate(BookFields):
    pass


class BookResponse(BookFields):
    model_config = ConfigDict(from_attributes=True)

    id: int
