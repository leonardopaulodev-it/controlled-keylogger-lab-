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

        self.setPlaceholderText("Escreve aqui...")
        self.setMinimumHeight(100)

    def keyPressEvent(self, event) -> None:
        """Handle keyboard input inside the controlled area."""

        key = event.key()

        # -------------------------
        # Modifier keys
        # -------------------------

        if key == Qt.Key_Control:
            self._log_control_event(
                EventType.CTRL,
                "ctrl",
            )
            event.accept()
            return

        if key == Qt.Key_Shift:
            self._log_control_event(
                EventType.SHIFT,
                "shift",
            )
            event.accept()
            return

        if key == Qt.Key_Alt:
            self._log_control_event(
                EventType.ALT,
                "alt",
            )
            event.accept()
            return

        # -------------------------
        # Backspace
        # -------------------------

        if key == Qt.Key_Backspace:
            self._handle_backspace(event)
            return

        # -------------------------
        # Enter
        # -------------------------

        if key in (
            Qt.Key_Return,
            Qt.Key_Enter,
        ):
            self._finish_input()

            self._log_control_event(
                EventType.ENTER,
                "enter",
            )

            self.clear()

            event.accept()
            return

        # -------------------------
        # Space
        # -------------------------

        if key == Qt.Key_Space:
            self._finish_input()

            self._log_control_event(
                EventType.SPACE,
                "space",
            )

            self.clear()

            event.accept()
            return

        # -------------------------
        # Tab
        # -------------------------

        if key == Qt.Key_Tab:
            self._log_control_event(
                EventType.TAB,
                "tab",
            )

            event.accept()
            return

        # -------------------------
        # Escape
        # -------------------------

        if key == Qt.Key_Escape:
            self._log_control_event(
                EventType.ESCAPE,
                "escape",
            )

            event.accept()
            return

        # -------------------------
        # Delete
        # -------------------------

        if key == Qt.Key_Delete:
            self._log_control_event(
                EventType.DELETE,
                "delete",
            )

            super().keyPressEvent(event)
            return

        # -------------------------
        # Letters
        # -------------------------

        text = event.text()

        if text and text.isalpha():
            self.text_buffer += text
            super().keyPressEvent(event)
            return

        # -------------------------
        # Other characters
        # -------------------------

        if text:
            super().keyPressEvent(event)
            return

        event.accept()

    def _handle_backspace(self, event) -> None:
        """Handle Backspace."""

        if self.text_buffer:
            self.text_buffer = self.text_buffer[:-1]

        self._log_control_event(
            EventType.BACKSPACE,
            "backspace",
        )

        super().keyPressEvent(event)

    def _finish_input(self) -> None:
        """Classify and persist the current text."""

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