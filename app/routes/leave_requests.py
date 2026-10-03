from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import LeaveStatus
from app.schemas.leave_request import (
    LeaveRequestCreate,
    LeaveRequestResponse,
)
from app.services import leave_service

router = APIRouter(prefix="/leave-requests", tags=["leave requests"])


@router.post(
    "",
    response_model=LeaveRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_leave_request(
    payload: LeaveRequestCreate,
    db: Session = Depends(get_db),
) -> LeaveRequestResponse:
    return leave_service.create_leave_request(
        db=db,
        employee_id=payload.employee_id,
        leave_type=payload.leave_type,
        start_date=payload.start_date,
        end_date=payload.end_date,
        reason=payload.reason,
    )


@router.get("", response_model=list[LeaveRequestResponse])
def get_leave_requests(
    db: Session = Depends(get_db),
) -> list[LeaveRequestResponse]:
    return leave_service.get_all_leave_requests(db)


@router.post(
    "/{leave_request_id}/approve",
    response_model=LeaveRequestResponse,
)
def approve_leave_request(
    leave_request_id: int,
    db: Session = Depends(get_db),
) -> LeaveRequestResponse:
    return leave_service.transition_leave_request(
        db,
        leave_request_id,
        LeaveStatus.APPROVED,
    )


@router.post(
    "/{leave_request_id}/reject",
    response_model=LeaveRequestResponse,
)
def reject_leave_request(
    leave_request_id: int,
    db: Session = Depends(get_db),
) -> LeaveRequestResponse:
    return leave_service.transition_leave_request(
        db,
        leave_request_id,
        LeaveStatus.REJECTED,
    )


@router.delete(
    "/{leave_request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_leave_request(
    leave_request_id: int,
    db: Session = Depends(get_db),
) -> Response:
    leave_service.delete_leave_request(db, leave_request_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
