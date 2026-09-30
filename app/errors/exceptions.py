from typing import Any


class ApplicationError(Exception):
    """Base class for expected application errors."""

    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details or []


class BookNotFoundError(ApplicationError):
    def __init__(self, book_id: int) -> None:
        super().__init__(
            status_code=404,
            code="BOOK_NOT_FOUND",
            message=f"Book with ID {book_id} was not found",
        )


class DuplicateISBNError(ApplicationError):
    def __init__(self) -> None:
        super().__init__(
            status_code=409,
            code="DUPLICATE_ISBN",
            message="A book with this ISBN already exists",
        )
