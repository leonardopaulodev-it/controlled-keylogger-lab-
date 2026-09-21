from __future__ import annotations

import logging
import sqlite3
from datetime import datetime
from pathlib import Path

from agent.models.events import EventType, KeyboardEvent


class EventLogger:
    """Persists keyboard events to a SQLite database."""

    DEFAULT_DATABASE_PATH = "data/events.sqlite"

    def __init__(
        self,
        database_path: str | Path = DEFAULT_DATABASE_PATH,
    ) -> None:
        self.database_path = Path(database_path)

        self._logger = logging.getLogger(__name__)

        self._ensure_storage_directory()
        self._initialize_database()

    def log(self, event: KeyboardEvent) -> None:
        """Persist a keyboard event to the database."""

        self._validate_event(event)

        try:
            with sqlite3.connect(self.database_path) as connection:
                connection.execute(
                    """
                    INSERT INTO events (
                        timestamp,
                        event_type,
                        key,
                        source
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        event.timestamp.strftime("%Y/%m/%d %H:%M:%S"),
                        event.event_type.value,
                        event.key,
                        event.source,
                    ),
                )

        except sqlite3.Error:
            self._logger.exception(
                "Failed to persist event to database: %s",
                self.database_path,
            )
            raise

        self._logger.debug(
            "Event persisted: type=%s key=%r source=%s",
            event.event_type.value,
            event.key,
            event.source,
        )

    def _validate_event(self, event: KeyboardEvent) -> None:
        """Validate the event before persisting it."""

        if not isinstance(event, KeyboardEvent):
            raise TypeError(
                "event must be an instance of KeyboardEvent"
            )

        if not isinstance(event.event_type, EventType):
            raise TypeError(
                "event.event_type must be an instance of EventType"
            )

        if not isinstance(event.key, str):
            raise TypeError(
                "event.key must be a string"
            )

        if not isinstance(event.source, str):
            raise TypeError(
                "event.source must be a string"
            )

    def _ensure_storage_directory(self) -> None:
        """Create the database directory if necessary."""

        try:
            self.database_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )
        except OSError:
            self._logger.exception(
                "Failed to create storage directory: %s",
                self.database_path.parent,
            )
            raise

    def _initialize_database(self) -> None:
        """Create the database schema if it does not exist."""

        try:
            with sqlite3.connect(self.database_path) as connection:
                connection.execute(
                    """
                    CREATE TABLE IF NOT EXISTS events (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        event_type TEXT NOT NULL,
                        key TEXT NOT NULL,
                        source TEXT NOT NULL
                    )
                    """
                )

                connection.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_events_timestamp
                    ON events(timestamp)
                    """
                )

                connection.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_events_event_type
                    ON events(event_type)
                    """
                )

        except sqlite3.Error:
            self._logger.exception(
                "Failed to initialize database: %s",
                self.database_path,
            )
            raise