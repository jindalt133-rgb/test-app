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

- `id`: integer identifier
- `title`: required, non-blank string
- `completed`: boolean that defaults to `false`

SQLite is used for persistence. The database path defaults to `tasks.db` and can be changed with the `TASK_DB_PATH` environment variable.

## Project structure

```text
task-management-service/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   └── schemas.py
├── tests/
│   └── test_tasks.py
├── .gitignore
├── pyproject.toml
└── README.md
```

The supplied test suite is present at `tests/test_tasks.py`. Tests use `pytest`, FastAPI's `TestClient`, and a separate SQLite database created in pytest's temporary directory for isolation.

## Installation

Python 3.11 or newer is required.

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install the dependencies:

```bash
pip install -e .
```

## Run the application

```bash
uvicorn app.main:app --reload
```

The API is available at:

```text
http://127.0.0.1:8000
```

To use a different SQLite database:

```bash
TASK_DB_PATH=./data/tasks.db uvicorn app.main:app --reload
```

On Windows PowerShell:

```powershell
$env:TASK_DB_PATH="./data/tasks.db"
uvicorn app.main:app --reload
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

A missing task returns `404 Not Found`:

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

A successful deletion returns `204 No Content`.

A missing task returns the same structured `404 Not Found` response:

```json
{
  "error": {
    "code": "TASK_NOT_FOUND",
    "message": "Task not found"
  }
}
```

## Validation errors

A blank title or otherwise invalid request returns `422 Unprocessable Entity`:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input",
    "details": []
  }
}
```

The `details` array contains the validation errors reported by Pydantic.

## Testing

The supplied test suite is `tests/test_tasks.py` and uses pytest.

Install the project dependencies, including test dependencies, with:

```bash
pip install -e ".[test]"
```

Run all tests:

```bash
pytest
```

Tests create and use an isolated SQLite database under pytest's `tmp_path` fixture. The application factory receives that temporary database path, so tests do not use the development database.

