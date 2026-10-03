"""SQLite database access for the task management service."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


class Database:
    """Small SQLite database wrapper using one connection per operation."""

    def __init__(self, path: str | Path) -> None:
        self.path = str(path)

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def initialize(self) -> None:
        """Create the database schema if it does not already exist."""
        connection = self._connect()
        try:
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
        finally:
            connection.close()

    def create_task(self, title: str, completed: bool) -> dict[str, Any]:
        connection = self._connect()
        try:
            cursor = connection.execute(
                "INSERT INTO tasks (title, completed) VALUES (?, ?)",
                (title, int(completed)),
            )
            connection.commit()
            task_id = cursor.lastrowid
            row = connection.execute(
                "SELECT id, title, completed FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()
            if row is None:
                raise RuntimeError("Created task could not be retrieved")
            return self._row_to_task(row)
        finally:
            connection.close()

    def get_tasks(self) -> list[dict[str, Any]]:
        connection = self._connect()
        try:
            rows = connection.execute(
                "SELECT id, title, completed FROM tasks ORDER BY id"
            ).fetchall()
            return [self._row_to_task(row) for row in rows]
        finally:
            connection.close()

    def get_task(self, task_id: int) -> dict[str, Any] | None:
        connection = self._connect()
        try:
            row = connection.execute(
                "SELECT id, title, completed FROM tasks WHERE id = ?",
                (task_id,),
            ).fetchone()
            return self._row_to_task(row) if row is not None else None
        finally:
            connection.close()

    def delete_task(self, task_id: int) -> bool:
        connection = self._connect()
        try:
            cursor = connection.execute(
                "DELETE FROM tasks WHERE id = ?",
                (task_id,),
            )
            connection.commit()
            return cursor.rowcount > 0
        finally:
            connection.close()

    @staticmethod
    def _row_to_task(row: sqlite3.Row) -> dict[str, Any]:
        return {
            "id": int(row["id"]),
            "title": str(row["title"]),
            "completed": bool(row["completed"]),
        }
