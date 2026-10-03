"""FastAPI application for the task management service."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from .database import Database
from .schemas import HealthResponse, Task, TaskCreate


def create_app(database_path: str | Path | None = None) -> FastAPI:
    """Create and configure the FastAPI application.

    A database path can be supplied directly for isolated testing. Otherwise,
    TASK_DB_PATH is used, falling back to tasks.db.
    """
    configured_path = database_path or os.getenv("TASK_DB_PATH", "tasks.db")
    database = Database(configured_path)

    application = FastAPI(title="task-management-service")

    @application.on_event("startup")
    def initialize_database() -> None:
        database.initialize()

    @application.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid input",
                    "details": _validation_details(exc),
                }
            },
        )

    @application.exception_handler(ValidationError)
    async def pydantic_validation_exception_handler(
        request: Request,
        exc: ValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid input",
                    "details": exc.errors(),
                }
            },
        )

    @application.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail,
            headers=exc.headers,
        )

    @application.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok")

    @application.post(
        "/tasks",
        response_model=Task,
        status_code=status.HTTP_201_CREATED,
    )
    def create_task(task_input: TaskCreate) -> Task:
        task = database.create_task(
            title=task_input.title,
            completed=task_input.completed,
        )
        return Task.model_validate(task)

    @application.get("/tasks", response_model=list[Task])
    def get_tasks() -> list[Task]:
        return [Task.model_validate(task) for task in database.get_tasks()]

    @application.get("/tasks/{task_id}", response_model=Task)
    def get_task(task_id: int) -> Task:
        task = database.get_task(task_id)
        if task is None:
            raise _task_not_found()
        return Task.model_validate(task)

    @application.delete(
        "/tasks/{task_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    def delete_task(task_id: int) -> None:
        if not database.delete_task(task_id):
            raise _task_not_found()

    return application


def _task_not_found() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "error": {
                "code": "TASK_NOT_FOUND",
                "message": "Task not found",
            }
        },
    )


def _validation_details(exception: RequestValidationError) -> list[dict[str, Any]]:
    details: list[dict[str, Any]] = []
    for error in exception.errors():
        normalized = dict(error)
        context = normalized.get("ctx")
        if context and "error" in context:
            normalized["ctx"] = {
                key: str(value) if key == "error" else value
                for key, value in context.items()
            }
        details.append(normalized)
    return details


app = create_app()
