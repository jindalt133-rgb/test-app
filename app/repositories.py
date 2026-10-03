from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Employee, LeaveRequest


class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, employee: Employee) -> Employee:
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def list(self) -> list[Employee]:
        return list(self.db.scalars(select(Employee).order_by(Employee.id)).all())

    def get(self, employee_id: int) -> Employee | None:
        return self.db.scalar(select(Employee).where(Employee.id == employee_id))

    def get_by_email(self, email: str) -> Employee | None:
        return self.db.scalar(select(Employee).where(Employee.email == email))


class LeaveRequestRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, leave_request: LeaveRequest) -> LeaveRequest:
        self.db.add(leave_request)
        self.db.commit()
        self.db.refresh(leave_request)
        return leave_request

    def list(self) -> list[LeaveRequest]:
        return list(self.db.scalars(select(LeaveRequest).order_by(LeaveRequest.id)).all())

    def list_by_employee(self, employee_id: int) -> list[LeaveRequest]:
        return list(self.db.scalars(select(LeaveRequest).where(LeaveRequest.employee_id == employee_id).order_by(LeaveRequest.id)).all())

    def get(self, leave_request_id: int) -> LeaveRequest | None:
        return self.db.scalar(select(LeaveRequest).where(LeaveRequest.id == leave_request_id))

    def save(self, leave_request: LeaveRequest) -> LeaveRequest:
        self.db.commit()
        self.db.refresh(leave_request)
        return leave_request

    def delete(self, leave_request: LeaveRequest) -> None:
        self.db.delete(leave_request)
        self.db.commit()
