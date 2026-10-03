from collections.abc import Mapping
from typing import Any
from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
class AppError(Exception):
    def __init__(self,status:int,code:str,message:str,details:Any|None=None): self.status=status; self.code=code; self.message=message; self.details=details; super().__init__(message)
def error_payload(status,code,message,details=None):
    error={"status":status,"code":code,"message":message}
    if details is not None: error["details"]=details
    return {"error":error}
async def app_error_handler(_:Request,exc:AppError): return JSONResponse(status_code=exc.status,content=error_payload(exc.status,exc.code,exc.message,exc.details))
async def validation_error_handler(_:Request,exc:RequestValidationError):
    details=[]
    for item in exc.errors():
        normalized=dict(item); context=normalized.get("ctx")
        if isinstance(context,Mapping): normalized["ctx"]={k:str(v) for k,v in context.items()}
        details.append(normalized)
    return JSONResponse(status_code=422,content=error_payload(422,"VALIDATION_ERROR","Request validation failed.",details))
