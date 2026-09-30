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
        details: list[dict[str, Any]] | None = None,
    ) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


def error_payload(
    def _error_body(code: str, message: str, details: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    error: dict[str, Any] = {"code": code, "message": message}
    if details is not None:
        error["details"] = details
    return {"error": error}


async def app_error_handler(
    _: Request,
    exc: AppError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content=error_payload(
            exc.code,
            exc.message,
            exc.details,
        ),
    )


async def validation_error_handler(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors: list[dict[str, str]] = []

    for item in exc.errors():
        location = item.get("loc", ())
        field = str(location[-1]) if location else "request"

        errors.append(
            {
                "field": field,
                "message": item.get("msg", "Invalid value."),
            }
        )

    return JSONResponse(
        status_code=422,
        content=_error_body("VALIDATION_ERROR", "Request validation failed", details),
    )
