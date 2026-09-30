from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.db.models import Book


class BookRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, book: Book) -> Book:
        self.db.add(book)
        self.db.commit()
        self.db.refresh(book)
        return book

    def list_all(self) -> list[Book]:
        statement = select(Book).order_by(Book.id)
        return list(self.db.scalars(statement).all())

    def get_by_id(self, book_id: int) -> Book | None:
        return self.db.get(Book, book_id)

    def get_by_isbn(self, isbn: str) -> Book | None:
        statement = select(Book).where(Book.isbn == isbn)
        return self.db.scalar(statement)

    def search(self, term: str) -> list[Book]:
        pattern = f"%{term}%"
        statement = (
            select(Book)
            .where(
                or_(
                    Book.title.ilike(pattern),
                    Book.author.ilike(pattern),
                )
            )
            .order_by(Book.id)
        )
        return list(self.db.scalars(statement).all())

    def update(self, book: Book) -> Book:
        self.db.commit()
        self.db.refresh(book)
        return book

    def delete(self, book: Book) -> None:
        self.db.delete(book)
        self.db.commit()