from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


@pytest.fixture
def client(tmp_path: Path):
    database_path = tmp_path / "tasks.db"
    with TestClient(create_app(database_path)) as test_client:
        yield test_client


def assert_validation_error(response) -> None:
    assert response.status_code == 422

    body = response.json()
    assert body["error"]["code"] == "VALIDATION_ERROR"
    assert body["error"]["message"] == "Invalid input"
    assert isinstance(body["error"]["details"], list)
    assert body["error"]["details"]


def assert_task_shape(task: dict, *, title: str, completed: bool) -> None:
    assert set(task) == {"id", "title", "completed"}
    assert isinstance(task["id"], int)
    assert task["id"] > 0
    assert task["title"] == title
    assert task["completed"] is completed


def test_health_returns_ok(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_get_tasks_returns_empty_list_for_new_database(
    client: TestClient,
) -> None:
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_create_task_defaults_completed_to_false(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": "Write documentation"})

    assert response.status_code == 201
    task = response.json()
    assert_task_shape(
        task,
        title="Write documentation",
        completed=False,
    )


def test_create_task_accepts_explicit_completed_value(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Review pull request", "completed": True},
    )

    assert response.status_code == 201
    task = response.json()
    assert_task_shape(
        task,
        title="Review pull request",
        completed=True,
    )


def test_create_task_preserves_non_blank_title_value(
    client: TestClient,
) -> None:
    title = "  Keep surrounding whitespace  "

    response = client.post("/tasks", json={"title": title})

    assert response.status_code == 201
    assert response.json()["title"] == title


def test_created_task_can_be_retrieved_by_id(client: TestClient) -> None:
    created = client.post("/tasks", json={"title": "Retrieve this task"})
    task_id = created.json()["id"]

    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json() == created.json()


def test_get_tasks_returns_tasks_in_id_order(client: TestClient) -> None:
    first = client.post("/tasks", json={"title": "First task"}).json()
    second = client.post(
        "/tasks",
        json={"title": "Second task", "completed": True},
    ).json()

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [first, second]


def test_task_data_persists_across_application_instances(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "persistent.db"

    with TestClient(create_app(database_path)) as first_client:
        created = first_client.post(
            "/tasks",
            json={"title": "Persist this task"},
        ).json()

    with TestClient(create_app(database_path)) as second_client:
        response = second_client.get(f"/tasks/{created['id']}")

    assert response.status_code == 200
    assert response.json() == created


def test_create_task_rejects_missing_title(client: TestClient) -> None:
    response = client.post("/tasks", json={})

    assert_validation_error(response)


@pytest.mark.parametrize(
    "title",
    [
        "",
        " ",
        "\t",
        "\n",
    ],
)
def test_create_task_rejects_blank_title(
    client: TestClient,
    title: str,
) -> None:
    response = client.post("/tasks", json={"title": title})

    assert_validation_error(response)


def test_create_task_rejects_non_string_title(client: TestClient) -> None:
    response = client.post("/tasks", json={"title": 123})

    assert_validation_error(response)


def test_create_task_rejects_invalid_completed_value(
    client: TestClient,
) -> None:
    response = client.post(
        "/tasks",
        json={"title": "Invalid completion value", "completed": "sometimes"},
    )

    assert_validation_error(response)


def test_create_task_rejects_malformed_json(client: TestClient) -> None:
    response = client.post(
        "/tasks",
        content='{"title": "Incomplete"',
        headers={"content-type": "application/json"},
    )

    assert_validation_error(response)


def test_get_missing_task_returns_structured_not_found_error(
    client: TestClient,
) -> None:
    response = client.get("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "TASK_NOT_FOUND",
            "message": "Task not found",
        }
    }


def test_get_task_rejects_non_integer_identifier(
    client: TestClient,
) -> None:
    response = client.get("/tasks/not-an-integer")

    assert_validation_error(response)


def test_delete_task_returns_no_content_and_removes_task(
    client: TestClient,
) -> None:
    created = client.post("/tasks", json={"title": "Delete this task"}).json()

    delete_response = client.delete(f"/tasks/{created['id']}")

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    get_response = client.get(f"/tasks/{created['id']}")
    assert get_response.status_code == 404
    assert get_response.json() == {
        "error": {
            "code": "TASK_NOT_FOUND",
            "message": "Task not found",
        }
    }


def test_delete_missing_task_returns_structured_not_found_error(
    client: TestClient,
) -> None:
    response = client.delete("/tasks/999999")

    assert response.status_code == 404
    assert response.json() == {
        "error": {
            "code": "TASK_NOT_FOUND",
            "message": "Task not found",
        }
    }


def test_delete_task_rejects_non_integer_identifier(
    client: TestClient,
) -> None:
    response = client.delete("/tasks/not-an-integer")

    assert_validation_error(response)
