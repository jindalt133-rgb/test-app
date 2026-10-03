import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    database_path = tmp_path / "tasks.db"
    monkeypatch.setenv("TASK_DATABASE_PATH", str(database_path))

    from app.main import app

    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def create_task(client):
    def _create_task(
        title: str = "Test task",
        completed: bool = False,
    ) -> dict:
        response = client.post(
            "/tasks",
            json={
                "title": title,
                "completed": completed,
            },
        )
        assert response.status_code == 201
        return response.json()

    return _create_task
