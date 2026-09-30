import os
import tempfile
from collections.abc import Iterator

# Configure the isolated database before importing application modules because
# app.db.database creates its SQLAlchemy engine during import.
_test_database_directory = tempfile.TemporaryDirectory()
_test_database_path = os.path.join(
    _test_database_directory.name,
    "test_library.db",
)
os.environ["DATABASE_URL"] = f"sqlite:///{_test_database_path}"

import pytest
from fastapi.testclient import TestClient

from app.db.database import Base, engine
from app.main import app


@pytest.fixture(autouse=True)
def reset_database() -> Iterator[None]:
    """Reset application tables before and after every test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client() -> Iterator[TestClient]:
    """Provide an in-process client with application startup enabled."""
    with TestClient(app) as test_client:
        yield test_client
def client() -> Generator[TestClient, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)