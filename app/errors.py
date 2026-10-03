from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(
        self,
        status_code: int,
        code: str,
        message: str,
        details: Any | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


def app_error_response(error: AppError) -> JSONResponse:
    payload = {
        "error": {
            "status": error.status_code,
            "code": error.code,
            "message": error.message,
        }
    }
    if error.details is not None:
        payload["error"]["details"] = error.details
    return JSONResponse(status_code=error.status_code, content=payload)


async def app_error_handler(_: Request, error: AppError) -> JSONResponse:
    return app_error_response(error)


async def validation_error_handler(
    _: Request,
    error: RequestValidationError,
) -> JSONResponse:
    details = []
    messages = []

    for item in error.errors():
        message = str(item.get("msg", "Invalid value"))
        if message.startswith("Value error, "):
            message = message.removeprefix("Value error, ")

        location = [str(part) for part in item.get("loc", [])]
        details.append(
            {
                "location": location,
                "message": message,
                "type": item.get("type", "validation_error"),
            }
        )
        messages.append(message)

    message = messages[0] if messages else "Invalid request"

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "status": 422,
                "code": "VALIDATION_ERROR",
                "message": message,
                "details": details,
            }
        },
    )
