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
.venv\Scripts\activate
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




