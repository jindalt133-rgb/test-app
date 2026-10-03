from pydantic import BaseModel, ConfigDict, field_validator


class TaskCreate(BaseModel):
    title: str
    completed: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("title must not be blank")
        return value.strip()


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool
