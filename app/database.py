import sqlite3
from pathlib import Path
from typing import Any


SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    completed INTEGER NOT NULL DEFAULT 0 CHECK (completed IN (0, 1))
);
"""


def initialize_database(database_path: str) -> None:
    if database_path != ":memory:":
        Path(database_path).parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(database_path) as connection:
        connection.execute(SCHEMA)
        connection.commit()


def create_task(database_path: str, title: str, completed: bool) -> dict[str, Any]:
    with sqlite3.connect(database_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO tasks (title, completed)
            VALUES (?, ?)
            """,
            (title, int(completed)),
        )
        task_id = cursor.lastrowid
        connection.commit()

    return get_task(database_path, task_id)


def list_tasks(database_path: str) -> list[dict[str, Any]]:
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            """
            SELECT id, title, completed
            FROM tasks
            ORDER BY id
            """
        ).fetchall()

    return [_row_to_task(row) for row in rows]


def get_task(database_path: str, task_id: int) -> dict[str, Any] | None:
    with sqlite3.connect(database_path) as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            """
            SELECT id, title, completed
            FROM tasks
            WHERE id = ?
            """,
            (task_id,),
        ).fetchone()

    if row is None:
        return None

    return _row_to_task(row)


def delete_task(database_path: str, task_id: int) -> bool:
    with sqlite3.connect(database_path) as connection:
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
