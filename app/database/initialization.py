from app.database.base import Base
from app.database.session import engine
from app.models.book import Book


def initialize_database() -> None:
    """Create all database tables if they do not already exist."""
    Base.metadata.create_all(bind=engine)
