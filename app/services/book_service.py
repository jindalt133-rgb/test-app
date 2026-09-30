from fastapi import status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import AppError
from app.models.book import Book
from app.repositories.book_repository import BookRepository
from app.schemas.book import BookCreate, BookRead, BookUpdate


class BookService:
    def __init__(self, db: Session) -> None:
        self.repository = BookRepository(db)

    def create_book(self, payload: BookCreate) -> BookRead:
        if self.repository.get_by_isbn(payload.isbn) is not None:
            raise self.duplicate_isbn_error()

        book = Book(**payload.model_dump())

        try:
            return self.repository.create(book)
        except IntegrityError:
            self.repository.db.rollback()
            raise self.duplicate_isbn_error() from None

    def list_books(self) -> list[BookRead]:
        return [BookRead.model_validate(book) for book in self.repository.list()]

    

    def get_book(self, book_id: int) -> BookRead:
        book = self.repository.get_by_id(book_id)

        if book is None:
            raise self.not_found_error()

        return book

    def update_book(self, book_id: int, payload: BookUpdate) -> BookRead:
        book = self.get(book_id)

        existing = self.repository.get_by_isbn(payload.isbn)

        if existing is not None and existing.id != book_id:
            raise self.duplicate_isbn_error()

        for field, value in payload.model_dump().items():
            setattr(book, field, value)

        try:
            return self.repository.update(book)
        except IntegrityError:
            self.repository.db.rollback()
            raise self.duplicate_isbn_error() from None

    def delete_book(self, book_id: int) -> None:
        book = self.get(book_id)
        self.repository.delete(book)

    @staticmethod
    def _not_found_error(book_id: int) -> AppError:
        return AppError(
            status_code=status.HTTP_404_NOT_FOUND,
            code="BOOK_NOT_FOUND",
            message=f"Book with id {book_id} was not found",
        )

    @staticmethod
    def _duplicate_isbn_error(isbn: str) -> AppError:
        return AppError(
            status_code=status.HTTP_409_CONFLICT,
            code="ISBN_ALREADY_EXISTS",
            message=f"A book with ISBN {isbn} already exists",
        )