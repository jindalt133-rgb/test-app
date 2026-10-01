from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.leave_request import LeaveRequest
class LeaveRequestRepository:
 def __init__(self,db:Session): self.db=db
 def create(self,r): self.db.add(r); self.db.commit(); self.db.refresh(r); return r
 def get_all(self): return list(self.db.scalars(select(LeaveRequest).order_by(LeaveRequest.id)).all())
 def get_by_id(self,i): return self.db.scalar(select(LeaveRequest).where(LeaveRequest.id==i))
 def get_by_employee_id(self,i): return list(self.db.scalars(select(LeaveRequest).where(LeaveRequest.employee_id==i).order_by(LeaveRequest.id)).all())
 def save(self,r): self.db.add(r); self.db.commit(); self.db.refresh(r); return r
 def delete(self,r): self.db.delete(r); self.db.commit()
