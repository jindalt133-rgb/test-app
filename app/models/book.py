from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[str] = mapped_column(String(255), nullable=False)
    isbn: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
    )
    publication_year: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    genre: Mapped[str] = mapped_column(String(255), nullable=False)
    available: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )
