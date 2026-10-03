# task-management-service

A minimal Task Management REST API built with Python 3.11+, FastAPI, Pydantic, and SQLite.

## Overview

The service supports:

- Creating tasks
- Retrieving all tasks
- Retrieving a task by ID
- Deleting tasks
- Checking service health

Each task contains:

- `id`: Integer identifier
- `title`: Required, non-blank string
- `completed`: Boolean that defaults to `false`

The application stores tasks in SQLite. The database path defaults to `tasks.db` and can be changed with the `TASK_DATABASE_PATH` environment variable.

## Application structure

```text
app/
  __init__.py
  database.py
  main.py
  schemas.py
pyproject.toml
README.md
tests/
  test_api.py
```

The test suite uses pytest and FastAPI's `TestClient`. Tests use an isolated temporary SQLite database by creating the application with a temporary database path.

## Installation

Python 3.11 or newer is required.

Create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install application and test dependencies:

```bash
pip install -e ".[test]"
```

## Run the application

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

To use a different SQLite database file:

```bash
TASK_DATABASE_PATH=/path/to/tasks.db uvicorn app.main:app --reload
```

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

`completed` is optional and defaults to `false`.

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

Response:

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

A missing task returns status `404`:

```json
{
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task not found"
  }
}
```

### Delete a task

```http
DELETE /tasks/{task_id}
```

A successful deletion returns status `204 No Content`.

A missing task returns the same structured `404` response as retrieving a missing task.

## Validation errors

A missing or blank `title` returns status `422`:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request",
    "details": [
      {
        "type": "value_error",
        "loc": [
          "body",
          "title"
        ],
        "msg": "Value error, title must not be blank",
        "input": "   "
      }
    ]
  }
}
```

## Testing

The test suite is provided in `tests/test_api.py`. It uses pytest and FastAPI's `TestClient`.

Run all tests:

```bash
pytest
```

Run the API test module directly:

```bash
pytest tests/test_api.py
```

Tests use a separate temporary SQLite database for each test or test application instance, so they do not use the development database.

## Testing

The test suite is provided in `tests/test_api.py`. It uses pytest and FastAPI's `TestClient`.

Run all tests:

```bash
pytest
```

Run the API test module directly:

```bash
pytest tests/test_api.py
```

Tests use a separate temporary SQLite database for each test or test application instance, so they do not use the development database.

