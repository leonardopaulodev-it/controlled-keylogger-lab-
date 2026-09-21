from dataclasses import dataclass
from datetime import datetime


@dataclass
class KeyboardEvent:
    timestamp: datetime
    event_type: str
    key: str
    source: str