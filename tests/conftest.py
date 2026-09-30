"""Pytest fixtures for isolated library catalog API tests."""

from __future__ import annotations

import os
import tempfile
from collections.abc import Generator

_TEST_DATABASE_DIRECTORY = tempfile.TemporaryDirectory(prefix="library-catalog-tests-")
_TEST_DATABASE_PATH = os.path.join(_TEST_DATABASE_DIRECTORY.name, "test-library.db")
os.environ["DATABASE_URL"] = f"sqlite:///{_TEST_DATABASE_PATH}"

import pytest
from fastapi.testclient import TestClient

from app.db.database import Base, engine
from app.main import app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)