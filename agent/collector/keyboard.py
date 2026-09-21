from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from agent.models.events import KeyboardEvent
from agent.storage.event_logger import EventLogger


class KeyboardCollector(QWidget):
    """Collects keyboard input inside the controlled window."""

    SOURCE = "controlled-input-window"

    def __init__(self):
        super().__init__()

        self.text_buffer = ""
        self.logger = EventLogger()

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
            self._finish_input(event)
            return

        key = event.text()

        # Space
        if key == " ":
            self._finish_input(event)
            return

        # Letra
        if key and key.isalpha():
            self._handle_character(key)

        event.accept()

    def _handle_character(self, key):
        """Adiciona a letra ao buffer, sem a classificar ainda."""

        self.text_buffer += key

        print(f"CARÁCTER: {key}")
        print(f"BUFFER: {self.text_buffer}")

    def _handle_backspace(self, event):
        """Remove a última letra."""

        print("BACKSPACE utilizado")

        if self.text_buffer:
            self.text_buffer = self.text_buffer[:-1]

        print(f"BUFFER: {self.text_buffer}")

        event.accept()

    def _finish_input(self, event):
        """Classifica o buffer quando aparece Space ou Enter."""

        if not self.text_buffer:
            event.accept()
            return

        text = self.text_buffer

        # Uma única letra = LETTER
        if len(text) == 1:

            print(f"LETTER: {text}")

            letter_event = KeyboardEvent(
                timestamp=datetime.now(),
                event_type="letter",
                key=text,
                source=self.SOURCE,
            )

            self.logger.log(letter_event)

        # Duas ou mais letras = WORD
        else:

            print(f"WORD: {text}")

            word_event = KeyboardEvent(
                timestamp=datetime.now(),
                event_type="word",
                key=text,
                source=self.SOURCE,
            )

            self.logger.log(word_event)

        # Limpar depois de classificar
        self.text_buffer = ""

        event.accept()