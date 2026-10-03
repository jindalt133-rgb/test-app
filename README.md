# Employee Leave Management Service

A REST API for managing employees and employee leave requests.

## Application overview

The Employee Leave Management Service provides endpoints to:

- Create and retrieve employees.
- Submit leave requests for active employees.
- Retrieve all leave requests or requests for one employee.
- Approve and reject pending requests.
- Delete pending requests.
- Check application health.

The service uses a layered architecture with FastAPI routes, service-layer business rules, repository-layer persistence, Pydantic schemas, SQLAlchemy models, and centralized error handling.

## Technology stack

- Python 3.11+
- FastAPI 0.115.6
- SQLAlchemy 2.0.36
- Pydantic 2.10.3
- SQLite
- Uvicorn
- pytest 8.3.4
- HTTPX 0.28.1

## Project structure

```text
employee-leave-management-service/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── database.py
│   ├── errors.py
│   ├── main.py
│   ├── models.py
│   ├── repositories.py
│   ├── schemas.py
│   └── services.py
├── tests/
│   └── test_api.py
├── .env.example
├── requirements.txt
└── README.md
```

## Installation

Create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
py -3.11 -m venv .venv
.venv\\Scripts\\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The application reads the database connection from the `DATABASE_URL` environment variable.

A default SQLite database is used when `DATABASE_URL` is not set:

```text
sqlite:///./employee_leave.db
```

To configure a different database:

```bash
export DATABASE_URL="sqlite:///./employee_leave.db"
```

The included `.env.example` documents the supported configuration.

## Database

SQLite is used as the persistence layer. Tables are created automatically when the application starts.

No migration tool is required for the current implementation.

## Running the application

Start the development server with:

```bash
uvicorn app.main:app --reload
```

The API is then available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation is available at:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API endpoints

### Health

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Returns service health |

### Employees

| Method | Endpoint | Description |
|---|---|---|
| POST | `/employees` | Create an employee |
| GET | `/employees` | Retrieve all employees |
| GET | `/employees/{employee_id}` | Retrieve one employee |

Example employee:

```json
{
  "name": "Jane Smith",
  "email": "jane.smith@example.com",
  "department": "Engineering",
  "active": true
}
```

`active` defaults to `true`.

### Leave requests

| Method | Endpoint | Description |
|---|---|---|
| POST | `/leave-requests` | Submit a leave request |
| GET | `/leave-requests` | Retrieve all leave requests |
| GET | `/employees/{employee_id}/leave-requests` | Retrieve requests for an employee |
| PATCH | `/leave-requests/{leave_request_id}/approve` | Approve a pending request |
| PATCH | `/leave-requests/{leave_request_id}/reject` | Reject a pending request |
| DELETE | `/leave-requests/{leave_request_id}` | Delete a pending request |

Example leave request:

```json
{
  "employee_id": 1,
  "leave_type": "ANNUAL",
  "start_date": "2025-06-02",
  "end_date": "2025-06-06",
  "reason": "Annual vacation"
}
```

New leave requests always have the `PENDING` status.

## Employee model

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique employee identifier |
| `name` | string | Required, non-blank employee name |
| `email` | string | Required, valid and unique email address |
| `department` | string | Required, non-blank department |
| `active` | boolean | Whether the employee may submit leave requests |

## Leave request model

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique leave request identifier |
| `employee_id` | integer | Associated employee identifier |
| `leave_type` | string | `ANNUAL`, `SICK`, or `PERSONAL` |
| `start_date` | date | First day of leave |
| `end_date` | date | Last day of leave |
| `reason` | string or null | Optional explanation |
| `status` | string | `PENDING`, `APPROVED`, or `REJECTED` |

## Business rules

- Employee email addresses must be unique.
- Employee `name`, `email`, and `department` must not be blank.
- A leave request can only be created for an existing active employee.
- Supported leave types are:
  - `ANNUAL`
  - `SICK`
  - `PERSONAL`
- `start_date` cannot be after `end_date`.
- New leave requests default to `PENDING`.
- Only pending requests can be approved.
- Only pending requests can be rejected.
- Approval changes the status to `APPROVED`.
- Rejection changes the status to `REJECTED`.
- Only pending requests can be deleted.

## Error responses

Application errors use this structure:

```json
{
  "error": {
    "status": 404,
    "code": "EMPLOYEE_NOT_FOUND",
    "message": "Employee 1 was not found."
  }
}
```

Validation errors use this structure:

```json
{
  "error": {
    "status": 422,
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed.",
    "details": [
      {
        "loc": ["body", "name"],
        "msg": "Value must not be blank.",
        "type": "value_error"
      }
    ]
  }
}
```

Common error codes include:

- `EMPLOYEE_NOT_FOUND`
- `LEAVE_REQUEST_NOT_FOUND`
- `DUPLICATE_EMPLOYEE_EMAIL`
- `INACTIVE_EMPLOYEE`
- `INVALID_LEAVE_STATUS`
- `VALIDATION_ERROR`

## Testing

Run the generated test suite with:

```bash
pytest
```

Run with verbose output:

```bash
pytest -v
```

The test suite is located at `tests/test_api.py`.

Tests use an isolated in-memory SQLite database, preventing test data from affecting the development database. The suite covers:

- Employee creation and retrieval
- Unique employee email validation
- Leave request creation and retrieval
- Employee-specific leave retrieval
- Approval, rejection, and deletion
- Inactive employee behavior
- Missing employees and leave requests
- Invalid leave types
- Invalid date ranges
- Invalid status transitions
- Blank required fields
- Positive, negative, validation, and edge-case scenarios
- Health checks

## Test strategy

API tests exercise the FastAPI application through HTTPX and pytest. Each test uses an isolated in-memory SQLite database, and database state is reset between tests. This verifies routing, validation, service rules, repository behavior, persistence, and structured error responses together.



The service supports:

- Creating and retrieving employees
- Unique employee email enforcement
- Active and inactive employees
- Creating leave requests for active employees
- Retrieving all leave requests
- Retrieving leave requests for a specific employee
- Approving and rejecting pending leave requests
- Deleting pending leave requests
- Structured validation, not-found, conflict, and transition errors
- Health checks

The application uses Python 3.11+, FastAPI, SQLAlchemy, Pydantic, SQLite, Uvicorn, pytest, and HTTPX.

## Technology Stack

- Python 3.11+
- FastAPI
- SQLAlchemy 2
- Pydantic 2
- SQLite
- Uvicorn
- pytest
- HTTPX

## Architecture

```text
HTTP Request
    |
    v
FastAPI Routes
    |
    v
Services
    |
    v
Repositories
    |
    v
SQLAlchemy Models
    |
    v
SQLite
```

- Routes handle HTTP concerns and dependency injection.
- Services enforce business rules.
- Repositories encapsulate database access.
- Pydantic schemas validate requests and responses.
- SQLAlchemy models define the database schema.
- Centralized exception handlers return structured errors.

## Project Structure

```text
employee-leave-management-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── employees.py
│   │       ├── health.py
│   │       └── leave_requests.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   └── errors.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── configuration.py
│   │   └── session.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── employee.py
│   │   └── leave_request.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── employee_repository.py
│   │   └── leave_request_repository.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── employee.py
│   │   └── leave_request.py
│   └── services/
│       ├── __init__.py
│       ├── employee_service.py
│       └── leave_request_service.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_employees.py
│   ├── test_health.py
│   └── test_leave_requests.py
├── requirements.txt
└── README.md
```

## Configuration

The application reads its database URL from `DATABASE_URL`.

Default:

```text
sqlite:///./employee_leave_management.db
```

Linux/macOS:

```bash
export DATABASE_URL="sqlite:///./employee_leave_management.db"
```

Windows PowerShell:

```powershell
$env:DATABASE_URL = "sqlite:///./employee_leave_management.db"
```

SQLite-specific connection settings are configured automatically.

No credentials or external services are required.

## Installation

Prerequisites:

- Python 3.11 or later
- pip
- A writable local filesystem

Create a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
py -3.11 -m venv .venv
.venv\\Scripts\\Activate.ps1
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Application

```bash
uvicorn app.main:app --reload
```

The API is available at:

```text
http://127.0.0.1:8000
```

OpenAPI documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc documentation:

```text
http://127.0.0.1:8000/redoc
```

Database tables are created automatically during application startup.

## API Endpoints

### Health

#### `GET /health`

Response:

```json
{
  "status": "ok"
}
```

### Employees

#### `POST /employees`

Creates an employee.

```json
{
  "name": "Alex Morgan",
  "email": "alex.morgan@example.com",
  "department": "Engineering",
  "active": true
}
```

The `active` field defaults to `true`.

#### `GET /employees`

Returns all employees.

#### `GET /employees/{employee_id}`

Returns one employee.

#### `GET /employees/{employee_id}/leave-requests`

Returns leave requests for an employee.

Missing employees return a structured HTTP 404 response.

### Leave Requests

#### `POST /leave-requests`

Creates a leave request for an existing active employee.

```json
{
  "employee_id": 1,
  "leave_type": "ANNUAL",
  "start_date": "2025-06-10",
  "end_date": "2025-06-14",
  "reason": "Planned vacation"
}
```

Supported leave types:

- `ANNUAL`
- `SICK`
- `PERSONAL`

New requests always have status `PENDING`.

#### `GET /leave-requests`

Returns all leave requests.

#### `POST /leave-requests/{leave_request_id}/approve`

Approves a pending leave request.

#### `POST /leave-requests/{leave_request_id}/reject`

Rejects a pending leave request.

#### `DELETE /leave-requests/{leave_request_id}`

Deletes a pending leave request.

## Employee Model

| Field | Type | Rules |
|---|---|---|
| `id` | integer | Generated identifier |
| `name` | string | Required and non-blank |
| `email` | string | Required, non-blank, and unique |
| `department` | string | Required and non-blank |
| `active` | boolean | Defaults to `true` |

## Leave Request Model

| Field | Type | Rules |
|---|---|---|
| `id` | integer | Generated identifier |
| `employee_id` | integer | References an employee |
| `leave_type` | enum | `ANNUAL`, `SICK`, or `PERSONAL` |
| `start_date` | date | Cannot be after `end_date` |
| `end_date` | date | Cannot be before `start_date` |
| `reason` | string or null | Optional |
| `status` | enum | `PENDING`, `APPROVED`, or `REJECTED` |

## Business Rules

1. Employee email addresses must be unique.
2. Employee name, email, and department are required and cannot be blank.
3. Leave requests require an existing active employee.
4. Only `ANNUAL`, `SICK`, and `PERSONAL` leave types are accepted.
5. `start_date` must not be after `end_date`.
6. New leave requests default to `PENDING`.
7. Only pending leave requests can be approved.
8. Only pending leave requests can be rejected.
9. Approval changes the status to `APPROVED`.
10. Rejection changes the status to `REJECTED`.
11. Only pending leave requests can be deleted.
12. Missing employees and leave requests return structured 404 errors.
13. Invalid request data returns structured validation errors.
14. Duplicate employee email returns a structured conflict error.

## Error Responses

Application errors use this structure:

```json
{
  "error": {
    "code": "EMPLOYEE_NOT_FOUND",
    "message": "Employee with ID 99 was not found",
    "details": {
      "employee_id": 99
    }
  }
}
```

Typical status codes:

| Status | Usage |
|---|---|
| `404` | Missing employee or leave request |
| `409` | Duplicate email, inactive employee, or invalid status transition |
| `422` | Request validation failure |
| `500` | Unexpected server error |

Validation errors use the same structure:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": {
      "name": "Value error, must not be blank"
    }
  }
}
```

## Database Behavior

The application uses SQLite through SQLAlchemy.

The production or development database is selected through `DATABASE_URL`.

The test suite creates a temporary SQLite database and sets `DATABASE_URL` before importing application modules. This ensures that the application engine points to the isolated test database. Tests do not use FastAPI dependency overrides.

Test data is cleared between tests, and the temporary database is removed after the test session.

## Testing

Install dependencies from `requirements.txt`, then run:

```bash
pytest
```

Verbose execution:

```bash
pytest -v
```

The generated suite contains **34 test functions**:

- 1 health test
- 11 employee tests
- 22 leave-request tests

The test suite uses:

- pytest
- FastAPI `TestClient`
- HTTPX
- A temporary isolated SQLite database
- Database URL configuration before application import

## Test Strategy

The tests cover:

### Employee scenarios

- Employee creation
- Default active status
- Explicit inactive status
- Employee listing
- Employee retrieval by ID
- Duplicate email rejection
- Blank name rejection
- Blank email rejection
- Blank department rejection
- Missing employee handling
- Missing and malformed input
- Invalid path parameters

### Leave request scenarios

- Leave request creation
- Default `PENDING` status
- All supported leave types
- Optional reason
- Same-day leave ranges
- Global leave retrieval
- Employee-specific leave retrieval
- Missing employee handling
- Inactive employee handling
- Invalid leave types
- Invalid date ranges
- Missing fields
- Approval
- Rejection
- Deletion
- Invalid status transitions
- Missing leave requests
- Invalid path parameters

### General scenarios

- Health endpoint
- Structured 404 errors
- Structured 409 errors
- Structured 422 errors
- Test database isolation
- Positive, negative, validation, and edge cases

## Unsupported Application Profile

The following were not specified and remain `Not Specified`:

- Deployment infrastructure
- Cloud provider
- Authentication or authorization
- Service owner
- JIRA board
- On-call rotation
- Security scanning process
