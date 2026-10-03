"""SQLite database access and schema initialization."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterator


SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0, 1))
);
"""


class Database:
    """Manage SQLite connections for the application."""

    def __init__(self, database_path: str | Path) -> None:
        self.database_path = str(database_path)

    def initialize(self) -> None:
        """Create the database schema if it does not already exist."""
        connection = self.connect()
        try:
            connection.executescript(SCHEMA)
            connection.commit()
        finally:
            connection.close()

    def connect(self) -> sqlite3.Connection:
        """Open a configured SQLite connection."""
        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row
        return connection

    def connection(self) -> Iterator[sqlite3.Connection]:
        """Provide a connection that is closed after use."""
        connection = self.connect()
        try:
            yield connection
        finally:
            connection.close()
