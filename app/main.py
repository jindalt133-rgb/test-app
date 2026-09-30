from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.books import router as books_router
from app.api.routes.health import router as health_router
from app.core.errors import register_exception_handlers
from app.database.base import Base
from app.database.session import engine
from app.models import book  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Library Catalog Service",
    version="0.1.0",
    lifespan=lifespan,
)

register_exception_handlers(app)
app.include_router(health_router)
app.include_router(books_router, prefix="/api/v1")