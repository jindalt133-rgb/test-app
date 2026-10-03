from __future__ import annotations

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import database
from app.schemas import HealthResponse, TaskCreate, TaskResponse


def create_app(database_path: str | Path | None = None) -> FastAPI:
    application = FastAPI(title="task-management-service")
    application.state.database_path = str(database_path) if database_path else None
    database.initialize_database(application.state.database_path)

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid request",
                    "details": _json_safe_errors(exc.errors()),
                }
            },
        )

    @application.exception_handler(HTTPException)
    async def http_exception_handler(
        request: Request,
        exc: HTTPException,
    ) -> JSONResponse:
        if isinstance(exc.detail, dict):
            content: Any = {"error": exc.detail}
        else:
            content = {"error": {"code": "HTTP_ERROR", "message": str(exc.detail)}}

    @application.post("/tasks", response_model=TaskResponse, status_code=201)

    @application.get("/health", response_model=HealthResponse)
    def health() -> HealthResponse:
        return HealthResponse(status="ok")

    @application.post("/tasks", response_model=TaskResponse, status_code=201)
    def create_task(task: TaskCreate) -> dict[str, Any]:
        return database.create_task(title=task.title, completed=task.completed, path=application.state.database_path)

    @application.get("/tasks", response_model=list[TaskResponse])
    def get_tasks() -> list[dict[str, Any]]:
        return database.get_tasks(application.state.database_path)

    @application.get("/tasks/{task_id}", response_model=TaskResponse)
    def get_task(task_id: int) -> dict[str, Any]:
        task = database.get_task(task_id, application.state.database_path)
        if task is None:
            raise _task_not_found()
        return task

    @application.delete("/tasks/{task_id}", status_code=204)
    def delete_task(task_id: int) -> None:
        if not database.delete_task(task_id, application.state.database_path):
            raise _task_not_found()

    return application


def _task_not_found() -> HTTPException:
    return HTTPException(status_code=404, detail={"code": "TASK_NOT_FOUND", "message": "Task not found"})


def _json_safe_errors(errors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [_json_safe_value(error) for error in errors]


def _json_safe_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe_value(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


app = create_app()
import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app import database
from app.schemas import HealthResponse, TaskCreate, TaskResponse


class TaskNotFoundError(Exception):
    """Raised when a requested task does not exist."""


def create_app(database_path: str | None = None) -> FastAPI:
    configured_database_path = database_path or os.getenv(
        "TASK_DATABASE_PATH",
        "tasks.db",
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        database.initialize_database(configured_database_path)
        yield

    application = FastAPI(
        title="task-management-service",
        lifespan=lifespan,
    )

    @application.exception_handler(TaskNotFoundError)
    async def task_not_found_handler(
        _: Request,
        __: TaskNotFoundError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=404,
            content={
                "error": {
                    "code": "task_not_found",
                    "message": "Task not found",
                }
            },
        )

    @application.exception_handler(RequestValidationError)
    async def validation_error_handler(
        _: Request,
        exc: RequestValidationError,
    ) -> JSONResponse:
        details: list[dict[str, Any]] = []

        for error in exc.errors():
            details.append(
                {
                    "loc": list(error["loc"]),
                    "msg": error["msg"],
                    "type": error["type"],
                }
            )

        return JSONResponse(
            status_code=422,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "Invalid request",
                    "details": details,
                }
            },
        )

    @application.get("/health", response_model=HealthResponse)
    async def health() -> HealthResponse:
        return HealthResponse(status="ok")

    @application.post(
        "/tasks",
        response_model=TaskResponse,
        status_code=201,
    )
    async def create_task(task: TaskCreate) -> dict[str, Any]:
        return database.create_task(
            configured_database_path,
            task.title,
            task.completed,
        )

    @application.get("/tasks", response_model=list[TaskResponse])
    async def get_tasks() -> list[dict[str, Any]]:
        return database.list_tasks(configured_database_path)

    @application.get("/tasks/{task_id}", response_model=TaskResponse)
    async def get_task(task_id: int) -> dict[str, Any]:
        task = database.get_task(configured_database_path, task_id)

        if task is None:
            raise TaskNotFoundError

        return task

    @application.delete("/tasks/{task_id}", status_code=204)
    async def remove_task(task_id: int) -> None:
        deleted = database.delete_task(configured_database_path, task_id)

        if not deleted:
            raise TaskNotFoundError

    return application


app = create_app()
