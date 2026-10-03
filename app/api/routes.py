from typing import Annotated
from fastapi import APIRouter,Depends,Path,Response,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import LeaveStatus
from app.schemas import EmployeeCreate,EmployeeResponse,LeaveRequestCreate,LeaveRequestResponse
from app.services import EmployeeService,LeaveRequestService
router=APIRouter(); DatabaseSession=Annotated[Session,Depends(get_db)]
@router.get('/health')
def health_check(): return {'status':'healthy'}
@router.post('/employees',response_model=EmployeeResponse,status_code=status.HTTP_201_CREATED)
def create_employee(data:EmployeeCreate,db:DatabaseSession): return EmployeeService(db).create_employee(data)
@router.get('/employees',response_model=list[EmployeeResponse])
def list_employees(db:DatabaseSession): return EmployeeService(db).list_employees()
@router.get('/employees/{employee_id}',response_model=EmployeeResponse)
def get_employee(employee_id:Annotated[int,Path(gt=0)],db:DatabaseSession): return EmployeeService(db).get_employee(employee_id)
@router.post('/leave-requests',response_model=LeaveRequestResponse,status_code=201)
def create_leave_request(data:LeaveRequestCreate,db:DatabaseSession): return LeaveRequestService(db).create_leave_request(data)
@router.get('/leave-requests',response_model=list[LeaveRequestResponse])
def list_leave_requests(db:DatabaseSession): return LeaveRequestService(db).list_leave_requests()
@router.get('/employees/{employee_id}/leave-requests',response_model=list[LeaveRequestResponse])
def list_employee_leave_requests(employee_id:Annotated[int,Path(gt=0)],db:DatabaseSession): return LeaveRequestService(db).list_employee_leave_requests(employee_id)
@router.patch('/leave-requests/{leave_request_id}/approve',response_model=LeaveRequestResponse)
def approve(leave_request_id:Annotated[int,Path(gt=0)],db:DatabaseSession): return LeaveRequestService(db).transition(leave_request_id,LeaveStatus.APPROVED)
@router.patch('/leave-requests/{leave_request_id}/reject',response_model=LeaveRequestResponse)
def reject(leave_request_id:Annotated[int,Path(gt=0)],db:DatabaseSession): return LeaveRequestService(db).transition(leave_request_id,LeaveStatus.REJECTED)
@router.delete('/leave-requests/{leave_request_id}',status_code=204)
def delete(leave_request_id:Annotated[int,Path(gt=0)],db:DatabaseSession): LeaveRequestService(db).delete_leave_request(leave_request_id); return Response(status_code=204)
