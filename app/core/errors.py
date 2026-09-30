"""Application exceptions and consistent error handlers."""

from __future__ import annotations

from typing import Any

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class ApplicationError(Exception):
    """Base exception for expected application errors."""

    def __init__(self, status_code: int, code: str, message: str, errors: list[dict[str, Any]] | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.code = code
        self.message = message
        self.errors = errors or []


def error_body(status: int, code: str, message: str, errors: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {"status": status, "code": code, "message": message, "errors": errors or []}


async def application_error_handler(_request: Request, exc: ApplicationError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=error_body(exc.status_code, exc.code, exc.message, exc.errors))


async def validation_error_handler(_request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = []
    for item in exc.errors():
        location = item.get("loc", ())
        field = ".".join(str(value) for value in location if value != "body")
        errors.append({"field": field or "request", "message": str(item.get("msg", "Invalid value"))})
    return JSONResponse(status_code=422, content=error_body(422, "VALIDATION_ERROR", "Request validation failed.", errors))


async def unexpected_error_handler(_request: Request, _exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=500, content=error_body(500, "INTERNAL_SERVER_ERROR", "An unexpected server error occurred."))
