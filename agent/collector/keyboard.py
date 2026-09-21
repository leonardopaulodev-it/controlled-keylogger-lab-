from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from agent.models.events import EventType, KeyboardEvent
from agent.processor.event_processor import EventProcessor
from agent.storage.event_logger import EventLogger


class KeyboardCollector(QWidget):
    """Collects keyboard input inside the controlled window."""

    SOURCE = "controlled-input-window"

    def __init__(self):
        super().__init__()

        self.text_buffer = ""
        self.logger = EventLogger()
        self.processor = EventProcessor()

        self.setWindowTitle("Controlled Keyboard Lab")
        self.setMinimumSize(600, 400)
        self.setFocusPolicy(Qt.StrongFocus)

    def keyPressEvent(self, event):

        # Backspace
        if event.key() == Qt.Key_Backspace:
            self._handle_backspace(event)
            return

        # Enter
        if event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self._finish_input()
            self._log_control_event(EventType.ENTER, "enter")
            event.accept()
            return

        # Space
        if event.key() == Qt.Key_Space:
            self._finish_input()
            self._log_control_event(EventType.SPACE, "space")
            event.accept()
            return

        key = event.text()

        # Letra
        if key and key.isalpha():
            self._handle_character(key)
            event.accept()
            return

        event.accept()

    def _handle_character(self, key: str):
        """Adiciona a letra ao buffer sem a classificar ainda."""

        self.text_buffer += key

        print(f"CARÁCTER: {key}")
        print(f"BUFFER: {self.text_buffer}")

    def _handle_backspace(self, event):
        """Remove a última letra do buffer e regista o Backspace."""

        print("BACKSPACE utilizado")

        if self.text_buffer:
            self.text_buffer = self.text_buffer[:-1]

        print(f"BUFFER: {self.text_buffer}")

        self._log_control_event(
            EventType.BACKSPACE,
            "backspace",
        )

        event.accept()

    def _finish_input(self):
        """Classifica e regista o conteúdo atual do buffer."""

        if not self.text_buffer:
            return

        text = self.text_buffer

        # O EventProcessor decide o tipo.
        event_type = self.processor.classify_text(text)

        print(f"{event_type.value.upper()}: {text}")

        keyboard_event = KeyboardEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            key=text,
            source=self.SOURCE,
        )

        self.logger.log(keyboard_event)

        # Limpar o buffer depois de processar.
        self.text_buffer = ""

    def _log_control_event(
        self,
        event_type: EventType,
        key: str,
    ):
        """Regista uma tecla de controlo como um evento."""

        print(f"CONTROL: {key}")

        keyboard_event = KeyboardEvent(
            timestamp=datetime.now(),
            event_type=event_type,
            key=key,
            source=self.SOURCE,
        )

        self.logger.log(keyboard_event)