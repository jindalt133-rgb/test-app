from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.employee import Employee


class EmployeeRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, employee: Employee) -> Employee:
        self.db.add(employee)
        self.db.commit()
        self.db.refresh(employee)
        return employee

    def get_all(self) -> list[Employee]:
        return list(self.db.scalars(select(Employee).order_by(Employee.id)).all())

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self.db.get(Employee, employee_id)

    def get_by_email(self, email: str) -> Employee | None:
        statement = select(Employee).where(Employee.email == email)
        return self.db.scalar(statement)
