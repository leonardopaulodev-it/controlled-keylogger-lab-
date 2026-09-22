from datetime import datetime

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QTextEdit

from agent.models.events import EventType, KeyboardEvent
from agent.processor.event_processor import EventProcessor
from agent.storage.event_logger import EventLogger


class KeyboardCollector(QTextEdit):
    """Controlled keyboard input area."""

    event_created = Signal(object)

    SOURCE = "controlled-input-window"

    def __init__(self) -> None:
        super().__init__()

        self.text_buffer = ""

        self.logger = EventLogger()
        self.processor = EventProcessor()

        self.setPlaceholderText(
            "Escreve aqui..."
        )

        self.setMinimumHeight(100)

    def keyPressEvent(self, event) -> None:
        """Handle keyboard input inside the controlled text area."""

        # Backspace
        if event.key() == Qt.Key_Backspace:
            self._handle_backspace()
            event.accept()
            return

        # Enter
        if event.key() in (
            Qt.Key_Return,
            Qt.Key_Enter,
        ):
            self._finish_input()

            self._log_control_event(
                EventType.ENTER,
                "enter",
            )

            super().keyPressEvent(event)
            return

        # Space
        if event.key() == Qt.Key_Space:
            self._finish_input()

            self._log_control_event(
                EventType.SPACE,
                "space",
            )

            super().keyPressEvent(event)
            return

        # Letras
        key = event.text()

        if key and key.isalpha():
            self.text_buffer += key

            super().keyPressEvent(event)
            return

        # Outros caracteres normais
        if key:
            super().keyPressEvent(event)
            return

        event.accept()

    def _handle_backspace(self) -> None:
        """Remove the last character from the current word."""

        if self.text_buffer:
            self.text_buffer = self.text_buffer[:-1]

        self._log_control_event(
            EventType.BACKSPACE,
            "backspace",
        )

        super().keyPressEvent(
            self._create_backspace_event()
        )

    def _create_backspace_event(self):
        """Create a Backspace key event."""

        from PySide6.QtGui import QKeyEvent

        return QKeyEvent(
            QKeyEvent.KeyPress,
            Qt.Key_Backspace,
            Qt.NoModifier,
        )

    def _finish_input(self) -> None:
        """Classify and persist the current word."""

        if not self.text_buffer:
            return

        text = self.text_buffer

        event_type = self.processor.classify_text(text)

        keyboard_event = KeyboardEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            key=text,
            source=self.SOURCE,
        )

        self.logger.log(keyboard_event)
        self.event_created.emit(keyboard_event)

        self.text_buffer = ""

    def _log_control_event(
        self,
        event_type: EventType,
        key: str,
    ) -> None:
        """Persist and emit a control event."""

        keyboard_event = KeyboardEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            key=key,
            source=self.SOURCE,
        )

        self.logger.log(keyboard_event)
        self.event_created.emit(keyboard_event)