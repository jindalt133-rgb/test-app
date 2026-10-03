from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import LeaveRequest


def create_leave_request(
    db: Session,
    leave_request: LeaveRequest,
) -> LeaveRequest:
    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)
    return leave_request


def get_all_leave_requests(db: Session) -> list[LeaveRequest]:
    return list(
        db.scalars(select(LeaveRequest).order_by(LeaveRequest.id)).all()
    )


def get_leave_request_by_id(
    db: Session,
    leave_request_id: int,
) -> LeaveRequest | None:
    return db.get(LeaveRequest, leave_request_id)


def get_leave_requests_for_employee(
    db: Session,
    employee_id: int,
) -> list[LeaveRequest]:
    statement = (
        select(LeaveRequest)
        .where(LeaveRequest.employee_id == employee_id)
        .order_by(LeaveRequest.id)
    )
    return list(db.scalars(statement).all())


def save_leave_request(
    db: Session,
    leave_request: LeaveRequest,
) -> LeaveRequest:
    db.add(leave_request)
    db.commit()
    db.refresh(leave_request)
    return leave_request


def delete_leave_request(db: Session, leave_request: LeaveRequest) -> None:
    db.delete(leave_request)
    db.commit()
