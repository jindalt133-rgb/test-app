from fastapi import APIRouter,Depends,status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.employee import EmployeeCreate,EmployeeResponse
from app.schemas.leave_request import LeaveRequestResponse
from app.services.employee_service import EmployeeService
from app.services.leave_request_service import LeaveRequestService
router=APIRouter(prefix='/employees',tags=['employees'])
@router.post('',response_model=EmployeeResponse,status_code=201)
def create_employee(data:EmployeeCreate,db:Session=Depends(get_db)): return EmployeeResponse.model_validate(EmployeeService(db).create_employee(data))
@router.get('',response_model=list[EmployeeResponse])
def get_employees(db:Session=Depends(get_db)): return [EmployeeResponse.model_validate(x) for x in EmployeeService(db).get_all_employees()]
@router.get('/{employee_id}',response_model=EmployeeResponse)
def get_employee(employee_id:int,db:Session=Depends(get_db)): return EmployeeResponse.model_validate(EmployeeService(db).get_employee(employee_id))
@router.get('/{employee_id}/leave-requests',response_model=list[LeaveRequestResponse])
def get_employee_leave_requests(employee_id:int,db:Session=Depends(get_db)): return [LeaveRequestResponse.model_validate(x) for x in LeaveRequestService(db).get_employee_leave_requests(employee_id)]
