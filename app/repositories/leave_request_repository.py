from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.leave_request import LeaveRequest


class LeaveRequestRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, leave_request: LeaveRequest) -> LeaveRequest:
        self.db.add(leave_request)
        self.db.commit()
        self.db.refresh(leave_request)
        return leave_request

    def get_all(self) -> list[LeaveRequest]:
        return list(self.db.scalars(select(LeaveRequest).order_by(LeaveRequest.id)).all())

    def get_by_id(self, leave_request_id: int) -> LeaveRequest | None:
        return self.db.get(LeaveRequest, leave_request_id)

    def get_by_employee_id(self, employee_id: int) -> list[LeaveRequest]:
        statement = (
            select(LeaveRequest)
            .where(LeaveRequest.employee_id == employee_id)
            .order_by(LeaveRequest.id)
        )
        return list(self.db.scalars(statement).all())

    def save(self, leave_request: LeaveRequest) -> LeaveRequest:
        self.db.add(leave_request)
        self.db.commit()
        self.db.refresh(leave_request)
        return leave_request

    def delete(self, leave_request: LeaveRequest) -> None:
        self.db.delete(leave_request)
        self.db.commit()
