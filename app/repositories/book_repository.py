from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.book import Book


class BookRepository:
    """Database access operations for books."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def list_books(self) -> list[Book]:
        statement = select(Book).order_by(Book.id)
        return list(self.db.scalars(statement).all())

    def get_by_id(self, book_id: int) -> Book | None:
        return self.db.get(Book, book_id)

    def get_by_isbn(self, isbn: str) -> Book | None:
        statement = select(Book).where(Book.isbn == isbn)
        return self.db.scalars(statement).first()

    def add(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def delete(self, book: Book) -> None:
        self.db.delete(book)
        self.db.commit()
