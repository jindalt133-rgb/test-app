# Employee Leave Management Service

A REST API for managing employees and employee leave requests.

## Technology Stack

- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- Uvicorn
- pytest

## Project Structure

```text
employee-leave-management-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── errors.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── employee.py
│   │   └── leave_request.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── employee_repository.py
│   │   └── leave_request_repository.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── employees.py
│   │   ├── leave_requests.py
│   │   └── health.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── employee.py
│   │   └── leave_request.py
│   └── services/
│       ├── __init__.py
│       ├── employee_service.py
│       └── leave_request_service.py
├── tests/
│   ├── conftest.py
│   └── test_api.py
├── .env.example
├── requirements.txt
└── README.md
```

The `tests/conftest.py` and `tests/test_api.py` paths contain the pytest test suite.

## Installation

Create and activate a virtual environment:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

The application reads the `DATABASE_URL` environment variable.

Copy the example configuration:

```bash
cp .env.example .env
```

Default configuration:

```text
DATABASE_URL=sqlite:///./employee_leave.db
```

`DATABASE_URL` may point to another SQLite database. SQLite is the supported database implementation.

The application creates the database tables automatically when the application starts.

## Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

The API is available at:

```text
http://127.0.0.1:8000
```

Interactive API documentation:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Health

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Returns service health |

### Employees

| Method | Path | Description |
|---|---|---|
| POST | `/employees` | Create an employee |
| GET | `/employees` | Retrieve all employees |
| GET | `/employees/{employee_id}` | Retrieve an employee by ID |

Create employee request:

```json
{
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "department": "Engineering",
  "active": true
}
```

The `active` field defaults to `true`.

### Leave Requests

| Method | Path | Description |
|---|---|---|
| POST | `/leave-requests` | Submit a leave request |
| GET | `/leave-requests` | Retrieve all leave requests |
| GET | `/employees/{employee_id}/leave-requests` | Retrieve an employee's leave requests |
| POST | `/leave-requests/{leave_request_id}/approve` | Approve a pending leave request |
| POST | `/leave-requests/{leave_request_id}/reject` | Reject a pending leave request |
| DELETE | `/leave-requests/{leave_request_id}` | Delete a pending leave request |

Create leave request:

```json
{
  "employee_id": 1,
  "leave_type": "ANNUAL",
  "start_date": "2025-07-01",
  "end_date": "2025-07-05",
  "reason": "Annual vacation"
}
```

New leave requests always have the `PENDING` status.

## Employee Model

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | integer | response only | Employee identifier |
| `name` | string | yes | Employee name |
| `email` | string | yes | Unique employee email |
| `department` | string | yes | Employee department |
| `active` | boolean | no | Whether the employee may submit leave requests; defaults to `true` |

Names, emails, and departments cannot be blank or whitespace-only.

## Leave Request Model

| Field | Type | Required | Description |
|---|---|---:|---|
| `id` | integer | response only | Leave request identifier |
| `employee_id` | integer | yes | Existing employee identifier |
| `leave_type` | string | yes | `ANNUAL`, `SICK`, or `PERSONAL` |
| `start_date` | date | yes | First leave date |
| `end_date` | date | yes | Last leave date |
| `reason` | string | no | Optional explanation |
| `status` | string | response only | `PENDING`, `APPROVED`, or `REJECTED` |

## Business Rules

- Employee email addresses must be unique.
- Employee `name`, `email`, and `department` are required and cannot be blank.
- Leave requests can only be created for existing active employees.
- Supported leave types are `ANNUAL`, `SICK`, and `PERSONAL`.
- `start_date` cannot be after `end_date`.
- New leave requests default to `PENDING`.
- Only pending requests can be approved.
- Only pending requests can be rejected.
- Only pending requests can be deleted.
- Approval changes status to `APPROVED`.
- Rejection changes status to `REJECTED`.
- Missing employees and leave requests return structured 404 errors.

## Error Responses

Application errors use this structure:

```json
{
  "error": {
    "status": 404,
    "code": "EMPLOYEE_NOT_FOUND",
    "message": "Employee 99 was not found"
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

Validation errors use this structure:

```json
{
  "error": {
    "status": 422,
    "code": "VALIDATION_ERROR",
    "message": "value must not be blank",
    "details": [
      {
        "location": ["body", "name"],
        "message": "value must not be blank",
        "type": "value_error"
      }
    ]
  }
}
```

## Testing

The pytest suite uses an isolated in-memory SQLite database through dependency overrides and is located at:

```text
tests/conftest.py
tests/test_api.py
```

Run the test suite with:

```bash
pytest
```

Run with more detailed output:

```bash
pytest -v
```

The test strategy covers:

- Employee creation and retrieval
- Unique email validation
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
- Health endpoint behavior
- Isolated test data per test
- Isolated test data per test

## Assumptions

- SQLite is used as the persistence layer.
- Database tables are created automatically during application startup.
- The API uses synchronous SQLAlchemy sessions.
- No authentication or authorization requirements were specified.
- No pagination requirements were specified.
- Dates are represented using ISO 8601 `YYYY-MM-DD` strings.
