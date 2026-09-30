from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes.books import router as books_router
from app.api.routes.health import router as health_router
from app.database.initialization import initialize_database
from app.errors.exceptions import ApplicationError


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="Library Catalog Service",
    description="REST API for managing a library book catalog.",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(ApplicationError)
async def application_error_handler(
    _: Request,
    exc: ApplicationError,
) -> JSONResponse:
    error: dict[str, Any] = {
        "code": exc.code,
        "message": exc.message,
    }

    if exc.details:
        error["details"] = exc.details

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": error},
    )


@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    _: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    details: list[dict[str, str]] = []

    for error in exc.errors():
        location = error.get("loc", ())
        field_parts = [
            str(part)
            for part in location
            if part != "body"
        ]
        field = ".".join(field_parts) or "request"
        message = str(error.get("msg", "Invalid value"))

        if error.get("type") == "value_error":
            message = message.removeprefix("Value error, ")

        details.append(
            {
                "field": field,
                "message": message,
            }
        )

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "details": details,
            }
        },
    )


app.include_router(health_router)
app.include_router(books_router)
