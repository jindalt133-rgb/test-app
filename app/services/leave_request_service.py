from app.core.errors import AppError
from app.models.leave_request import LeaveRequest,LeaveStatus
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.leave_request_repository import LeaveRequestRepository
class LeaveRequestService:
 def __init__(self,db): self.employee_repository=EmployeeRepository(db); self.repository=LeaveRequestRepository(db)
 def create_leave_request(self,d):
  e=self.employee_repository.get_by_id(d.employee_id)
  if e is None: raise AppError(404,'EMPLOYEE_NOT_FOUND',f'Employee with ID {d.employee_id} was not found',{'employee_id':d.employee_id})
  if not e.active: raise AppError(409,'EMPLOYEE_INACTIVE','Leave requests can only be created for active employees',{'employee_id':d.employee_id})
  return self.repository.create(LeaveRequest(employee_id=d.employee_id,leave_type=d.leave_type,start_date=d.start_date,end_date=d.end_date,reason=d.reason,status=LeaveStatus.PENDING))
 def get_all_leave_requests(self): return self.repository.get_all()
 def get_employee_leave_requests(self,i):
  if self.employee_repository.get_by_id(i) is None: raise AppError(404,'EMPLOYEE_NOT_FOUND',f'Employee with ID {i} was not found',{'employee_id':i})
  return self.repository.get_by_employee_id(i)
 def _get(self,i):
  r=self.repository.get_by_id(i)
  if r is None: raise AppError(404,'LEAVE_REQUEST_NOT_FOUND',f'Leave request with ID {i} was not found',{'leave_request_id':i})
  return r
 def _change(self,i,s):
  r=self._get(i)
  if r.status!=LeaveStatus.PENDING: raise AppError(409,'INVALID_STATUS_TRANSITION','Only pending leave requests can be changed',{'leave_request_id':r.id,'current_status':r.status.value})
  r.status=s; return self.repository.save(r)
 def approve_leave_request(self,i): return self._change(i,LeaveStatus.APPROVED)
 def reject_leave_request(self,i): return self._change(i,LeaveStatus.REJECTED)
 def delete_leave_request(self,i):
  r=self._get(i)
  if r.status!=LeaveStatus.PENDING: raise AppError(409,'INVALID_STATUS_TRANSITION','Only pending leave requests can be changed',{'leave_request_id':r.id,'current_status':r.status.value})
  self.repository.delete(r)
