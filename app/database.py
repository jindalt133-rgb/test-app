import os
from collections.abc import Generator
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./employee_leave.db")
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False
engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""
def get_db() -> Generator[Session, None, None]:
    """Yield a database session for one request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
def init_db() -> None:
    """Create all database tables."""
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
