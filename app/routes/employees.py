from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.employee import EmployeeCreate, EmployeeResponse
from app.schemas.leave_request import LeaveRequestResponse
from app.services import employee_service, leave_service

router = APIRouter(prefix="/employees", tags=["employees"])


@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    payload: EmployeeCreate,
    db: Session = Depends(get_db),
) -> EmployeeResponse:
    return employee_service.create_employee(
        db=db,
        name=payload.name,
        email=payload.email,
        department=payload.department,
        active=payload.active,
    )


@router.get("", response_model=list[EmployeeResponse])
def get_employees(
    db: Session = Depends(get_db),
) -> list[EmployeeResponse]:
    return employee_service.get_all_employees(db)


@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
) -> EmployeeResponse:
    return employee_service.get_employee(db, employee_id)


@router.get(
    "/{employee_id}/leave-requests",
    response_model=list[LeaveRequestResponse],
)
def get_employee_leave_requests(
    employee_id: int,
    db: Session = Depends(get_db),
) -> list[LeaveRequestResponse]:
    return leave_service.get_leave_requests_for_employee(db, employee_id)
