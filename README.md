# library-catalog-service

A REST API for managing a library book catalog. Library administrators can create, retrieve, update, delete, and search books.

## Technology Stack

- Python 3.12
- FastAPI
- Uvicorn
- SQLAlchemy 2.x
- SQLite
- Pydantic 2.x
- Pytest
- HTTPX

## Features

- Create, retrieve, update, and delete books
- Search books by title or author
- Enforce unique ISBN values
- Validate required and numeric fields
- Return consistent JSON error responses
- Persist data in SQLite
- Provide a health endpoint
- Automated API tests with isolated temporary SQLite data

## Project Structure

```text
library-catalog-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── books.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── errors.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── books.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── books.py
│   └── services/
│       ├── __init__.py
│       └── books.py
├── tests/
│   ├── conftest.py
│   └── test_books.py
├── .env.example
├── pyproject.toml
└── README.md
```

## Installation

Python 3.12 and `pip` are required.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

On Windows PowerShell:

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Configuration

The application reads the optional `DATABASE_URL` environment variable. The default is `sqlite:///./library.db`. The supported placeholder is provided in `.env.example`; no credentials, API keys, or external services are required.

## Database

- Database engine: SQLite
- Default database file: `library.db`
- SQLAlchemy 2.x manages persistence.
- Tables are created automatically during application startup.
- ISBN uniqueness is enforced by the service layer and database constraint.
- Tests use a separate temporary SQLite database.

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Interactive documentation is available at `/docs` and `/redoc`.

## API Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET | `/health` | Return application health |
| POST | `/books` | Create a book |
| GET | `/books` | Retrieve all books |
| GET | `/books?q=<query>` | Search by title or author |
| GET | `/books/{book_id}` | Retrieve a book |
| PUT | `/books/{book_id}` | Replace a book |
| DELETE | `/books/{book_id}` | Delete a book |

Successful status codes include `200`, `201`, and `204`. Error status codes include `404`, `409`, `422`, and `500`.

## Validation Rules

- `title`, `author`, `isbn`, and `category` are required and cannot be blank.
- Surrounding whitespace is removed from required text fields.
- Maximum lengths are 255 for title and author, 50 for ISBN, and 100 for category.
- ISBN values must be unique.
- `price` and `quantity` must be greater than or equal to `0`.

## Error Responses

All application errors use `{status, code, message, errors}`. Duplicate ISBN errors use `409 DUPLICATE_ISBN`; validation errors use `422 VALIDATION_ERROR`; not-found errors use `404 BOOK_NOT_FOUND`.

## Testing

Tests are located in `tests/conftest.py` and `tests/test_books.py`. The fixture configures a temporary SQLite database before importing the application database module and recreates the schema for each test.

```bash
pytest
pytest --cov=app --cov-report=term-missing
```

The suite covers health, CRUD, title and author search, duplicate ISBN creation and update, missing and blank fields, negative price and quantity, zero boundaries, string-length boundaries, malformed JSON, invalid identifiers, nonexistent books, and consistent error responses.

No authentication, authorization, pagination, sorting, or migration framework was requested.
