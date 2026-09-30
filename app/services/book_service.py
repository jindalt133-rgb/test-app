from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.errors.exceptions import (
    BookNotFoundError,
    DuplicateISBNError,
)
from app.models.book import Book
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookUpdate


class BookService:
    """Business operations for books."""

    def __init__(self, db: Session) -> None:
        self.repository = BookRepository(db)

    def list_books(self) -> list[Book]:
        return self.repository.list_books()

    def get_book(self, book_id: int) -> Book:
        book = self.repository.get_by_id(book_id)

        if book is None:
            raise BookNotFoundError(book_id)

        return book

    def create_book(self, book_data: BookCreate) -> Book:
        if self.repository.get_by_isbn(book_data.isbn) is not None:
            raise DuplicateISBNError()

        book = Book(**book_data.model_dump())

        try:
            return self.repository.add(book)
        except IntegrityError as exc:
            raise DuplicateISBNError() from exc

    def update_book(self, book_id: int, book_data: BookUpdate) -> Book:
        book = self.get_book(book_id)

        existing = self.repository.get_by_isbn(book_data.isbn)

        if existing is not None and existing.id != book_id:
            raise DuplicateISBNError()

        for field, value in book_data.model_dump().items():
            setattr(book, field, value)

        try:
            return self.repository.add(book)
        except IntegrityError as exc:
            raise DuplicateISBNError() from exc

    def delete_book(self, book_id: int) -> None:
        book = self.get_book(book_id)
        self.repository.delete(book)
