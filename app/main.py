"""Application factory and FastAPI application entry point."""

from __future__ import annotations

import os
from collections.abc import Mapping
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncIterator

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api import router
from app.database import Database
from app.models import ValidationErrorResponse


def _make_json_safe(value: Any) -> Any:
    """Convert validation error values into JSON-serializable values."""
    if isinstance(value, BaseException):
        return str(value)
    if isinstance(value, Mapping):
        return {str(key): _make_json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_make_json_safe(item) for item in value]
    if isinstance(value, set):
        return [_make_json_safe(item) for item in value]
    return value


def create_app(database_path: str | Path | None = None) -> FastAPI:
    """Create a FastAPI application using the supplied SQLite database path."""
    configured_path = database_path or os.getenv("TASK_DB_PATH", "tasks.db")
    database = Database(configured_path)

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        database.initialize()
        yield

    application = FastAPI(title="task-management-service", lifespan=lifespan)
    application.state.database = database

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(_: Request, exception: RequestValidationError) -> JSONResponse:
        response = ValidationErrorResponse(
            code="VALIDATION_ERROR",
            detail=_make_json_safe(exception.errors()),
        )
        return JSONResponse(status_code=422, content=response.model_dump())

    application.include_router(router)
    return application


app = create_app()
