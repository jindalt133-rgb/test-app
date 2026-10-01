from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(self, status_code: int, code: str, message: str, details: Any = None) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details if details is not None else {}
        super().__init__(message)


def app_error_response(error: AppError) -> JSONResponse:
    return JSONResponse(status_code=error.status_code, content={"error": {"code": error.code, "message": error.message, "details": error.details}})


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    details: dict[str, str] = {}
    for validation_error in exc.errors():
        location = validation_error.get("loc", ())
        field = ".".join(str(item) for item in location if item != "body")
        details[field or "request"] = validation_error.get("msg", "Invalid value")
    return JSONResponse(status_code=422, content={"error": {"code": "VALIDATION_ERROR", "message": "Request validation failed", "details": details}})
