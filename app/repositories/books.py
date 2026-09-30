"""Book repository operations."""

from __future__ import annotations

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models import Book


def create_book(session: Session, book: Book) -> Book:
    session.add(book)
    session.commit()
    session.refresh(book)
    return book


def get_book(session: Session, book_id: int) -> Book | None:
    return session.get(Book, book_id)


def list_books(session: Session, query: str | None = None) -> list[Book]:
    statement = select(Book).order_by(Book.id)
    if query:
        pattern = f"%{query}%"
        statement = statement.where(or_(Book.title.ilike(pattern), Book.author.ilike(pattern)))
    return list(session.scalars(statement).all())


def find_by_isbn(session: Session, isbn: str) -> Book | None:
    return session.scalar(select(Book).where(Book.isbn == isbn))


def update_book(session: Session, book: Book) -> Book:
    session.commit()
    session.refresh(book)
    return book


def delete_book(session: Session, book: Book) -> None:
    session.delete(book)
    session.commit()
