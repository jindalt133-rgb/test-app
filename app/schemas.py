from pydantic import BaseModel, ConfigDict, field_validator


class TaskCreate(BaseModel):
    title: str
    completed: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        stripped_value = value.strip()
        if not stripped_value:
            raise ValueError("title must not be blank")
        return stripped_value


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    completed: bool


class HealthResponse(BaseModel):
    status: str
