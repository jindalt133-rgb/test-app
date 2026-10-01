from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.employee import Employee
class EmployeeRepository:
 def __init__(self,db:Session): self.db=db
 def create(self,e): self.db.add(e); self.db.commit(); self.db.refresh(e); return e
 def get_all(self): return list(self.db.scalars(select(Employee).order_by(Employee.id)).all())
 def get_by_id(self,i): return self.db.scalar(select(Employee).where(Employee.id==i))
 def get_by_email(self,email): return self.db.scalar(select(Employee).where(Employee.email==email))
