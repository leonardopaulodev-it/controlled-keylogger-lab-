from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from agent.models.events import KeyboardEvent
from agent.storage.event_logger import EventLogger


class KeyboardCollector(QWidget):
    def __init__(self):
        super().__init__()

        self.text_buffer = ""

        self.setWindowTitle("Controlled Keyboard Lab")
        self.setMinimumSize(600, 400)
        self.setFocusPolicy(Qt.StrongFocus)

        self.logger = EventLogger()

    def keyPressEvent(self, event):
        # Backspace
        if event.key() == Qt.Key_Backspace :
            print("BACKSPACE")

            keyboard_event = KeyboardEvent(
                timestamp=datetime.now(),
                event_type="key_press",
                key="Backspace",
                source="controlled-input-window"
            )

            self.logger.log(keyboard_event)
            
        
        if event.key() == Qt.Key_Return:
            print("ENTER")
            

            keyboard_event = KeyboardEvent(
                timestamp=datetime.now(),
                event_type="key_press",
                key="ENTER",
                source="controlled-input-window"
            )

            self.logger.log(keyboard_event)

            event.accept()
            return

        key = event.text()

        # Espaço = terminou uma palavra
        if key == " ":
            if self.text_buffer:
                print(f"WORD: {self.text_buffer}")

                word_event = KeyboardEvent(
                    timestamp=datetime.now(),
                    event_type="word",
                    key=self.text_buffer,
                    source="controlled-input-window"
                )

                self.logger.log(word_event)

                self.text_buffer = ""

        # Letras ficam apenas no buffer
        elif key:
            self.text_buffer += key
            print(f"BUFFER: {self.text_buffer}")

        event.accept()