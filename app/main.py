from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api import books, health
from app.database import initialize_database
from app.exceptions import AppError
from app.schemas import ErrorResponse

app = FastAPI(title="library-catalog-service", description="REST API for managing a library book catalog", version="1.0.0")
@app.on_event("startup")
def startup() -> None: initialize_database()
@app.exception_handler(AppError)
def handle_app_error(_: Request, exc: AppError) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=ErrorResponse(status=exc.status_code, code=exc.code, message=exc.message, errors=exc.errors).model_dump())
@app.exception_handler(RequestValidationError)
def handle_validation_error(_: Request, exc: RequestValidationError) -> JSONResponse:
    errors = []
    for item in exc.errors():
        location = item.get("loc", ())
        fields = [str(value) for value in location if value not in {"body", "query", "path"}]
        errors.append({"field": ".".join(fields) if fields else "request", "message": str(item.get("msg", "Invalid value"))})
    body = ErrorResponse(status=422, code="VALIDATION_ERROR", message="Request validation failed", errors=errors)
    return JSONResponse(status_code=422, content=body.model_dump())
@app.exception_handler(Exception)
def handle_unexpected_error(_: Request, __: Exception) -> JSONResponse:
    body = ErrorResponse(status=500, code="INTERNAL_SERVER_ERROR", message="An unexpected server error occurred", errors=[])
    return JSONResponse(status_code=500, content=body.model_dump())
app.include_router(books.router)
app.include_router(health.router)