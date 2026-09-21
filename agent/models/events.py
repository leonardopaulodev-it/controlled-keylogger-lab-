from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class EventType(Enum):
    """Supported keyboard event types."""

    LETTER = "letter"
    WORD = "word"
    CHARACTER = "character"

    BACKSPACE = "backspace"
    ENTER = "enter"
    SPACE = "space"
    CTRL = "ctrl"
    SHIFT = "shift"
    ALT = "alt"
    TAB = "tab"
    ESCAPE = "escape"
    DELETE = "delete"

    UNKNOWN = "unknown"


@dataclass(frozen=True)
class KeyboardEvent:
    """Represents a keyboard event captured by the application."""

    timestamp: datetime
    event_type: EventType
    key: str
    source: str