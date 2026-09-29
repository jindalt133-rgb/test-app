import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base
from app.dependencies import database_session
from app.main import app

@pytest.fixture
def client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    testing_session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)
    Base.metadata.create_all(bind=engine)
    def override_database_session():
        db = testing_session_local()
        try: yield db
        finally: db.close()
    app.dependency_overrides[database_session] = override_database_session
    try:
        with TestClient(app) as test_client: yield test_client
    finally:
        app.dependency_overrides.clear(); Base.metadata.drop_all(bind=engine); engine.dispose()
@pytest.fixture
def book_payload():
    return {"title":"The Pragmatic Programmer","author":"Andrew Hunt","isbn":"9780135957059","category":"Software Engineering","price":49.99,"quantity":10}