from __future__ import annotations

import sqlite3
from pathlib import Path


class EventRepository:
    """Provides read-only queries for the events database."""

    DEFAULT_DATABASE_PATH = "data/events.sqlite"

    def __init__(
        self,
        database_path: str | Path = DEFAULT_DATABASE_PATH,
    ) -> None:
        self.database_path = Path(database_path)

    def get_events(
        self,
        limit: int = 500,
    ) -> list[tuple]:
        """Return the most recent events."""

        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.execute(
                """
                SELECT
                    id,
                    timestamp,
                    event_type,
                    key,
                    source
                FROM events
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            )

            return cursor.fetchall()

    def count_events(self) -> int:
        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.execute(
                """
                SELECT COUNT(*)
                FROM events
                """
            )

            result = cursor.fetchone()
        return int(result[0]) if result else 0

    def search_events(
        self,
        search_text: str = "",
        event_type: str = "",
        limit: int = 500,
    ) -> list[tuple]:
        query = """
            SELECT
                id,
                timestamp,
                event_type,
                key,
                source
            FROM events
            WHERE 1 = 1
        """

        parameters: list[str | int] = []

        if search_text:
            query += """
                AND (
                    key LIKE ?
                    OR source LIKE ?
                )
            """

            pattern = f"%{search_text}%"

            parameters.extend(
                [pattern, pattern]
            )

        if event_type:
            query += """
                AND event_type = ?
            """

            parameters.append(event_type)

        query += """
            ORDER BY id DESC
            LIMIT ?
        """

        parameters.append(limit)

        with sqlite3.connect(self.database_path) as connection:
            cursor = connection.execute(
                query,
                parameters,
            )
            return cursor.fetchall()