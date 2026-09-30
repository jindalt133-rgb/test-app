from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy import create_engine
from app.core.config import get_settings


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""


database_url = get_database_url()

connect_args = (
    {"check_same_thread": False}
    if database_url.startswith("sqlite")
    else {}
)

engine = create_engine(database_url, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


def get_db() -> Generator[Session, None, None]:
    """Provide a database session for a request."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def initialize_database() -> None:
    """Create all configured database tables."""
    from app.db import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
