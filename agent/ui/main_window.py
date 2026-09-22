from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from agent.collector.keyboard import KeyboardCollector
from agent.models.events import EventType
from agent.ui.database_view import DatabaseView


class MainWindow(QMainWindow):
    """Main application window."""

    def __init__(self) -> None:
        super().__init__()

        self.collector = KeyboardCollector()

        self.event_count = 0
        self.word_count = 0
        self.control_count = 0
        self.character_count = 0

        self.setWindowTitle("Keyboard AI")
        self.setMinimumSize(1050, 700)

        self._build_ui()
        self._connect_signals()

        self.collector.event_created.connect(
            self._handle_event
        )

        self._update_status(True)

    # =========================================================
    # EVENT HANDLING
    # =========================================================

    def _handle_event(self, event) -> None:
        """Handle a newly created keyboard event."""

        self.event_count += 1

        if event.event_type == EventType.WORD:
            self.word_count += 1

        elif event.event_type in (
            EventType.LETTER,
            EventType.CHARACTER,
        ):
            self.character_count += 1

        elif event.event_type in (
            EventType.BACKSPACE,
            EventType.ENTER,
            EventType.SPACE,
            EventType.CTRL,
            EventType.SHIFT,
            EventType.ALT,
            EventType.TAB,
            EventType.ESCAPE,
            EventType.DELETE,
        ):
            self.control_count += 1

        timestamp = event.timestamp.strftime(
            "%Y/%m/%d %H:%M:%S"
        )

        self.add_event(
            timestamp,
            event.event_type,
            event.key,
            event.source,
        )

        self._update_counters()

        # Se a database estiver aberta, atualiza-a.
        if self.database_view is not None:
            self.database_view._load_events()

    # =========================================================
    # MAIN UI
    # =========================================================

    def _build_ui(self) -> None:
        """Build the main application interface."""

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # =====================================================
        # SIDEBAR
        # =====================================================

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(230)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(
            20,
            24,
            20,
            20,
        )
        sidebar_layout.setSpacing(8)

        app_title = QLabel("Keyboard Logger")
        app_title.setObjectName("app-title")

        app_subtitle = QLabel(
            "Local keyboard workspace"
        )
        app_subtitle.setObjectName("app-subtitle")

        sidebar_layout.addWidget(app_title)
        sidebar_layout.addWidget(app_subtitle)

        sidebar_layout.addSpacing(30)

        self.overview_button = QPushButton(
            "Overview"
        )
        self.overview_button.setObjectName(
            "nav-active"
        )

        self.live_button = QPushButton(
            "Live events"
        )
        self.live_button.setObjectName(
            "nav-button"
        )

        self.database_button = QPushButton(
            "Database"
        )
        self.database_button.setObjectName(
            "nav-button"
        )

        sidebar_layout.addWidget(
            self.overview_button
        )


        sidebar_layout.addWidget(
            self.database_button
        )

        sidebar_layout.addStretch()

        connection = QLabel(
            "●  Connected"
        )
        connection.setObjectName("connection")

        session = QLabel(
            "Local session"
        )
        session.setObjectName("session")

        sidebar_layout.addWidget(connection)
        sidebar_layout.addWidget(session)

        root.addWidget(sidebar)

        # =====================================================
        # CONTENT
        # =====================================================

        content = QWidget()
        content.setObjectName("content")

        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(
            34,
            28,
            34,
            28,
        )

        content_layout.setSpacing(0)

        root.addWidget(content)

        # =====================================================
        # STACKED VIEWS
        # =====================================================

        self.pages = QStackedWidget()

        self.overview_page = self._create_overview_page()

        self.database_view = DatabaseView()

        self.pages.addWidget(
            self.overview_page
        )

        self.pages.addWidget(
            self.database_view
        )

        content_layout.addWidget(
            self.pages
        )

        self._apply_styles()

    # =========================================================
    # OVERVIEW PAGE
    # =========================================================

    def _create_overview_page(self) -> QWidget:
        """Create the overview page."""

        page = QWidget()

        layout = QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # -----------------------------------------------------
        # Header
        # -----------------------------------------------------

        header = QHBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setSpacing(3)

        title = QLabel("Overview")
        title.setObjectName("page-title")

        subtitle = QLabel(
            "Monitor keyboard activity from this session."
        )
        subtitle.setObjectName("page-subtitle")

        title_layout.addWidget(title)
        title_layout.addWidget(subtitle)

        header.addLayout(title_layout)
        header.addStretch()

        self.status_label = QLabel(
            "● Running"
        )
        self.status_label.setObjectName(
            "status-running"
        )

        header.addWidget(
            self.status_label
        )

        layout.addLayout(header)

        # -----------------------------------------------------
        # Statistics
        # -----------------------------------------------------

        stats = QHBoxLayout()
        stats.setSpacing(12)

        self.events_value = self._create_stat(
            stats,
            "Events",
        )

        self.words_value = self._create_stat(
            stats,
            "Words",
        )

        self.characters_value = self._create_stat(
            stats,
            "Characters",
        )

        self.controls_value = self._create_stat(
            stats,
            "Controls",
        )

        layout.addLayout(stats)

        # -----------------------------------------------------
        # Live input
        # -----------------------------------------------------

        input_header = QHBoxLayout()

        input_title = QLabel(
            "Live input"
        )
        input_title.setObjectName(
            "section-title"
        )

        input_info = QLabel(
            "Events are captured only here"
        )
        input_info.setObjectName(
            "section-info"
        )

        input_header.addWidget(
            input_title
        )

        input_header.addStretch()

        input_header.addWidget(
            input_info
        )

        layout.addLayout(input_header)

        input_frame = QFrame()
        input_frame.setObjectName(
            "input-frame"
        )

        input_layout = QVBoxLayout(
            input_frame
        )

        input_layout.setContentsMargins(
            16,
            14,
            16,
            14,
        )

        input_layout.addWidget(
            self.collector
        )

        layout.addWidget(
            input_frame
        )

        # -----------------------------------------------------
        # Recent activity
        # -----------------------------------------------------

        activity_header = QHBoxLayout()

        activity_title = QLabel(
            "Recent activity"
        )
        activity_title.setObjectName(
            "section-title"
        )

        activity_header.addWidget(
            activity_title
        )

        activity_header.addStretch()

        layout.addLayout(
            activity_header
        )

        self.event_table = QTableWidget()

        self.event_table.setColumnCount(4)

        self.event_table.setHorizontalHeaderLabels(
            [
                "Time",
                "Type",
                "Key",
                "Source",
            ]
        )

        self.event_table.setEditTriggers(
            QTableWidget.NoEditTriggers
        )

        self.event_table.setSelectionBehavior(
            QTableWidget.SelectRows
        )

        self.event_table.setAlternatingRowColors(
            True
        )

        table_header = (
            self.event_table.horizontalHeader()
        )

        table_header.setSectionResizeMode(
            0,
            QHeaderView.ResizeToContents,
        )

        table_header.setSectionResizeMode(
            1,
            QHeaderView.ResizeToContents,
        )

        table_header.setSectionResizeMode(
            2,
            QHeaderView.Stretch,
        )

        table_header.setSectionResizeMode(
            3,
            QHeaderView.ResizeToContents,
        )

        layout.addWidget(
            self.event_table,
            1,
        )

        # -----------------------------------------------------
        # Bottom
        # -----------------------------------------------------

        bottom = QHBoxLayout()

        database_status = QLabel(
            "SQLite · Connected"
        )
        database_status.setObjectName(
            "database-status"
        )

        bottom.addWidget(
            database_status
        )

        bottom.addStretch()

        self.stop_button = QPushButton(
            "Stop"
        )
        self.stop_button.setObjectName(
            "secondary-button"
        )

        self.start_button = QPushButton(
            "Start"
        )
        self.start_button.setObjectName(
            "primary-button"
        )

        bottom.addWidget(
            self.stop_button
        )

        bottom.addWidget(
            self.start_button
        )

        layout.addLayout(bottom)

        return page

    # =========================================================
    # STATISTICS
    # =========================================================

    def _create_stat(
        self,
        layout: QHBoxLayout,
        title: str,
    ) -> QLabel:
        """Create a statistic card."""

        frame = QFrame()
        frame.setObjectName("stat")

        stat_layout = QVBoxLayout(frame)

        stat_layout.setContentsMargins(
            16,
            13,
            16,
            13,
        )

        stat_layout.setSpacing(2)

        title_label = QLabel(title)
        title_label.setObjectName(
            "stat-title"
        )

        value_label = QLabel("0")
        value_label.setObjectName(
            "stat-value"
        )

        stat_layout.addWidget(
            title_label
        )

        stat_layout.addWidget(
            value_label
        )

        layout.addWidget(frame)

        return value_label

    # =========================================================
    # COUNTERS
    # =========================================================

    def _update_counters(self) -> None:
        """Update session counters."""

        self.events_value.setText(
            str(self.event_count)
        )

        self.words_value.setText(
            str(self.word_count)
        )

        self.characters_value.setText(
            str(self.character_count)
        )

        self.controls_value.setText(
            str(self.control_count)
        )

    # =========================================================
    # EVENT TABLE
    # =========================================================

    def add_event(
        self,
        timestamp: str,
        event_type: EventType,
        key: str,
        source: str,
    ) -> None:
        """Add an event to the live table."""

        row = self.event_table.rowCount()

        self.event_table.insertRow(row)

        values = [
            timestamp,
            event_type.value.upper(),
            key,
            source,
        ]

        for column, value in enumerate(values):
            item = QTableWidgetItem(value)

            self.event_table.setItem(
                row,
                column,
                item,
            )

        self.event_table.scrollToBottom()

    # =========================================================
    # NAVIGATION
    # =========================================================

    def _connect_signals(self) -> None:
        """Connect interface signals."""

        self.start_button.clicked.connect(
            self._start_monitoring
        )

        self.stop_button.clicked.connect(
            self._stop_monitoring
        )

        self.overview_button.clicked.connect(
            self._show_overview
        )

        self.database_button.clicked.connect(
            self._show_database
        )

    def _show_overview(self) -> None:
        """Show overview page."""

        self.pages.setCurrentWidget(
            self.overview_page
        )

        self._set_active_button(
            self.overview_button
        )

    def _show_live_events(self) -> None:
        """Show the live events page."""

        self.pages.setCurrentWidget(
            self.overview_page
        )

        self._set_active_button(
            self.live_button
        )

    def _show_database(self) -> None:
        """Show the database page."""

        self.pages.setCurrentWidget(
            self.database_view
        )

        self.database_view._load_events()

        self._set_active_button(
            self.database_button
        )

    def _set_active_button(
        self,
        active_button: QPushButton,
    ) -> None:

        buttons = [
            self.overview_button,
            self.live_button,
            self.database_button,
        ]

        for button in buttons:
            if button is active_button:
                button.setObjectName(
                    "nav-active"
                )
            else:
                button.setObjectName(
                    "nav-button"
                )

            button.style().unpolish(button)
            button.style().polish(button)

    # =========================================================
    # MONITORING
    # =========================================================

    def _start_monitoring(self) -> None:
        """Enable the controlled input."""

        self.collector.setEnabled(True)
        self.collector.setFocus()

        self._update_status(True)

    def _stop_monitoring(self) -> None:
        """Disable the controlled input."""

        self.collector.setEnabled(False)

        self._update_status(False)

    def _update_status(
        self,
        running: bool,
    ) -> None:
        """Update monitoring status."""

        if running:
            self.status_label.setText(
                "● Running"
            )

            self.status_label.setObjectName(
                "status-running"
            )

        else:
            self.status_label.setText(
                "● Stopped"
            )

            self.status_label.setObjectName(
                "status-stopped"
            )

        self.status_label.style().unpolish(
            self.status_label
        )

        self.status_label.style().polish(
            self.status_label
        )

    # =========================================================
    # STYLES
    # =========================================================

    def _apply_styles(self) -> None:
        """Apply the application stylesheet."""

        self.setStyleSheet(
            """
            QMainWindow {
                background: #F4F1EA;
            }

            QWidget {
                font-family: "Segoe UI";
                color: #29251F;
                font-size: 13px;
            }

            /* Sidebar */

            QFrame#sidebar {
                background: #2E294E;
                border: none;
            }

            QLabel#app-title {
                color: #FFFFFF;
                font-size: 22px;
                font-weight: 700;
            }

            QLabel#app-subtitle {
                color: #B9B4D0;
                font-size: 12px;
            }

            QPushButton#nav-button,
            QPushButton#nav-active {
                text-align: left;
                padding: 11px 13px;
                border-radius: 8px;
                border: none;
                font-size: 13px;
            }

            QPushButton#nav-button {
                background: transparent;
                color: #C7C2D8;
            }

            QPushButton#nav-button:hover {
                background: #403A65;
                color: #FFFFFF;
            }

            QPushButton#nav-active {
                background: #5B5485;
                color: #FFFFFF;
                font-weight: 600;
            }

            QLabel#connection {
                color: #A8D5BA;
                font-size: 12px;
                font-weight: 600;
            }

            QLabel#session {
                color: #9993B2;
                font-size: 11px;
            }

            /* Page */

            QLabel#page-title {
                font-size: 28px;
                font-weight: 650;
                color: #29251F;
            }

            QLabel#page-subtitle {
                color: #827D73;
                font-size: 13px;
            }

            QLabel#status-running {
                background: #E3F1E7;
                color: #39734D;
                padding: 8px 13px;
                border-radius: 15px;
                font-weight: 600;
            }

            QLabel#status-stopped {
                background: #F1E5E3;
                color: #8A4B45;
                padding: 8px 13px;
                border-radius: 15px;
                font-weight: 600;
            }

            /* Statistics */

            QFrame#stat {
                background: #FFFFFF;
                border: 1px solid #E5E0D7;
                border-radius: 10px;
            }

            QLabel#stat-title {
                color: #8A857B;
                font-size: 11px;
            }

            QLabel#stat-value {
                color: #342E48;
                font-size: 24px;
                font-weight: 650;
            }

            /* Sections */

            QLabel#section-title {
                color: #403A35;
                font-size: 14px;
                font-weight: 650;
            }

            QLabel#section-info {
                color: #9A958C;
                font-size: 11px;
            }

            /* Input */

            QFrame#input-frame {
                background: #FFFFFF;
                border: 1px solid #DDD8CE;
                border-radius: 12px;
            }

            QTextEdit {
                background: #FFFFFF;
                color: #29251F;
                border: none;
                font-size: 15px;
                padding: 8px;
                selection-background-color: #D9D2F2;
            }

            /* Tables */

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

            /* Buttons */

            QPushButton#primary-button,
            QPushButton#secondary-button {
                padding: 9px 18px;
                border-radius: 7px;
                font-weight: 600;
            }

            QPushButton#primary-button {
                background: #665C9F;
                color: #FFFFFF;
                border: 1px solid #5B518F;
            }

            QPushButton#primary-button:hover {
                background: #756BAE;
            }

            QPushButton#secondary-button {
                background: #FFFFFF;
                color: #514C45;
                border: 1px solid #D7D1C7;
            }

            QPushButton#secondary-button:hover {
                background: #F1EEE8;
            }

            QLabel#database-status {
                color: #777168;
                font-size: 11px;
            }
            """
        )