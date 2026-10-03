import json

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path):
    database_path = tmp_path / "tasks.sqlite"
    application = create_app(database_path)

    with TestClient(application) as test_client:
        yield test_client


def assert_validation_response(response, *, expected_location):
    assert response.status_code == 422

    body = response.json()
    assert body["code"] == "VALIDATION_ERROR"
    assert isinstance(body["detail"], list)
    assert body["detail"]

    # The complete response must be JSON-safe, including nested error context.
    json.dumps(body)

    matching_errors = [
        error
        for error in body["detail"]
        if error.get("loc") == expected_location
    ]
    assert matching_errors

    error = matching_errors[0]
    assert isinstance(error["type"], str)
    assert isinstance(error["msg"], str)

    context = error.get("ctx")
    if context is not None:
        assert isinstance(context, dict)
        for value in context.values():
            assert not isinstance(value, BaseException)


def test_health_endpoint_returns_ok(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task_returns_created_task_with_default_completed_status(client):
    response = client.post("/tasks", json={"title": "  Write documentation  "})

    assert response.status_code == 201
    task = response.json()
    assert task["id"] > 0
    assert task["title"] == "Write documentation"
    assert task["completed"] is False


def test_create_task_accepts_explicit_completed_status(client):
    response = client.post(
        "/tasks",
        json={"title": "Finish implementation", "completed": True},
    )

    assert response.status_code == 201
    task = response.json()
    assert task["title"] == "Finish implementation"
    assert task["completed"] is True


def test_get_tasks_returns_tasks_in_id_order(client):
    first = client.post("/tasks", json={"title": "First task"}).json()
    second = client.post("/tasks", json={"title": "Second task"}).json()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {"id": first["id"], "title": "First task", "completed": False},
        {"id": second["id"], "title": "Second task", "completed": False},
    ]


def test_get_tasks_returns_empty_list_when_no_tasks_exist(client):
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_get_task_returns_existing_task(client):
    created = client.post(
        "/tasks",
        json={"title": "Retrieve this task", "completed": True},
    ).json()

    response = client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_get_task_returns_structured_not_found_error(client):
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": {"code": "TASK_NOT_FOUND", "message": "Task not found"}}


def test_delete_task_removes_existing_task(client):
    created = client.post("/tasks", json={"title": "Delete this task"}).json()

    response = client.delete(f"/tasks/{created['id']}")

    assert response.status_code == 204
    assert response.content == b""
    assert client.get(f"/tasks/{created['id']}").status_code == 404
    assert client.get("/tasks").json() == []


def test_delete_task_returns_structured_not_found_error(client):
    response = client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {"detail": {"code": "TASK_NOT_FOUND", "message": "Task not found"}}


@pytest.mark.parametrize("title", ["", "   ", "\t\n"])
def test_create_task_rejects_blank_title_with_json_safe_error(title, client):
    response = client.post("/tasks", json={"title": title})

    assert_validation_response(response, expected_location=["body", "title"])

    error = next(error for error in response.json()["detail"] if error.get("loc") == ["body", "title"])
    assert error["msg"] == "Value error, title must not be blank"
    assert error["input"] == title


def test_create_task_rejects_missing_title(client):
    response = client.post("/tasks", json={"completed": False})
    assert_validation_response(response, expected_location=["body", "title"])


def test_create_task_rejects_null_title(client):
    response = client.post("/tasks", json={"title": None})
    assert_validation_response(response, expected_location=["body", "title"])


@pytest.mark.parametrize(
    "payload",
    [[], "not an object", {"title": ["not", "a", "string"]}, {"title": "Valid title", "completed": []}],
)
def test_create_task_rejects_malformed_payloads(payload, client):
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert body["code"] == "VALIDATION_ERROR"
    assert isinstance(body["detail"], list)
    json.dumps(body)


def test_create_task_rejects_invalid_completed_value(client):
    response = client.post("/tasks", json={"title": "Valid title", "completed": []})
    assert_validation_response(response, expected_location=["body", "completed"])
