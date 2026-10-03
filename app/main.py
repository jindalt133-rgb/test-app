from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from fastapi import FastAPI

from app.database import create_tables
from app.routes import employees, health, leave_requests


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    create_tables()
    yield


app = FastAPI(
    title="Employee Leave Management Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health.router)
app.include_router(employees.router)
app.include_router(leave_requests.router)
