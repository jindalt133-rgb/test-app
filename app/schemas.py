from datetime import date
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator, model_validator
from app.models import LeaveStatus, LeaveType
def validate_non_blank(value: str) -> str:
    if not value.strip(): raise ValueError("Value must not be blank.")
    return value.strip()
class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    active: bool = True
    @field_validator("name", "department")
    @classmethod
    def validate_text_fields(cls, value: str) -> str: return validate_non_blank(value)
class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int; name: str; email: EmailStr; department: str; active: bool
class LeaveRequestCreate(BaseModel):
    employee_id: int; leave_type: LeaveType; start_date: date; end_date: date; reason: str | None = None
    @field_validator("reason")
    @classmethod
    def normalize_reason(cls, value): return None if value is None else value.strip() or None
    @model_validator(mode="after")
    def validate_date_range(self):
        if self.start_date > self.end_date: raise ValueError("start_date must not be after end_date.")
        return self
class LeaveRequestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)
    id: int; employee_id: int; leave_type: LeaveType; start_date: date; end_date: date; reason: str | None; status: LeaveStatus
