from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from agent.storage.event_repository import EventRepository


class DatabaseView(QWidget):
    """Interface for browsing the events database."""

    def __init__(self) -> None:
        super().__init__()

        self.repository = EventRepository()

        self._build_ui()
        self._load_events()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def _build_ui(self) -> None:
        """Build the database interface."""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(18)

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(3)

        title = QLabel("Database")
        title.setObjectName("database-title")

        subtitle = QLabel(
            "Browse and search stored keyboard events."
        )
        subtitle.setObjectName("database-subtitle")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header.addLayout(title_layout)
        header.addStretch()

        self.count_label = QLabel("0 events")
        self.count_label.setObjectName("database-count")

        header.addWidget(self.count_label)

        layout.addLayout(header)

        # -----------------------------------------------------
        # Search bar
        # -----------------------------------------------------

        search_frame = QFrame()
        search_frame.setObjectName("database-search")

        search_layout = QHBoxLayout(search_frame)
        search_layout.setContentsMargins(
            12, 10, 12, 10
        )
        search_layout.setSpacing(10)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(
            "Search events..."
        )

        self.type_filter = QComboBox()

        self.type_filter.addItems(
            [
                "All types",
                "letter",
                "word",
                "character",
                "backspace",
                "enter",
                "space",
                "ctrl",
                "shift",
                "alt",
                "tab",
                "escape",
                "delete",
                "unknown",
            ]
        )

        self.refresh_button = QPushButton(
            "Refresh"
        )
        self.refresh_button.setObjectName(
            "database-refresh"
        )

        search_layout.addWidget(
            self.search_input,
            1,
        )

        search_layout.addWidget(
            self.type_filter
        )

        search_layout.addWidget(
            self.refresh_button
        )

        layout.addWidget(search_frame)

        # -----------------------------------------------------
        # Table
        # -----------------------------------------------------

        self.table = QTableWidget()

        self.table.setColumnCount(5)

        self.table.setHorizontalHeaderLabels(
            [
                "ID",
                "Time",
                "Type",
                "Key",
                "Source",
            ]
        )

        self.table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.table.setAlternatingRowColors(
            True
        )

        self.table.setSortingEnabled(True)

        header = self.table.horizontalHeader()

        header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            2,
            QHeaderView.ResizeToContents,
        )

        header.setSectionResizeMode(
            3,
            QHeaderView.Stretch,
        )

        header.setSectionResizeMode(
            4,
            QHeaderView.ResizeToContents,
        )

        layout.addWidget(
            self.table,
            1,
        )

        # -----------------------------------------------------
        # Bottom
        # -----------------------------------------------------

        bottom = QHBoxLayout()

        self.result_label = QLabel(
            "Showing latest events"
        )
        self.result_label.setObjectName(
            "database-result"
        )

        bottom.addWidget(
            self.result_label
        )

        bottom.addStretch()

        layout.addLayout(bottom)

        # -----------------------------------------------------
        # Signals
        # -----------------------------------------------------

        self.search_input.textChanged.connect(
            self._load_events
        )

        self.type_filter.currentTextChanged.connect(
            self._load_events
        )

        self.refresh_button.clicked.connect(
            self._load_events
        )

        self._apply_styles()

    # ---------------------------------------------------------
    # Database
    # ---------------------------------------------------------

    def _load_events(self) -> None:
        """Load events from the database."""

        search_text = (
            self.search_input.text().strip()
        )

        selected_type = (
            self.type_filter.currentText()
        )

        event_type = ""

        if selected_type != "All types":
            event_type = selected_type

        events = self.repository.search_events(
            search_text=search_text,
            event_type=event_type,
            limit=500,
        )

        self.table.setSortingEnabled(False)
        self.table.setRowCount(0)

        for event in events:
            row = self.table.rowCount()

            self.table.insertRow(row)

            values = [
                str(event[0]),
                event[1],
                event[2].upper(),
                event[3],
                event[4],
            ]

            for column, value in enumerate(values):
                item = QTableWidgetItem(value)

                if column == 0:
                    item.setTextAlignment(
                        Qt.AlignCenter
                    )

                self.table.setItem(
                    row,
                    column,
                    item,
                )

        self.table.setSortingEnabled(True)

        total = self.repository.count_events()

        self.count_label.setText(
            f"{total:,} events"
        )

        self.result_label.setText(
            f"Showing {len(events):,} results"
        )

    # ---------------------------------------------------------
    # Styles
    # ---------------------------------------------------------

    def _apply_styles(self) -> None:
        """Apply database view styles."""

        self.setStyleSheet(
            """
            QLabel#database-title {
                color: #29251F;
                font-size: 28px;
                font-weight: 650;
            }

            QLabel#database-subtitle {
                color: #827D73;
                font-size: 13px;
            }

            QLabel#database-count {
                background: #E9E4F6;
                color: #5B518F;
                padding: 8px 13px;
                border-radius: 14px;
                font-weight: 600;
            }

            QFrame#database-search {
                background: #FFFFFF;
                border: 1px solid #DDD8CE;
                border-radius: 10px;
            }

            QLineEdit {
                background: #FAF9F6;
                color: #29251F;
                border: 1px solid #E1DCD2;
                border-radius: 7px;
                padding: 8px 10px;
            }

            QLineEdit:focus {
                border: 1px solid #9A8CC7;
            }

            QComboBox {
                background: #FAF9F6;
                color: #514C45;
                border: 1px solid #E1DCD2;
                border-radius: 7px;
                padding: 8px 10px;
                min-width: 110px;
            }

            QPushButton#database-refresh {
                background: #665C9F;
                color: #FFFFFF;
                border: none;
                border-radius: 7px;
                padding: 9px 16px;
                font-weight: 600;
            }

            QPushButton#database-refresh:hover {
                background: #756BAE;
            }

            QTableWidget {
                background: #FFFFFF;
                alternate-background-color: #FAF8F4;
                border: 1px solid #E1DCD2;
                border-radius: 10px;
                gridline-color: #EEEAE2;
                selection-background-color: #E6E0F4;
                selection-color: #29251F;
            }

            QHeaderView::section {
                background: #F0ECE5;
                color: #777168;
                border: none;
                border-bottom: 1px solid #DDD8CE;
                padding: 9px;
                font-size: 11px;
                font-weight: 600;
            }

            QLabel#database-result {
                color: #8A857B;
                font-size: 11px;
            }
            """
        )