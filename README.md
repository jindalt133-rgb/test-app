# library-catalog-service

A REST API for managing a library's book catalog. Library administrators can create, view, update, delete, and search books through a FastAPI application backed by SQLite.

## Features

- Create books with title, author, ISBN, category, price, and quantity
- Retrieve all books, retrieve by ID, update, delete, and search by title or author
- Enforce unique ISBN values and validate required, non-blank, and non-negative fields
- Return consistent JSON error responses and provide a health-check endpoint
- Persist data with SQLite and provide automated API tests using Pytest and HTTPX

## Technology Stack

- Python 3.12, FastAPI, Uvicorn, SQLAlchemy 2.x, SQLite, Pydantic 2.x
- Pytest and HTTPX

## API Endpoints

- `GET /health` returns `{"status":"ok"}` with `200`.
- `POST /books` creates a book with `201`.
- `GET /books` retrieves all books; optional `q` searches title and author case-insensitively.
- `GET /books/{book_id}` retrieves a book or returns `404`.
- `PUT /books/{book_id}` replaces a book or returns `404`/`409`.
- `DELETE /books/{book_id}` returns `204` or `404`.

All errors use `{status, code, message, errors}`. Validation is `422 VALIDATION_ERROR`, missing books are `404 BOOK_NOT_FOUND`, and duplicate ISBN values are `409 DUPLICATE_ISBN`.

## Installation and Running

Requires Python 3.12+, pip, and a virtual environment.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The optional `DATABASE_URL` controls the SQLite database; the default is `sqlite:///./library_catalog.db`. Tables initialize automatically and the runtime database is excluded from source control. Interactive documentation is available at `/docs` and `/redoc`.

## Testing

```bash
pytest
```

The suite covers health, CRUD, title and author search, duplicate ISBN, missing and blank fields, numeric and length boundaries, nonexistent books, malformed IDs, and consistent error structures. Tests use an isolated in-memory SQLite database through the `database_session` override.

No credentials, authentication, authorization, external services, pagination, or sorting are required.
