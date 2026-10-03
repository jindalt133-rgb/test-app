from datetime import date

from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import LeaveRequest, LeaveStatus, LeaveType
from app.repositories import employee_repository, leave_repository


def create_leave_request(
    db: Session,
    employee_id: int,
    leave_type: LeaveType,
    start_date: date,
    end_date: date,
    reason: str | None,
) -> LeaveRequest:
    employee = employee_repository.get_employee_by_id(db, employee_id)

    if employee is None:
        raise AppError(
            status=404,
            code="EMPLOYEE_NOT_FOUND",
            message="Employee was not found",
        )

    if not employee.active:
        raise AppError(
            status=409,
            code="EMPLOYEE_INACTIVE",
            message="Leave requests can only be created for active employees",
        )

    leave_request = LeaveRequest(
        employee_id=employee_id,
        leave_type=leave_type,
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        status=LeaveStatus.PENDING,
    )
    return leave_repository.create_leave_request(db, leave_request)


def get_all_leave_requests(db: Session) -> list[LeaveRequest]:
    return leave_repository.get_all_leave_requests(db)


def get_leave_requests_for_employee(
    db: Session,
    employee_id: int,
) -> list[LeaveRequest]:
    employee = employee_repository.get_employee_by_id(db, employee_id)
    if employee is None:
        raise AppError(
            status=404,
            code="EMPLOYEE_NOT_FOUND",
            message="Employee was not found",
        )

    return leave_repository.get_leave_requests_for_employee(db, employee_id)


def get_leave_request(db: Session, leave_request_id: int) -> LeaveRequest:
    leave_request = leave_repository.get_leave_request_by_id(
        db,
        leave_request_id,
    )
    if leave_request is None:
        raise AppError(
            status=404,
            code="LEAVE_REQUEST_NOT_FOUND",
            message="Leave request was not found",
        )
    return leave_request


def transition_leave_request(
    db: Session,
    leave_request_id: int,
    target_status: LeaveStatus,
) -> LeaveRequest:
    leave_request = get_leave_request(db, leave_request_id)

    if leave_request.status != LeaveStatus.PENDING:
        raise AppError(
            status=409,
            code="INVALID_STATUS_TRANSITION",
            message="Only pending leave requests can change status",
        )

    leave_request.status = target_status
    return leave_repository.save_leave_request(db, leave_request)


def delete_leave_request(db: Session, leave_request_id: int) -> None:
    leave_request = get_leave_request(db, leave_request_id)

    if leave_request.status != LeaveStatus.PENDING:
        raise AppError(
            status=409,
            code="INVALID_STATUS_TRANSITION",
            message="Only pending leave requests can be deleted",
        )

    leave_repository.delete_leave_request(db, leave_request)
