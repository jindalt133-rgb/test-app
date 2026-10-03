from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.database import Base, engine
from app.errors import AppError, app_error_handler, validation_error_handler
from app.models import Employee, LeaveRequest
from app.routes import employees, health, leave_requests


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Employee Leave Management Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)

app.include_router(health.router)
app.include_router(employees.router)
app.include_router(leave_requests.router)

__all__ = ["app"]
