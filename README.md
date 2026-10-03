# Employee Leave Management Service

A REST API for managing employees and employee leave requests.

## Application overview

`employee-leave-management-service` is a REST API for managing employees and employee leave requests.

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
