import sqlite3

from app.schemas import TaskCreate


def row_to_task(row: sqlite3.Row) -> dict:
    return {
        "id": row["id"],
        "title": row["title"],
        "completed": bool(row["completed"]),
    }


def create_task(connection: sqlite3.Connection, task: TaskCreate) -> dict:
    cursor = connection.execute(
        """
        INSERT INTO tasks (title, completed)
        VALUES (?, ?)
        """,
        (task.title, int(task.completed)),
    )
    connection.commit()

    row = connection.execute(
        "SELECT id, title, completed FROM tasks WHERE id = ?",
        (cursor.lastrowid,),
    ).fetchone()

    return row_to_task(row)


def get_all_tasks(connection: sqlite3.Connection) -> list[dict]:
    rows = connection.execute(
        """
        SELECT id, title, completed
        FROM tasks
        ORDER BY id
        """
    ).fetchall()

    return [row_to_task(row) for row in rows]


def get_task(connection: sqlite3.Connection, task_id: int) -> dict | None:
    row = connection.execute(
        """
        SELECT id, title, completed
        FROM tasks
        WHERE id = ?
        """,
        (task_id,),
    ).fetchone()

    return row_to_task(row) if row is not None else None


def delete_task(connection: sqlite3.Connection, task_id: int) -> bool:
    cursor = connection.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,),
    )
    connection.commit()
    return cursor.rowcount > 0
