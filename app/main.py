from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.api.books import router as books_router
from app.api.health import router as health_router
from app.core.errors import (
    AppError,
    app_error_handler,
    validation_error_handler,
)
from app.db.database import init_db

app = FastAPI(
    title="library-catalog-service",
    version="1.0.0",
    description="REST API for managing a library book catalog.",
)


@app.on_event("startup")
def startup() -> None:
    init_db()


app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(
    RequestValidationError,
    validation_error_handler,
)

app.include_router(health_router)
app.include_router(books_router)