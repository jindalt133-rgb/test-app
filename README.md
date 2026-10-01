# Employee Leave Management Service

## Overview

`employee-leave-management-service` is a REST API for managing employees and employee leave requests.

The service supports employee creation and retrieval, unique email enforcement, active and inactive employees, leave request creation and retrieval, pending approval/rejection/deletion, structured errors, and health checks.

## Technology Stack

Python 3.11+, FastAPI, SQLAlchemy 2, Pydantic 2, SQLite, Uvicorn, pytest, and HTTPX.

## Configuration

The application reads `DATABASE_URL`, defaulting to `sqlite:///./employee_leave_management.db`. SQLite connection settings are configured automatically. The test suite creates a temporary SQLite database and sets `DATABASE_URL` before importing application modules; tests do not use FastAPI dependency overrides. Data is cleared between tests.

## Installation and running

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: `http://127.0.0.1:8000`; docs: `/docs`; ReDoc: `/redoc`.

## Endpoints

- `GET /health`
- `POST /employees`, `GET /employees`, `GET /employees/{employee_id}`
- `GET /employees/{employee_id}/leave-requests`
- `POST /leave-requests`, `GET /leave-requests`
- `POST /leave-requests/{leave_request_id}/approve`
- `POST /leave-requests/{leave_request_id}/reject`
- `DELETE /leave-requests/{leave_request_id}`

Employees require non-blank name, email, and department; email is unique. Leave requests require an existing active employee, support `ANNUAL`, `SICK`, and `PERSONAL`, default to `PENDING`, enforce valid dates, and permit only pending transitions. Errors use structured 404, 409, and 422 responses.

## Testing

Run `pytest` or `pytest -v`. The generated suite contains **34 test functions**: 1 health test, 11 employee tests, and 22 leave-request tests. Coverage includes positive, negative, validation, transition, missing-resource, inactive-employee, edge-case, and health scenarios.

## Architecture and structure

The layered application separates routes, services, repositories, Pydantic schemas, SQLAlchemy models, database configuration, and structured error handling. The `app/` directory contains the implementation and `tests/` contains the isolated pytest suite.

Deployment infrastructure, cloud provider, authentication, authorization, service owner, JIRA board, on-call rotation, and security scanning remain `Not Specified`.
