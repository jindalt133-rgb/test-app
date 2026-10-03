from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session, sessionmaker

from app.database import Base, get_db
from app.main import app


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Provide an isolated in-memory SQLite database for each test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False,
    )

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)

    try:
        yield test_client
    finally:
        app.dependency_overrides.clear()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def employee_payload(
    *,
    name: str = "Jane Smith",
    email: str = "jane.smith@example.com",
    department: str = "Engineering",
    active: bool = True,
) -> dict:
    return {
        "name": name,
        "email": email,
        "department": department,
        "active": active,
    }


def leave_payload(
    employee_id: int,
    *,
    leave_type: str = "ANNUAL",
    start_date: str = "2025-06-02",
    end_date: str = "2025-06-06",
    reason: str | None = "Annual vacation",
) -> dict:
    return {
        "employee_id": employee_id,
        "leave_type": leave_type,
        "start_date": start_date,
        "end_date": end_date,
        "reason": reason,
    }


def create_employee(
    client: TestClient,
    *,
    email: str = "jane.smith@example.com",
    active: bool = True,
) -> dict:
    response = client.post(
        "/employees",
        json=employee_payload(email=email, active=active),
    )
    assert response.status_code == 201
    return response.json()


def create_leave_request(
    client: TestClient,
    employee_id: int,
    **kwargs,
) -> dict:
    response = client.post(
        "/leave-requests",
        json=leave_payload(employee_id, **kwargs),
    )
    assert response.status_code == 201
    return response.json()


def assert_application_error(
    response,
    *,
    status: int,
    code: str,
    message: str,
) -> None:
    assert response.status_code == status
    assert response.json() == {
        "error": {
            "status": status,
            "code": code,
            "message": message,
        }
    }


def assert_validation_error(response) -> None:
    body = response.json()
    assert response.status_code == 422
    assert body["error"]["status"] == 422
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["message"] == "Request validation failed."
    assert isinstance(body["error"]["details"], list)
    assert body["error"]["details"]


def validation_detail(response, field: str) -> dict:
    return next(
        detail
        for detail in response.json()["error"]["details"]
        if field in detail["loc"]
    )


def health_placeholder():
    pass
