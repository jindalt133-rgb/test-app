from dataclasses import dataclass, field

@dataclass
class AppError(Exception):
    status_code: int
    code: str
    message: str
    errors: list[dict[str, str]] = field(default_factory=list)

class BookNotFoundError(AppError):
    def __init__(self, book_id: int) -> None:
        super().__init__(404, "BOOK_NOT_FOUND", f"Book with ID {book_id} was not found")

class DuplicateISBNError(AppError):
    def __init__(self, isbn: str) -> None:
        super().__init__(409, "DUPLICATE_ISBN", f"ISBN '{isbn}' is already assigned to another book")