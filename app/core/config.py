"""Application configuration."""

from __future__ import annotations

import os


DEFAULT_DATABASE_URL = "sqlite:///./library.db"


def get_database_url() -> str:
    """Return the configured database URL or the SQLite default."""
    return os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
