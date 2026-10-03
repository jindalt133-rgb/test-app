# task-management-service

A minimal REST API for managing tasks. The service uses FastAPI, Pydantic, and SQLite.

## Requirements

- Python 3.11+
- pip

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

Start the application with:

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`.

The SQLite database path defaults to `tasks.db`. Set `TASK_DATABASE_PATH` to use a different database file:

```bash
TASK_DATABASE_PATH=custom-tasks.db uvicorn app.main:app --reload
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
  "title": "Buy groceries",
  "completed": false
}
```

`title` is required and must not be blank. `completed` defaults to `false`.

### Retrieve all tasks

```http
GET /tasks
```

### Retrieve a task by ID

```http
GET /tasks/{task_id}
```

A missing task returns HTTP 404:

```json
{
  "error": {
    "code": "task_not_found",
    "message": "Task not found"
  }
}
```

### Delete a task

```http
DELETE /tasks/{task_id}
```

A successful deletion returns HTTP 204 with no response body. A missing task returns the structured 404 response described above.

## Validation errors

Invalid request data returns HTTP 422 with this structure:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request",
    "details": [
      {
        "loc": ["body", "title"],
        "msg": "Value error, title must not be blank",
        "type": "value_error"
      }
    ]
  }
}
```

## Project structure

```text
app/
├── __init__.py
├── database.py
├── main.py
└── schemas.py
tests/
└── test_api.py
requirements.txt
README.md
```

- `app/main.py` defines the FastAPI application, routes, and error handlers.
- `app/database.py` contains SQLite initialization and task data access.
- `app/schemas.py` contains Pydantic request and response models.
- `tests/test_api.py` contains the pytest test suite.

## Testing

The test suite uses pytest, FastAPI `TestClient`, and an isolated SQLite database. Each test client uses a temporary SQLite database, so tests do not use the development database.

Run the test suite with:

```bash
pytest
```

The test suite covers:

- The health endpoint
- Task creation with default and explicit completion values
- Title whitespace handling
- Retrieval of all tasks, including empty results and ID ordering
- Retrieval of a task by ID
- Deletion of tasks and missing-task deletion errors
- Missing and blank titles
- Invalid title and completion values
- Invalid task identifiers
- Structured validation and not-found errors
- Database isolation between application instances
