from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from agent.models.events import KeyboardEvent
from agent.storage.event_logger import EventLogger


class KeyboardCollector(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Controlled Keyboard Lab")
        self.setMinimumSize(600, 400)

        self.setFocusPolicy(Qt.StrongFocus)

        self.logger = EventLogger()

    def keyPressEvent(self, event):
        key = event.text()

        if not key:
            key = str(event.key())

        keyboard_event = KeyboardEvent(
            timestamp=datetime.now(),
            event_type="key_press",
            key=key,
            source="controlled-input-window"
        )

        self.logger.log(keyboard_event)

        print(keyboard_event)

        event.accept()