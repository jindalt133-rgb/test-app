from sqlalchemy.exc import IntegrityError
from app.core.errors import AppError
from app.models.employee import Employee
from app.repositories.employee_repository import EmployeeRepository
class EmployeeService:
 def __init__(self,db): self.repository=EmployeeRepository(db)
 def create_employee(self,data):
  if self.repository.get_by_email(data.email): raise AppError(409,'EMPLOYEE_EMAIL_CONFLICT','An employee with this email already exists',{'email':data.email})
  try:return self.repository.create(Employee(name=data.name,email=data.email,department=data.department,active=data.active))
  except IntegrityError: raise AppError(409,'EMPLOYEE_EMAIL_CONFLICT','An employee with this email already exists',{'email':data.email}) from None
 def get_all_employees(self): return self.repository.get_all()
 def get_employee(self,i):
  e=self.repository.get_by_id(i)
  if e is None: raise AppError(404,'EMPLOYEE_NOT_FOUND',f'Employee with ID {i} was not found',{'employee_id':i})
  return e
