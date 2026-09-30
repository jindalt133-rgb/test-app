"""Book catalog business logic."""

from __future__ import annotations

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import ApplicationError
from app.db.models import Book
from app.repositories import books as book_repository
from app.schemas.books import BookCreate, BookUpdate


def _duplicate_isbn_error() -> ApplicationError:
    return ApplicationError(409, "DUPLICATE_ISBN", "A book with this ISBN already exists.", [{"field": "isbn", "message": "ISBN must be unique."}])


def _not_found_error() -> ApplicationError:
    return ApplicationError(404, "BOOK_NOT_FOUND", "Book not found.")


def _ensure_isbn_available(session: Session, isbn: str, exclude_book_id: int | None = None) -> None:
    existing = book_repository.find_by_isbn(session, isbn)
    if existing is not None and existing.id != exclude_book_id:
        raise _duplicate_isbn_error()


def create_book(session: Session, payload: BookCreate) -> Book:
    _ensure_isbn_available(session, payload.isbn)
    try:
        return book_repository.create_book(session, Book(**payload.model_dump()))
    except IntegrityError as exc:
        session.rollback()
        if "isbn" in str(exc).lower():
            raise _duplicate_isbn_error() from exc
        raise


def list_books(session: Session, query: str | None = None) -> list[Book]:
    normalized_query = query.strip() if query is not None else None
    return book_repository.list_books(session, normalized_query or None)


def get_book(session: Session, book_id: int) -> Book:
    book = book_repository.get_book(session, book_id)
    if book is None:
        raise _not_found_error()
    return book


def update_book(session: Session, book_id: int, payload: BookUpdate) -> Book:
    book = get_book(session, book_id)
    _ensure_isbn_available(session, payload.isbn, exclude_book_id=book_id)
    for field, value in payload.model_dump().items():
        setattr(book, field, value)
    try:
        return book_repository.update_book(session, book)
    except IntegrityError as exc:
        session.rollback()
        if "isbn" in str(exc).lower():
            raise _duplicate_isbn_error() from exc
        raise


def delete_book(session: Session, book_id: int) -> None:
    book_repository.delete_book(session, get_book(session, book_id))
