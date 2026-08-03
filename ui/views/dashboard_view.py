import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSpinBox,
    QComboBox, QFrame, QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Signal, Qt
from core.app_state import AppState
from core.project_manager import Project
from ui.widgets.stat_card import StatCard
from ui.widgets.custom_controls import PathPickerRow, StatusBadge

class DashboardView(QWidget):
    """Main Dashboard View for monitoring downloads, counters, and activity."""

    start_watcher_requested = Signal()
    stop_watcher_requested = Signal()
    reset_counter_requested = Signal()
    scan_folder_requested = Signal()
    save_project_requested = Signal()

    def __init__(self, app_state: AppState, parent=None):
        super().__init__(parent)
        self.app_state = app_state
        self.init_ui()
        self.connect_signals()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Header Bar
        header_layout = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        self.title_label = QLabel("Dashboard")
        self.title_label.setObjectName("HeaderTitle")

        self.subtitle_label = QLabel("Active Project: Default Project")
        self.subtitle_label.setStyleSheet("color: #64748B; font-size: 13px;")

        title_box.addWidget(self.title_label)
        title_box.addWidget(self.subtitle_label)

        header_layout.addLayout(title_box)
        header_layout.addStretch()

        self.status_badge = StatusBadge(is_watching=False)
        header_layout.addWidget(self.status_badge)

        self.toggle_watch_btn = QPushButton("Start Watching")
        self.toggle_watch_btn.setObjectName("btnPrimary")
        self.toggle_watch_btn.setMinimumHeight(38)
        self.toggle_watch_btn.setMinimumWidth(150)
        self.toggle_watch_btn.clicked.connect(self._on_toggle_watch)
        header_layout.addWidget(self.toggle_watch_btn)

        main_layout.addLayout(header_layout)

        # Stats Metrics Row
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(16)

        self.card_counter = StatCard("Current Counter", "001")
        self.card_today = StatCard("Files Today", "0")
        self.card_total = StatCard("Files Total", "0")

        stats_layout.addWidget(self.card_counter)
        stats_layout.addWidget(self.card_today)
        stats_layout.addWidget(self.card_total)

        main_layout.addLayout(stats_layout)

        # Main Configuration Card
        config_card = QFrame()
        config_card.setProperty("class", "CardWidget")
        config_layout = QVBoxLayout(config_card)
        config_layout.setContentsMargins(20, 20, 20, 20)
        config_layout.setSpacing(16)

        config_title = QLabel("PROJECT & FOLDER CONFIGURATION")
        config_title.setObjectName("SectionTitle")
        config_layout.addWidget(config_title)

        # Path Selectors
        self.watch_picker = PathPickerRow("Watch Folder (Chrome Downloads)", "Select folder to monitor...")
        self.watch_picker.path_changed.connect(self._on_path_changed)
        config_layout.addWidget(self.watch_picker)

        self.output_picker = PathPickerRow("Output Folder (Destination Project Directory)", "Select destination folder...")
        self.output_picker.path_changed.connect(self._on_path_changed)
        config_layout.addWidget(self.output_picker)

        # Counter Controls
        counter_row = QHBoxLayout()
        counter_row.setSpacing(20)

        # Starting Number Input
        spin_box_layout = QVBoxLayout()
        spin_label = QLabel("Current / Starting Counter:")
        spin_label.setStyleSheet("font-weight: 700; color: #94A3B8;")
        self.counter_spinbox = QSpinBox()
        self.counter_spinbox.setRange(1, 999999)
        self.counter_spinbox.setValue(1)
        self.counter_spinbox.valueChanged.connect(self._on_counter_spinbox_changed)
        spin_box_layout.addWidget(spin_label)
        spin_box_layout.addWidget(self.counter_spinbox)
        counter_row.addLayout(spin_box_layout)

        # Padding Digits Selector
        digits_layout = QVBoxLayout()
        digits_label = QLabel("Padding Digits Format:")
        digits_label.setStyleSheet("font-weight: 700; color: #94A3B8;")
        self.digits_combo = QComboBox()
        self.digits_combo.addItem("3 Digits (001.mp4)", 3)
        self.digits_combo.addItem("4 Digits (0001.mp4)", 4)
        self.digits_combo.addItem("5 Digits (00001.mp4)", 5)
        self.digits_combo.currentIndexChanged.connect(self._on_digits_changed)
        digits_layout.addWidget(digits_label)
        digits_layout.addWidget(self.digits_combo)
        counter_row.addLayout(digits_layout)

        # Actions Buttons (Reset Counter & Smart Scan Output)
        action_btns_layout = QVBoxLayout()
        action_label = QLabel("Smart Actions:")
        action_label.setStyleSheet("font-weight: 700; color: #94A3B8;")
        
        btns_row = QHBoxLayout()
        self.scan_btn = QPushButton("Scan Output Folder")
        self.scan_btn.setObjectName("btnSecondary")
        self.scan_btn.clicked.connect(self._on_scan_clicked)

        self.reset_btn = QPushButton("Reset Counter")
        self.reset_btn.setObjectName("btnSecondary")
        self.reset_btn.clicked.connect(self._on_reset_clicked)

        btns_row.addWidget(self.scan_btn)
        btns_row.addWidget(self.reset_btn)

        action_btns_layout.addWidget(action_label)
        action_btns_layout.addLayout(btns_row)
        counter_row.addLayout(action_btns_layout)

        config_layout.addLayout(counter_row)
        main_layout.addWidget(config_card)

        # Recent Renamed Activity Log Table
        activity_card = QFrame()
        activity_card.setProperty("class", "CardWidget")
        activity_layout = QVBoxLayout(activity_card)
        activity_layout.setContentsMargins(20, 20, 20, 20)
        activity_layout.setSpacing(12)

        activity_header = QHBoxLayout()
        activity_title = QLabel("RECENT RENAMED ACTIVITY")
        activity_title.setObjectName("SectionTitle")
        activity_header.addWidget(activity_title)
        activity_header.addStretch()

        activity_layout.addLayout(activity_header)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Time", "Original Filename", "New Filename", "Status"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeToContents)
        activity_layout.addWidget(self.table)

        main_layout.addWidget(activity_card)

    def connect_signals(self):
        self.app_state.active_project_changed.connect(self.update_project_ui)
        self.app_state.stats_updated.connect(self.update_stats_ui)
        self.app_state.watcher_status_changed.connect(self.update_watcher_status)

    def update_project_ui(self, project: Project):
        self.subtitle_label.setText(f"Active Project: {project.name}")
        self.watch_picker.set_path(project.watch_dir)
        self.output_picker.set_path(project.output_dir)
        self.counter_spinbox.setValue(project.current_counter)
        
        index = self.digits_combo.findData(project.padding_digits)
        if index >= 0:
            self.digits_combo.setCurrentIndex(index)

        formatted_val = f"{project.current_counter:0{project.padding_digits}d}"
        self.card_counter.set_value(formatted_val)
        self.card_today.set_value(project.files_today)
        self.card_total.set_value(project.files_total)

    def update_stats_ui(self, stats: dict):
        counter = stats.get("current_counter", 1)
        padding = stats.get("padding_digits", 3)
        self.counter_spinbox.blockSignals(True)
        self.counter_spinbox.setValue(counter)
        self.counter_spinbox.blockSignals(False)

        self.card_counter.set_value(f"{counter:0{padding}d}")
        self.card_today.set_value(stats.get("files_today", 0))
        self.card_total.set_value(stats.get("files_total", 0))

    def update_watcher_status(self, is_watching: bool, watch_dir: str):
        self.status_badge.set_status(is_watching)
        if is_watching:
            self.toggle_watch_btn.setText("Stop Watching")
            self.toggle_watch_btn.setObjectName("btnDanger")
        else:
            self.toggle_watch_btn.setText("Start Watching")
            self.toggle_watch_btn.setObjectName("btnPrimary")
        self.toggle_watch_btn.setStyle(self.toggle_watch_btn.style())

    def add_activity_log(self, time_str: str, original_file: str, new_file: str, status: str = "SUCCESS"):
        row = self.table.rowCount()
        self.table.insertRow(row)

        item_time = QTableWidgetItem(time_str)
        item_orig = QTableWidgetItem(original_file)
        item_new = QTableWidgetItem(new_file)
        item_status = QTableWidgetItem(status)

        if status == "SUCCESS":
            item_status.setForeground(Qt.GlobalColor.green)
        else:
            item_status.setForeground(Qt.GlobalColor.red)

        self.table.setItem(row, 0, item_time)
        self.table.setItem(row, 1, item_orig)
        self.table.setItem(row, 2, item_new)
        self.table.setItem(row, 3, item_status)

        self.table.scrollToBottom()

    def _on_toggle_watch(self):
        if self.app_state.is_watching:
            self.stop_watcher_requested.emit()
        else:
            self.start_watcher_requested.emit()

    def _on_path_changed(self, text: str):
        proj = self.app_state.active_project
        if proj:
            proj.watch_dir = self.watch_picker.get_path()
            proj.output_dir = self.output_picker.get_path()
            self.save_project_requested.emit()

    def _on_counter_spinbox_changed(self, val: int):
        proj = self.app_state.active_project
        if proj:
            proj.current_counter = val
            self.card_counter.set_value(f"{val:0{proj.padding_digits}d}")
            self.save_project_requested.emit()

    def _on_digits_changed(self, index: int):
        padding = self.digits_combo.itemData(index)
        proj = self.app_state.active_project
        if proj and padding:
            proj.padding_digits = padding
            self.card_counter.set_value(f"{proj.current_counter:0{padding}d}")
            self.save_project_requested.emit()

    def _on_scan_clicked(self):
        self.scan_folder_requested.emit()

    def _on_reset_clicked(self):
        reply = QMessageBox.question(
            self, "Reset Counter",
            "Are you sure you want to reset the file counter back to 1?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.reset_counter_requested.emit()
