"""FastAPI application entry point."""

from __future__ import annotations

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.books import router as books_router
from app.core.errors import ApplicationError, application_error_handler, unexpected_error_handler, validation_error_handler
from app.db.database import initialize_database
from app.schemas.books import HealthResponse


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncIterator[None]:
    initialize_database()
    yield


app = FastAPI(title="library-catalog-service", description="REST API for managing a library book catalog.", version="0.1.0", lifespan=lifespan)
app.add_exception_handler(ApplicationError, application_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.add_exception_handler(Exception, unexpected_error_handler)
app.include_router(books_router)


@app.get("/health", response_model=HealthResponse, tags=["health"])
def health() -> HealthResponse:
    return HealthResponse(status="ok")