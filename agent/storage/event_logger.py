import json
from pathlib import Path

from agent.models.events import KeyboardEvent


class EventLogger:
    def __init__(self, file_path: str = "data/events.json"):
        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

    def log(self, event: KeyboardEvent):
        events = []

        if self.file_path.exists():
            with self.file_path.open("r", encoding="utf-8") as file:
                try:
                    events = json.load(file)
                except json.JSONDecodeError:
                    events = []

        events.append({
            "timestamp": event.timestamp.isoformat(),
            "event_type": event.event_type,
            "key": event.key,
            "source": event.source
        })

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(
                events,
                file,
                indent=4,
                ensure_ascii=False
            )