from fastapi import APIRouter,Depends,Response
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.leave_request import LeaveRequestCreate,LeaveRequestResponse
from app.services.leave_request_service import LeaveRequestService
router=APIRouter(prefix='/leave-requests',tags=['leave-requests'])
@router.post('',response_model=LeaveRequestResponse,status_code=201)
def create_leave_request(data:LeaveRequestCreate,db:Session=Depends(get_db)): return LeaveRequestResponse.model_validate(LeaveRequestService(db).create_leave_request(data))
@router.get('',response_model=list[LeaveRequestResponse])
def get_leave_requests(db:Session=Depends(get_db)): return [LeaveRequestResponse.model_validate(x) for x in LeaveRequestService(db).get_all_leave_requests()]
@router.post('/{leave_request_id}/approve',response_model=LeaveRequestResponse)
def approve_leave_request(leave_request_id:int,db:Session=Depends(get_db)): return LeaveRequestResponse.model_validate(LeaveRequestService(db).approve_leave_request(leave_request_id))
@router.post('/{leave_request_id}/reject',response_model=LeaveRequestResponse)
def reject_leave_request(leave_request_id:int,db:Session=Depends(get_db)): return LeaveRequestResponse.model_validate(LeaveRequestService(db).reject_leave_request(leave_request_id))
@router.delete('/{leave_request_id}',status_code=204)
def delete_leave_request(leave_request_id:int,db:Session=Depends(get_db)): LeaveRequestService(db).delete_leave_request(leave_request_id); return Response(status_code=204)
