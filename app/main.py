from contextlib import asynccontextmanager
from fastapi import FastAPI,Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.routes import employees,health,leave_requests
from app.core.errors import AppError,app_error_response,validation_exception_handler
from app.database.configuration import engine
from app.models.employee import Base
@asynccontextmanager
async def lifespan(application):
 Base.metadata.create_all(bind=engine); yield
app=FastAPI(title='Employee Leave Management Service',version='1.0.0',lifespan=lifespan)
@app.exception_handler(AppError)
async def handle_app_error(request:Request,exc:AppError)->JSONResponse: return app_error_response(exc)
@app.exception_handler(RequestValidationError)
async def handle_validation_error(request:Request,exc:RequestValidationError)->JSONResponse: return await validation_exception_handler(request,exc)
app.include_router(health.router); app.include_router(employees.router); app.include_router(leave_requests.router)
