from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.leave_request_repository import LeaveRequestRepository
from app.schemas.leave_request import LeaveRequestCreate, LeaveRequestResponse
from app.services.leave_request_service import LeaveRequestService

router = APIRouter(tags=["leave requests"])


def get_leave_request_service(db: Session = Depends(get_db)) -> LeaveRequestService:
    return LeaveRequestService(
        repository=LeaveRequestRepository(db),
        employee_repository=EmployeeRepository(db),
    )


@router.post(
    "/leave-requests",
    response_model=LeaveRequestResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_leave_request(
    data: LeaveRequestCreate,
    service: LeaveRequestService = Depends(get_leave_request_service),
) -> LeaveRequestResponse:
    return service.create(data)


@router.get("/leave-requests", response_model=list[LeaveRequestResponse])
def get_leave_requests(
    service: LeaveRequestService = Depends(get_leave_request_service),
) -> list[LeaveRequestResponse]:
    return service.get_all()


@router.get(
    "/employees/{employee_id}/leave-requests",
    response_model=list[LeaveRequestResponse],
)
def get_employee_leave_requests(
    employee_id: int,
    service: LeaveRequestService = Depends(get_leave_request_service),
) -> list[LeaveRequestResponse]:
    return service.get_by_employee_id(employee_id)


@router.post(
    "/leave-requests/{leave_request_id}/approve",
    response_model=LeaveRequestResponse,
)
def approve_leave_request(
    leave_request_id: int,
    service: LeaveRequestService = Depends(get_leave_request_service),
) -> LeaveRequestResponse:
    return service.approve(leave_request_id)


@router.post(
    "/leave-requests/{leave_request_id}/reject",
    response_model=LeaveRequestResponse,
)
def reject_leave_request(
    leave_request_id: int,
    service: LeaveRequestService = Depends(get_leave_request_service),
) -> LeaveRequestResponse:
    return service.reject(leave_request_id)


@router.delete(
    "/leave-requests/{leave_request_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_leave_request(
    leave_request_id: int,
    service: LeaveRequestService = Depends(get_leave_request_service),
) -> Response:
    service.delete(leave_request_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
