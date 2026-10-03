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
