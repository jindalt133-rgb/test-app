from fastapi import FastAPI

from app.api.routes import router
from app.database import init_db
from app.errors import (
    AppError,
    app_error_handler,
    validation_error_handler,
)
from fastapi.exceptions import RequestValidationError

app = FastAPI(
    title="Employee Leave Management Service",
    version="1.0.0",
)

app.add_exception_handler(AppError, app_error_handler)
app.add_exception_handler(RequestValidationError, validation_error_handler)
app.include_router(router)


@app.on_event("startup")
def startup() -> None:
    init_db()
