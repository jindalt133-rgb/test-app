# task-management-service

## Overview

A minimal Task Management REST API built with Python 3.11+, FastAPI, Pydantic, and SQLite.

The API supports creating, listing, retrieving, and deleting tasks. Each task has an ID, a required non-blank title, and a completed status that defaults to `false`.

## Application structure

```text
app/
├── __init__.py
├── api.py
├── database.py
├── main.py
├── models.py
└── repository.py

tests/
└── test_tasks.py
pyproject.toml
```

The test file is planned at `tests/test_tasks.py` and is generated separately.

## Installation

Create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Install application and test dependencies:

```bash
pip install -e ".[test]"
```

## Configuration

The SQLite database path is configured with the `TASK_DB_PATH` environment variable.

If it is not set, the application uses `tasks.db` in the current working directory.

Example:

```bash
export TASK_DB_PATH=tasks.db
```

## Run command

Start the development server with:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API endpoints

### Health

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
  "title": "Write documentation",
  "completed": false
}
```

The `completed` field is optional and defaults to `false`.

Response: `201 Created`

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

Response: `200 OK`

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

Response: `200 OK`

```json
{
  "id": 1,
  "title": "Write documentation",
  "completed": false
}
```

If the task does not exist, the response is `404 Not Found`:

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

Response: `204 No Content`

If the task does not exist, the response is `404 Not Found` with the same structured error shown above.

## Validation errors

A blank title is invalid. Validation errors return `422 Unprocessable Entity`:

```json
{
  "code": "VALIDATION_ERROR",
  "detail": [
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
```

## Testing

Tests use `pytest` and FastAPI's `TestClient`, with `httpx` declared as a compatible client dependency.

Run the test suite with:

```bash
pytest
```

Tests use an isolated SQLite database created under pytest's `tmp_path` fixture. The application factory accepts an explicit database path so tests do not use the development database.

The planned test coverage includes:

- Health endpoint
- Task creation
- Retrieving all tasks
- Retrieving a task by ID
- Deleting a task
- Blank title validation
- Missing task handling

