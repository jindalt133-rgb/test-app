import os


DEFAULT_DATABASE_URL = "sqlite:///./employee_leave_management.db"


def get_database_url() -> str:
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
