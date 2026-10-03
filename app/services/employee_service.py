from sqlalchemy.exc import IntegrityError

from app.errors import AppError
from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
from app.schemas.employee import EmployeeCreate


class EmployeeService:
    def __init__(self, repository: EmployeeRepository) -> None:
        self.repository = repository

    def create(self, data: EmployeeCreate) -> Employee:
        if self.repository.get_by_email(data.email) is not None:
            raise AppError(
                status_code=409,
                code="DUPLICATE_EMPLOYEE_EMAIL",
                message=f"Employee email '{data.email}' already exists",
            )

        employee = Employee(
            name=data.name,
            email=data.email,
            department=data.department,
            active=data.active,
        )

        try:
            return self.repository.create(employee)
        except IntegrityError:
            self.repository.db.rollback()
            raise AppError(
                status_code=409,
                code="DUPLICATE_EMPLOYEE_EMAIL",
                message=f"Employee email '{data.email}' already exists",
            )

    def get_all(self) -> list[Employee]:
        return self.repository.get_all()

    def get_by_id(self, employee_id: int) -> Employee:
        employee = self.repository.get_by_id(employee_id)
        if employee is None:
            raise AppError(
                status_code=404,
                code="EMPLOYEE_NOT_FOUND",
                message=f"Employee {employee_id} was not found",
            )
        return employee
