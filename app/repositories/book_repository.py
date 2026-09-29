from sqlalchemy import or_, select
from sqlalchemy.orm import Session
from app.models import Book

def create(db: Session, book: Book) -> Book:
    db.add(book); db.commit(); db.refresh(book); return book
def get_by_id(db: Session, book_id: int) -> Book | None:
    return db.scalar(select(Book).where(Book.id == book_id))
def get_by_isbn(db: Session, isbn: str) -> Book | None:
    return db.scalar(select(Book).where(Book.isbn == isbn))
def list_books(db: Session, search: str | None = None) -> list[Book]:
    statement = select(Book).order_by(Book.id)
    if search:
        pattern = f"%{search}%"
        statement = statement.where(or_(Book.title.ilike(pattern), Book.author.ilike(pattern)))
    return list(db.scalars(statement).all())
def save(db: Session, book: Book) -> Book:
    db.commit(); db.refresh(book); return book
def delete(db: Session, book: Book) -> None:
    db.delete(book); db.commit()