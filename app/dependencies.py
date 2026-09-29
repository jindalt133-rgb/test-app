from collections.abc import Generator
from sqlalchemy.orm import Session
from app.database import get_db

def database_session() -> Generator[Session, None, None]:
    """Provide the request-scoped database session dependency."""
    yield from get_db()