from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from app.core.config import get_database_url


def create_database_engine() -> Engine:
    database_url = get_database_url()
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, connect_args=connect_args, pool_pre_ping=True)


engine = create_database_engine()
