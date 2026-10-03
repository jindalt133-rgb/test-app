from collections.abc import Generator
from contextlib import asynccontextmanager
from sqlite3 import Connection

from fastapi import Depends, FastAPI, HTTPException, Path, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.db import get_connection, initialize_database
from app.repository import create_task, delete_task, get_all_tasks, get_task
from app.schemas import TaskCreate, TaskResponse


@asynccontextmanager
async def lifespan(_: FastAPI):
    initialize_database()
    yield


app = FastAPI(title="task-management-service", lifespan=lifespan)


def get_db() -> Generator[Connection, None, None]:
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    errors = [{"type": error["type"], "loc": list(error["loc"]), "msg": error["msg"]} for error in exc.errors()]
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": {"code": "VALIDATION_ERROR", "message": "Invalid request", "errors": errors}})


def task_not_found() -> HTTPException:
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={"code": "TASK_NOT_FOUND", "message": "Task not found"})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(task: TaskCreate, connection: Connection = Depends(get_db)) -> dict:
    return create_task(connection, task)


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks_endpoint(connection: Connection = Depends(get_db)) -> list[dict]:
    return get_all_tasks(connection)


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_endpoint(task_id: int = Path(gt=0), connection: Connection = Depends(get_db)) -> dict:
    task = get_task(connection, task_id)
    if task is None:
        raise task_not_found()
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task_endpoint(task_id: int = Path(gt=0), connection: Connection = Depends(get_db)) -> None:
    if not delete_task(connection, task_id):
        raise task_not_found()
