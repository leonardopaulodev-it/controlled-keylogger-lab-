import sys

from PySide6.QtWidgets import QApplication

from agent.collector.keyboard import KeyboardCollector


def main():
    app = QApplication(sys.argv)

    window = KeyboardCollector()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()