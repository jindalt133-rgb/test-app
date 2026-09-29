from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app import models
from app.exceptions import BookNotFoundError, DuplicateISBNError
from app.repositories import book_repository
from app.schemas import BookCreate, BookUpdate

def create_book(db: Session, payload: BookCreate) -> models.Book:
    if book_repository.get_by_isbn(db, payload.isbn) is not None: raise DuplicateISBNError(payload.isbn)
    book = models.Book(**payload.model_dump())
    try: return book_repository.create(db, book)
    except IntegrityError as exc:
        db.rollback(); raise DuplicateISBNError(payload.isbn) from exc
def list_books(db: Session, search: str | None = None) -> list[models.Book]:
    return book_repository.list_books(db, search.strip() if search is not None and search.strip() else None)
def get_book(db: Session, book_id: int) -> models.Book:
    book = book_repository.get_by_id(db, book_id)
    if book is None: raise BookNotFoundError(book_id)
    return book
def update_book(db: Session, book_id: int, payload: BookUpdate) -> models.Book:
    book = get_book(db, book_id)
    existing = book_repository.get_by_isbn(db, payload.isbn)
    if existing is not None and existing.id != book_id: raise DuplicateISBNError(payload.isbn)
    for field_name, value in payload.model_dump().items(): setattr(book, field_name, value)
    try: return book_repository.save(db, book)
    except IntegrityError as exc:
        db.rollback(); raise DuplicateISBNError(payload.isbn) from exc
def delete_book(db: Session, book_id: int) -> None:
    book_repository.delete(db, get_book(db, book_id))