"""Repository layer."""
++ b/app/repositories/employee_repository.py
"""Pydantic API schemas."""
++ b/app/schemas/employee.py
"""Service layer."""
++ b/app/services/employee_service.py
"""Employee Leave Management Service application package."""

++ b/app/main.py
from enum import Enum
from sqlalchemy import Boolean, Date, Enum as SqlEnum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models import Employee


def create_employee(db: Session, employee: Employee) -> Employee:
    db.add(employee)
    db.commit()
    db.refresh(employee)
    return employee


def get_all_employees(db: Session) -> list[Employee]:
    return list(db.scalars(select(Employee).order_by(Employee.id)).all())


def get_employee_by_id(db: Session, employee_id: int) -> Employee | None:
    return db.get(Employee, employee_id)


def get_employee_by_email(db: Session, email: str) -> Employee | None:
    statement = select(Employee).where(Employee.email == email)
    return db.scalar(statement)
++ b/app/schemas/__init__.py
from pydantic import BaseModel, ConfigDict, field_validator


class EmployeeCreate(BaseModel):
    name: str
    email: str
    department: str
    active: bool = True

    @field_validator("name", "email", "department")
    @classmethod
    def reject_blank_values(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must not be blank")
        return value.strip()


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    department: str
    active: bool
++ b/app/schemas/leave_request.py

from pydantic import BaseModel, ConfigDict, field_validator, model_validator

from app.models import LeaveStatus, LeaveType


class LeaveRequestCreate(BaseModel):
    employee_id: int
    leave_type: LeaveType
    start_date: date
    end_date: date
    reason: str | None = None

    @field_validator("reason")
    @classmethod
    def normalize_reason(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        return normalized or None

    @model_validator(mode="after")
    def validate_date_range(self) -> "LeaveRequestCreate":
        if self.start_date > self.end_date:
            raise ValueError("start_date must not be after end_date")
        return self


class LeaveRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: int
    employee_id: int
    leave_type: LeaveType
    start_date: date
    end_date: date
    reason: str | None
    status: LeaveStatus
++ b/app/services/__init__.py
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import Employee
from app.repositories import employee_repository


def create_employee(db: Session, name: str, email: str, department: str, active: bool) -> Employee:
    existing = employee_repository.get_employee_by_email(db, email)
    if existing is not None:
        raise AppError(409, "EMPLOYEE_EMAIL_EXISTS", "An employee with this email already exists")
    employee = Employee(name=name, email=email, department=department, active=active)
    return employee_repository.create_employee(db, employee)


def get_all_employees(db: Session) -> list[Employee]:
    return employee_repository.get_all_employees(db)


def get_employee(db: Session, employee_id: int) -> Employee:
    employee = employee_repository.get_employee_by_id(db, employee_id)
    if employee is None:
        raise AppError(404, "EMPLOYEE_NOT_FOUND", "Employee was not found")
    return employee