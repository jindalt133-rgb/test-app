# task-management-service

## Overview

A minimal Task Management REST API built with Python 3.11+, FastAPI, Pydantic, and SQLite.

Tasks contain:

- `id`
- `title`
- `completed`

The SQLite database path is configured with the `TASK_DATABASE_PATH` environment variable. It defaults to `tasks.db`.

## Application structure

```text
app/
├── __init__.py
├── db.py
├── main.py
├── repository.py
└── schemas.py
```

Test structure:

```text
tests/
├── conftest.py
└── test_api.py
```

Tests use pytest and FastAPI's `TestClient`. The test fixture should set `TASK_DATABASE_PATH` to a temporary SQLite file so tests use an isolated database.

## Installation

Create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run command

Start the API with:

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

## API endpoints

### Health check

```http
GET /health
```

Response:

```json
{
  "status": "ok"
}
```

### Create a task

```http
POST /tasks
Content-Type: application/json
```

Request:

```json
{
  "title": "Write documentation"
}
```

`completed` defaults to `false`.

Response status: `201 Created`

```json
{
  "id": 1,
  "title": "Write documentation",
  "completed": false
}
```

### Retrieve all tasks

```http
GET /tasks
```

Response status: `200 OK`

```json
[
  {
    "id": 1,
    "title": "Write documentation",
    "completed": false
  }
]
```

### Retrieve a task by ID

```http
GET /tasks/{task_id}
```

Response status: `200 OK`

A missing task returns `404 Not Found`:

```json
{
  "detail": {
    "code": "TASK_NOT_FOUND",
    "message": "Task not found"
  }
}
```

### Delete a task

```http
DELETE /tasks/{task_id}
```

Response status: `204 No Content`

A missing task returns the same structured `404 Not Found` response.

## Validation errors

A task title is required and must not be blank. Invalid input returns `422 Unprocessable Entity`:

```json
{
  "detail": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request",
    "errors": [
      {
        "type": "value_error",
        "loc": ["body", "title"],
        "msg": "Value error, title must not be blank"
      }
    ]
  }
}
```

## Testing

The test suite uses pytest, FastAPI `TestClient`, and an isolated temporary SQLite database.

Run all tests with:

```bash
pytest
```

Run the API tests directly with:

```bash
pytest tests/test_api.py
```

The tests cover the health endpoint, task creation, retrieving all tasks, retrieving a task by ID, deleting a task, blank titles, and missing tasks.

