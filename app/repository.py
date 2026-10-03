"""SQLite repository for task persistence."""

from __future__ import annotations

import sqlite3

from app.database import Database
from app.models import TaskCreate, TaskResponse


class TaskRepository:
    """Perform task persistence operations."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def create(self, task: TaskCreate) -> TaskResponse:
        connection = self.database.connect()
        try:
            cursor = connection.execute(
                "INSERT INTO tasks (title, completed) VALUES (?, ?)",
                (task.title, int(task.completed)),
            )
            connection.commit()
            task_id = int(cursor.lastrowid)
            return TaskResponse(id=task_id, title=task.title, completed=task.completed)
        finally:
            connection.close()

    def list_all(self) -> list[TaskResponse]:
        connection = self.database.connect()
        try:
            rows = connection.execute("SELECT id, title, completed FROM tasks ORDER BY id").fetchall()
            return [self._to_model(row) for row in rows]
        finally:
            connection.close()

    def get_by_id(self, task_id: int) -> TaskResponse | None:
        connection = self.database.connect()
        try:
            row = connection.execute("SELECT id, title, completed FROM tasks WHERE id = ?", (task_id,)).fetchone()
            return self._to_model(row) if row is not None else None
        finally:
            connection.close()

    def delete(self, task_id: int) -> bool:
        connection = self.database.connect()
        try:
            cursor = connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            connection.commit()
            return cursor.rowcount > 0
        finally:
            connection.close()

    @staticmethod
    def _to_model(row: sqlite3.Row) -> TaskResponse:
        return TaskResponse(id=int(row["id"]), title=str(row["title"]), completed=bool(row["completed"]))
