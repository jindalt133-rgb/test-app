from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.errors import AppError
from app.models import Employee, LeaveRequest, LeaveStatus
from app.repositories import EmployeeRepository, LeaveRequestRepository
class EmployeeService:
    def __init__(self,db): self.repository=EmployeeRepository(db)
    def create_employee(self,data):
        email=str(data.email).lower()
        if self.repository.get_by_email(email): raise AppError(409,"DUPLICATE_EMPLOYEE_EMAIL",f"An employee with email '{email}' already exists.")
        try: return self.repository.create(Employee(name=data.name,email=email,department=data.department,active=data.active))
        except IntegrityError:
            self.repository.db.rollback(); raise AppError(409,"DUPLICATE_EMPLOYEE_EMAIL",f"An employee with email '{email}' already exists.") from None
    def list_employees(self): return self.repository.list()
    def get_employee(self,eid):
        item=self.repository.get(eid)
        if item is None: raise AppError(404,"EMPLOYEE_NOT_FOUND",f"Employee {eid} was not found.")
        return item
class LeaveRequestService:
    def __init__(self,db): self.employee_repository=EmployeeRepository(db); self.repository=LeaveRequestRepository(db)
    def create_leave_request(self,data):
        employee=self.employee_repository.get(data.employee_id)
        if employee is None: raise AppError(404,"EMPLOYEE_NOT_FOUND",f"Employee {data.employee_id} was not found.")
        if not employee.active: raise AppError(409,"INACTIVE_EMPLOYEE",f"Employee {data.employee_id} is inactive and cannot submit leave.")
        return self.repository.create(LeaveRequest(employee_id=data.employee_id,leave_type=data.leave_type,start_date=data.start_date,end_date=data.end_date,reason=data.reason,status=LeaveStatus.PENDING))
    def list_leave_requests(self): return self.repository.list()
    def list_employee_leave_requests(self,eid):
        if self.employee_repository.get(eid) is None: raise AppError(404,"EMPLOYEE_NOT_FOUND",f"Employee {eid} was not found.")
        return self.repository.list_by_employee(eid)
    def get_leave_request(self,rid):
        item=self.repository.get(rid)
        if item is None: raise AppError(404,"LEAVE_REQUEST_NOT_FOUND",f"Leave request {rid} was not found.")
        return item
    def transition(self,rid,target):
        item=self.get_leave_request(rid)
        if item.status != LeaveStatus.PENDING: raise AppError(409,"INVALID_LEAVE_STATUS",f"Leave request {rid} has status {item.status.value} and cannot be transitioned.")
        item.status=target; return self.repository.save(item)
    def delete_leave_request(self,rid):
        item=self.get_leave_request(rid)
        if item.status != LeaveStatus.PENDING: raise AppError(409,"INVALID_LEAVE_STATUS",f"Leave request {rid} has status {item.status.value} and cannot be deleted.")
        self.repository.delete(item)
