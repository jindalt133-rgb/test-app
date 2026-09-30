# Library Catalog Service

`library-catalog-service` is a REST API for managing a library book catalog.

It provides book CRUD operations, ISBN uniqueness enforcement, input validation, structured error responses, health monitoring, and SQLite persistence through SQLAlchemy.

## Technology Stack

- Python 3.11+
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- Pydantic 2.x
- SQLite
- pytest
- HTTPX

## Features

- Create a book
- Retrieve all books
- Retrieve a book by ID
- Update a book
- Delete a book
- Health-check endpoint
- Validation of required fields
- Rejection of blank text values
- Text maximum-length validation
- Publication-year validation
- Unique ISBN enforcement
- Structured validation, not-found, and conflict errors
- Layered API, service, repository, schema, model, and database architecture
- Automated API tests using an isolated in-memory SQLite database

## Project Structure

```text
library-catalog-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── books.py
│   │       └── health.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── initialization.py
│   │   └── session.py
│   ├── errors/
│   │   ├── __init__.py
│   │   └── exceptions.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── book.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── book_repository.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── book.py
│   │   └── error.py
│   └── services/
│       ├── __init__.py
│       └── book_service.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_books.py
│   └── test_health.py
├── pyproject.toml
└── README.md
```

The runtime SQLite database file is created separately and is not part of the source tree.

## Installation

### Prerequisites

- Python 3.11 or later
- `pip`
- A virtual environment tool

### Create a virtual environment

Linux/macOS:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.venv\\Scripts\\Activate.ps1
```

### Install the application and development dependencies

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Configuration

The application reads its database URL from `DATABASE_URL`.

Default:

```text
sqlite:///./library.db
```

Linux/macOS:

```bash
export DATABASE_URL="sqlite:///./library.db"
```

Windows PowerShell:

```powershell
$env:DATABASE_URL = "sqlite:///./library.db"
```

A different SQLite file can be configured as follows:

```bash
export DATABASE_URL="sqlite:///./data/library.db"
```

The application creates the parent directory for file-based SQLite databases when required.

## Running the Application

```bash
uvicorn app.main:app --reload
```

The service is available at:

```text
http://127.0.0.1:8000
```

Interactive documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`
- OpenAPI: `http://127.0.0.1:8000/openapi.json`

## API Endpoints

### Health check

```http
GET /health
```

Returns:

```json
{
  "status": "ok"
}
```

### Create a book

```http
POST /books
Content-Type: application/json
```

Returns `201 Created`.

### Retrieve all books

```http
GET /books
```

Returns `200 OK` and a book array.

### Retrieve a book

```http
GET /books/{book_id}
```

Returns:

- `200 OK` when found
- `404 Not Found` when the book does not exist

### Update a book

```http
PUT /books/{book_id}
Content-Type: application/json
```

`PUT` performs a full update.

Returns:

- `200 OK` when updated
- `404 Not Found` when the book does not exist
- `409 Conflict` when the ISBN belongs to another book

### Delete a book

```http
DELETE /books/{book_id}
```

Returns:

- `204 No Content` when deleted
- `404 Not Found` when the book does not exist

## Book Fields

| Field | Type | Rules |
|---|---|---|
| `id` | integer | Auto-generated identifier |
| `title` | string | Required, non-blank, maximum length 255 |
| `author` | string | Required, non-blank, maximum length 255 |
| `isbn` | string | Required, non-blank, maximum length 50, and unique |
| `publication_year` | integer | Must be between 1 and 9999 |
| `genre` | string | Required, non-blank, maximum length 255 |
| `available` | boolean | Defaults to `true` when omitted |

Text values are trimmed before persistence.

## Error Responses

Application errors use this envelope:

```json
{
  "error": {
    "code": "BOOK_NOT_FOUND",
    "message": "Book with ID 123 was not found"
  }
}
```

Validation errors include a `details` array:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "title",
        "message": "Field must not be blank"
      }
    ]
  }
}
```

Validation errors return `422 Unprocessable Entity`.

Missing books return `404 Not Found` with error code `BOOK_NOT_FOUND`.

Duplicate ISBN values return `409 Conflict` with error code `DUPLICATE_ISBN`.

## Testing

The test suite uses pytest, FastAPI `TestClient`, HTTPX, and an isolated in-memory SQLite database.

Run all tests:

```bash
pytest
```

Run tests with verbose output:

```bash
pytest -v
```

Tests override the actual `get_db` dependency and do not modify the runtime SQLite database.

Coverage includes:

- Health-check behavior
- Book creation, retrieval, update, and deletion
- Empty catalog behavior
- Missing-book errors
- Duplicate ISBN errors
- Required-field validation
- Blank and whitespace-only text values
- Text length boundaries
- Publication-year boundaries
- Invalid field types
- Invalid route identifiers
- Malformed JSON
- Default values and text trimming
- Update and delete operations against missing IDs

Authentication and authorization tests are not applicable because the approved application does not implement authentication or authorization.

## Database

SQLAlchemy manages the SQLite database.

Tables are created during application startup. No migration tool is required for the current scope.

The `isbn` column uses a database-level unique constraint in addition to service-level duplicate checking.

## Scope Assumptions

- The API is mounted at the root path.
- `PUT` is a full replacement operation.
- Book identifiers are auto-generated integers.
- ISBN uniqueness is case-sensitive.
- No ISBN format validation beyond non-blank input is required.
- Authentication, authorization, pagination, search, sorting, and migrations are outside the requested scope.
