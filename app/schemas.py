"""Pydantic schemas for the task management API."""

from pydantic import BaseModel, field_validator


class TaskCreate(BaseModel):
    """Request body used to create a task."""

    title: str
    completed: bool = False

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("title must not be blank")
        return value


class Task(BaseModel):
    """Task response model."""

    id: int
    title: str
    completed: bool


class HealthResponse(BaseModel):
    """Health endpoint response model."""

    status: str
