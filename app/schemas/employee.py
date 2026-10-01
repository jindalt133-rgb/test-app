from pydantic import BaseModel, ConfigDict, field_validator
class EmployeeCreate(BaseModel):
 name:str; email:str; department:str; active:bool=True
 @field_validator('name','email','department')
 @classmethod
 def reject_blank(cls,v):
  v=v.strip()
  if not v: raise ValueError('must not be blank')
  return v
class EmployeeResponse(BaseModel):
 model_config=ConfigDict(from_attributes=True)
 id:int; name:str; email:str; department:str; active:bool
