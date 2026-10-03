from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Employee, LeaveRequest
class EmployeeRepository:
    def __init__(self,db:Session): self.db=db
    def create(self,employee): self.db.add(employee); self.db.commit(); self.db.refresh(employee); return employee
    def list(self): return list(self.db.scalars(select(Employee).order_by(Employee.id)).all())
    def get(self,employee_id): return self.db.scalar(select(Employee).where(Employee.id==employee_id))
    def get_by_email(self,email): return self.db.scalar(select(Employee).where(Employee.email==email))
class LeaveRequestRepository:
    def __init__(self,db:Session): self.db=db
    def create(self,item): self.db.add(item); self.db.commit(); self.db.refresh(item); return item
    def list(self): return list(self.db.scalars(select(LeaveRequest).order_by(LeaveRequest.id)).all())
    def list_by_employee(self,eid): return list(self.db.scalars(select(LeaveRequest).where(LeaveRequest.employee_id==eid).order_by(LeaveRequest.id)).all())
    def get(self,rid): return self.db.scalar(select(LeaveRequest).where(LeaveRequest.id==rid))
    def save(self,item): self.db.commit(); self.db.refresh(item); return item
    def delete(self,item): self.db.delete(item); self.db.commit()
