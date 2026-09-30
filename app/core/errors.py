from collections.abc import Iterable

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


class AppError(Exception):
    def __init__(
        self,
        status: int,
        code: str,
        message: str,
        errors: list[dict[str, str]] | None = None,
    ) -> None:
        self.status = status
        self.code = code
        self.message = message
        self.errors = errors or []
        super().__init__(message)


def error_payload(
    status: int,
    code: str,
    message: str,
    errors: Iterable[dict[str, str]] = (),
) -> dict:
    return {
        "status": status,
        "code": code,
        "message": message,
        "errors": list(errors),
    }


async def app_error_handler(
    _: Request,
    exc: AppError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status,
        content=error_payload(
            exc.status,
            exc.code,
            exc.message,
            exc.errors,
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
        content=error_payload(
            422,
            "VALIDATION_ERROR",
            "Request validation failed.",
            errors,
        ),
    )
