from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.errors import AppError
from app.models import Employee, LeaveRequest, LeaveStatus
from app.repositories import EmployeeRepository, LeaveRequestRepository
from app.schemas import EmployeeCreate, LeaveRequestCreate


class EmployeeService:
    def __init__(self, db: Session) -> None:
        self.repository = EmployeeRepository(db)

    def create_employee(self, data: EmployeeCreate) -> Employee:
        email = str(data.email).lower()
        if self.repository.get_by_email(email):
            raise AppError(
                409,
                "DUPLICATE_EMPLOYEE_EMAIL",
                f"An employee with email '{email}' already exists.",
            )

        employee = Employee(
            name=data.name,
            email=email,
            department=data.department,
            active=data.active,
        )
        try:
            return self.repository.create(employee)
        except IntegrityError:
            self.repository.db.rollback()
            raise AppError(
                409,
                "DUPLICATE_EMPLOYEE_EMAIL",
                f"An employee with email '{email}' already exists.",
            ) from None

    def list_employees(self) -> list[Employee]:
        return self.repository.list()

    def get_employee(self, employee_id: int) -> Employee:
        employee = self.repository.get(employee_id)
        if employee is None:
            raise AppError(
                404,
                "EMPLOYEE_NOT_FOUND",
                f"Employee {employee_id} was not found.",
            )
        return employee


class LeaveRequestService:
    def __init__(self, db: Session) -> None:
        self.employee_repository = EmployeeRepository(db)
        self.repository = LeaveRequestRepository(db)

    def create_leave_request(self, data: LeaveRequestCreate) -> LeaveRequest:
        employee = self.employee_repository.get(data.employee_id)
        if employee is None:
            raise AppError(
                404,
                "EMPLOYEE_NOT_FOUND",
                f"Employee {data.employee_id} was not found.",
            )
        if not employee.active:
            raise AppError(
                409,
                "INACTIVE_EMPLOYEE",
                f"Employee {data.employee_id} is inactive and cannot submit leave.",
            )

        leave_request = LeaveRequest(
            employee_id=data.employee_id,
            leave_type=data.leave_type,
            start_date=data.start_date,
            end_date=data.end_date,
            reason=data.reason,
            status=LeaveStatus.PENDING,
        )
        return self.repository.create(leave_request)

    def list_leave_requests(self) -> list[LeaveRequest]:
        return self.repository.list()

    def list_employee_leave_requests(
        self,
        employee_id: int,
    ) -> list[LeaveRequest]:
        if self.employee_repository.get(employee_id) is None:
            raise AppError(
                404,
                "EMPLOYEE_NOT_FOUND",
                f"Employee {employee_id} was not found.",
            )
        return self.repository.list_by_employee(employee_id)

    def get_leave_request(self, leave_request_id: int) -> LeaveRequest:
        leave_request = self.repository.get(leave_request_id)
        if leave_request is None:
            raise AppError(
                404,
                "LEAVE_REQUEST_NOT_FOUND",
                f"Leave request {leave_request_id} was not found.",
            )
        return leave_request

    def transition(
        self,
        leave_request_id: int,
        target_status: LeaveStatus,
    ) -> LeaveRequest:
        leave_request = self.get_leave_request(leave_request_id)
        if leave_request.status != LeaveStatus.PENDING:
            raise AppError(
                409,
                "INVALID_LEAVE_STATUS",
                (
                    f"Leave request {leave_request_id} has status "
                    f"{leave_request.status.value} and cannot be transitioned."
                ),
            )
        leave_request.status = target_status
        return self.repository.save(leave_request)

    def delete_leave_request(self, leave_request_id: int) -> None:
        leave_request = self.get_leave_request(leave_request_id)
        if leave_request.status != LeaveStatus.PENDING:
            raise AppError(
                409,
                "INVALID_LEAVE_STATUS",
                (
                    f"Leave request {leave_request_id} has status "
                    f"{leave_request.status.value} and cannot be deleted."
                ),
            )
        self.repository.delete(leave_request)
