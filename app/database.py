from __future__

import os
import sqlite3
from pathlib import Path
from typing import Any


DEFAULT_DATABASE_PATH = "tasks.db"


def database_path() -> str:
    """Return the configured SQLite database path."""
    return os.getenv("TASK_DATABASE_PATH", DEFAULT_DATABASE_PATH)


def connect(path: str | Path | None = None) -> sqlite3.Connection:
    """Open a SQLite connection with row-name access enabled."""
    connection = sqlite3.connect(str(path or database_path()))
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database(path: str | Path | None = None) -> None:
    """Create the tasks table if it does not already exist."""
    with connect(path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        connection.commit()


def create_task(
    title: str,
    completed: bool = False,
    path: str | Path | None = None,
) -> dict[str, Any]:
    with connect(path) as connection:
        cursor = connection.execute(
            "INSERT INTO tasks (title, completed) VALUES (?, ?)",
            (title, int(completed)),
        )
        connection.commit()
        task_id = cursor.lastrowid

    return get_task(task_id, path)


def get_tasks(path: str | Path | None = None) -> list[dict[str, Any]]:
    with connect(path) as connection:
        rows = connection.execute(
            "SELECT id, title, completed FROM tasks ORDER BY id"
        ).fetchall()

    return [_row_to_task(row) for row in rows]


def get_task(task_id: int, path: str | Path | None = None) -> dict[str, Any] | None:
    with connect(path) as connection:
        row = connection.execute(
            "SELECT id, title, completed FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

    return _row_to_task(row) if row is not None else None


def delete_task(task_id: int, path: str | Path | None = None) -> bool:
    with connect(path) as connection:
        cursor = connection.execute(
            "DELETE FROM tasks WHERE id = ?",
            (task_id,),
        )
        connection.commit()

    return cursor.rowcount > 0


def _row_to_task(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "id": row["id"],
        "title": row["title"],
        "completed": bool(row["completed"]),
    }
