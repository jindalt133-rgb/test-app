from datetime import date
from pydantic import BaseModel,ConfigDict,model_validator
from app.models.leave_request import LeaveType,LeaveStatus
class LeaveRequestCreate(BaseModel):
 employee_id:int; leave_type:LeaveType; start_date:date; end_date:date; reason:str|None=None
 @model_validator(mode='after')
 def valid_range(self):
  if self.start_date>self.end_date: raise ValueError('start_date must not be after end_date')
  return self
class LeaveRequestResponse(BaseModel):
 model_config=ConfigDict(from_attributes=True)
 id:int; employee_id:int; leave_type:LeaveType; start_date:date; end_date:date; reason:str|None; status:LeaveStatus
