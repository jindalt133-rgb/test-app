from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path: Path):
    database_path = tmp_path / "tasks.db"
    application = create_app(str(database_path))

    with TestClient(application) as test_client:
        yield test_client


def test_health_returns_ok(client: TestClient):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task_defaults_completed_to_false(client: TestClient):
    response = client.post("/tasks", json={"title": "Buy groceries"})

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Buy groceries",
        "completed": False,
    }


def test_create_task_accepts_explicit_completed_value(client: TestClient):
    response = client.post(
        "/tasks",
        json={"title": "Submit report", "completed": True},
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Submit report",
        "completed": True,
    }


def test_create_task_strips_surrounding_title_whitespace(client: TestClient):
    response = client.post(
        "/tasks",
        json={"title": "  Review pull request  "},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Review pull request"


def test_list_tasks_returns_empty_list_initially(client: TestClient):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_returns_tasks_in_id_order(client: TestClient):
    first = client.post("/tasks", json={"title": "First task"})
    second = client.post(
        "/tasks",
        json={"title": "Second task", "completed": True},
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": first.json()["id"],
            "title": "First task",
            "completed": False,
        },
        {
            "id": second.json()["id"],
            "title": "Second task",
            "completed": True,
        },
    ]


def test_get_task_returns_task_by_id(client: TestClient):
    created = client.post("/tasks", json={"title": "Read documentation"})
    task_id = created.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json() == {
        "id": task_id,
        "title": "Read documentation",
        "completed": False,
    }


def test_get_missing_task_returns_structured_not_found_error(
    client: TestClient,
):
    response = client.get("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "task_not_found",
            "message": "Task not found",
        }
    }


def test_delete_task_returns_no_content_and_removes_task(
    client: TestClient,
):
    created = client.post("/tasks", json={"title": "Temporary task"})
    task_id = created.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/tasks/{task_id}").status_code == 404
    assert client.get("/tasks").json() == []


def test_delete_missing_task_returns_structured_not_found_error(
    client: TestClient,
):
    response = client.delete("/tasks/999")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "task_not_found",
            "message": "Task not found",
        }
    }


def test_missing_title_returns_structured_validation_error(
    client: TestClient,
):
    response = client.post("/tasks", json={})

    assert response.status_code == 422
    body = response.json()

    assert body["error"]["code"] == "validation_error"
    assert body["error"]["message"] == "Invalid request"
    assert body["error"]["details"] == [
        {
            "loc": ["body", "title"],
            "msg": "Field required",
            "type": "missing",
        }
    ]


def test_blank_title_returns_structured_validation_error(
    client: TestClient,
):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422
    body = response.json()

    assert body["error"]["code"] == "validation_error"
    assert body["error"]["message"] == "Invalid request"
    assert body["error"]["details"] == [
        {
            "loc": ["body", "title"],
            "msg": "Value error, title must not be blank",
            "type": "value_error",
        }
    ]


def test_invalid_title_type_returns_structured_validation_error(
    client: TestClient,
):
    response = client.post("/tasks", json={"title": 123})

    assert response.status_code == 422
    body = response.json()

    assert response.status_code == 422
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["message"] == "Invalid request"
    assert body["error"]["details"][0]["loc"] == ["body", "title"]
    assert body["error"]["details"][0]["type"] == "string_type"


def test_invalid_completed_value_returns_structured_validation_error(
    client: TestClient,
):
    response = client.post(
        "/tasks",
        json={"title": "Valid title", "completed": "not-a-boolean"},
    )

    assert response.status_code == 422
    body = response.json()

    assert response.status_code == 422
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["message"] == "Invalid request"
    assert body["error"]["details"][0]["loc"] == ["body", "completed"]
    assert body["error"]["details"][0]["type"] == "bool_parsing"


def test_invalid_task_identifier_returns_structured_validation_error(
    client: TestClient,
):
    response = client.get("/tasks/not-an-integer")

    assert response.status_code == 422
    body = response.json()

    assert response.status_code == 422
    assert body["error"]["code"] == "validation_error"
    assert body["error"]["message"] == "Invalid request"
    assert body["error"]["details"][0]["loc"] == ["path", "task_id"]
    assert body["error"]["details"][0]["type"] == "int_parsing"


def test_database_isolation_between_application_instances(tmp_path: Path):
    first_database = tmp_path / "first.db"
    second_database = tmp_path / "second.db"

    first_app = create_app(str(first_database))
    second_app = create_app(str(second_database))

    with TestClient(first_app) as first_client:
        created = first_client.post(
            "/tasks",
            json={"title": "Only in the first database"},
        )
        assert created.status_code == 201
        assert first_client.get("/tasks").json() == [created.json()]

    with TestClient(second_app) as second_client:
        assert second_client.get("/tasks").status_code == 200
        assert second_client.get("/tasks").json() == []
