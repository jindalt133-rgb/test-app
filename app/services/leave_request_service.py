from app.errors import AppError
from app.models.leave_request import LeaveRequest, LeaveStatus
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.leave_request_repository import LeaveRequestRepository
from app.schemas.leave_request import LeaveRequestCreate


class LeaveRequestService:
    def __init__(
        self,
        repository: LeaveRequestRepository,
        employee_repository: EmployeeRepository,
    ) -> None:
        self.repository = repository
        self.employee_repository = employee_repository

    def create(self, data: LeaveRequestCreate) -> LeaveRequest:
        employee = self.employee_repository.get_by_id(data.employee_id)

        if employee is None:
            raise AppError(
                status_code=404,
                code="EMPLOYEE_NOT_FOUND",
                message=f"Employee {data.employee_id} was not found",
            )

        if not employee.active:
            raise AppError(
                status_code=409,
                code="INACTIVE_EMPLOYEE",
                message=f"Employee {data.employee_id} is inactive",
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

    def get_all(self) -> list[LeaveRequest]:
        return self.repository.get_all()

    def get_by_employee_id(self, employee_id: int) -> list[LeaveRequest]:
        self._ensure_employee_exists(employee_id)
        return self.repository.get_by_employee_id(employee_id)

    def approve(self, leave_request_id: int) -> LeaveRequest:
        leave_request = self._get_request(leave_request_id)
        self._ensure_pending(leave_request)
        leave_request.status = LeaveStatus.APPROVED
        return self.repository.save(leave_request)

    def reject(self, leave_request_id: int) -> LeaveRequest:
        leave_request = self._get_request(leave_request_id)
        self._ensure_pending(leave_request)
        leave_request.status = LeaveStatus.REJECTED
        return self.repository.save(leave_request)

    def delete(self, leave_request_id: int) -> None:
        leave_request = self._get_request(leave_request_id)
        self._ensure_pending(leave_request)
        self.repository.delete(leave_request)

    def _get_request(self, leave_request_id: int) -> LeaveRequest:
        leave_request = self.repository.get_by_id(leave_request_id)
        if leave_request is None:
            raise AppError(
                status_code=404,
                code="LEAVE_REQUEST_NOT_FOUND",
                message=f"Leave request {leave_request_id} was not found",
            )
        return leave_request

    def _ensure_employee_exists(self, employee_id: int) -> None:
        if self.employee_repository.get_by_id(employee_id) is None:
            raise AppError(
                status_code=404,
                code="EMPLOYEE_NOT_FOUND",
                message=f"Employee {employee_id} was not found",
            )

    def _ensure_pending(self, leave_request: LeaveRequest) -> None:
        if leave_request.status != LeaveStatus.PENDING:
            raise AppError(
                status_code=409,
                code="INVALID_LEAVE_STATUS",
                message=(
                    f"Leave request {leave_request.id} has status "
                    f"{leave_request.status.value} and cannot be changed"
                ),
            )
