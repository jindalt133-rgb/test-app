"""HTTP routes for the Task Management Service."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status

from app.models import TaskCreate, TaskResponse
from app.repository import TaskRepository


router = APIRouter()


def get_repository(request: Request) -> TaskRepository:
    """Provide a repository backed by the application's configured database."""
    return TaskRepository(request.app.state.database)


def task_not_found() -> HTTPException:
    """Build the standard missing-task error."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail={
            "code": "TASK_NOT_FOUND",
            "message": "Task not found",
        },
    )


@router.get("/health")
def health() -> dict[str, str]:
    """Return service health status."""
    return {"status": "ok"}


@router.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: TaskCreate,
    repository: Annotated[TaskRepository, Depends(get_repository)],
) -> TaskResponse:
    """Create and return a task."""
    return repository.create(task)


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    repository: Annotated[TaskRepository, Depends(get_repository)],
) -> list[TaskResponse]:
    """Return all tasks."""
    return repository.list_all()


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    repository: Annotated[TaskRepository, Depends(get_repository)],
) -> TaskResponse:
    """Return one task by ID."""
    task = repository.get_by_id(task_id)
    if task is None:
        raise task_not_found()
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    repository: Annotated[TaskRepository, Depends(get_repository)],
) -> Response:
    """Delete one task by ID."""
    if not repository.delete(task_id):
        raise task_not_found()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
