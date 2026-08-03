import csv
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit,
    QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QFileDialog, QFrame, QMessageBox
)
from PySide6.QtCore import Qt
from core.logger import log_bridge, LOG_FILE

class LogsView(QWidget):
    """Activity Log View with search, filter, and CSV/TXT export capabilities."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.log_data = []
        self.init_ui()
        self.connect_signals()
        self.load_log_file()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        title_label = QLabel("Activity Logs")
        title_label.setObjectName("HeaderTitle")

        subtitle_label = QLabel("Inspect automated download renaming activity and errors")
        subtitle_label.setStyleSheet("color: #64748B; font-size: 13px;")

        title_box.addWidget(title_label)
        title_box.addWidget(subtitle_label)

        header_layout.addLayout(title_box)
        header_layout.addStretch()

        export_btn = QPushButton("Export Logs...")
        export_btn.setObjectName("btnSecondary")
        export_btn.clicked.connect(self._on_export_logs)

        clear_btn = QPushButton("Clear View")
        clear_btn.setObjectName("btnSecondary")
        clear_btn.clicked.connect(self._on_clear_logs)

        header_layout.addWidget(export_btn)
        header_layout.addWidget(clear_btn)

        main_layout.addLayout(header_layout)

        # Filter & Search Bar
        filter_card = QFrame()
        filter_card.setProperty("class", "CardWidget")
        filter_layout = QHBoxLayout(filter_card)
        filter_layout.setContentsMargins(16, 12, 16, 12)
        filter_layout.setSpacing(16)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search logs by filename, message, or project...")
        self.search_input.textChanged.connect(self._filter_table)
        filter_layout.addWidget(self.search_input, stretch=1)

        self.level_combo = QComboBox()
        self.level_combo.addItems(["All Levels", "INFO", "WARNING", "ERROR"])
        self.level_combo.currentIndexChanged.connect(self._filter_table)
        filter_layout.addWidget(self.level_combo)

        main_layout.addWidget(filter_card)

        # Logs Table
        table_card = QFrame()
        table_card.setProperty("class", "CardWidget")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(16, 16, 16, 16)

        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels(["Timestamp", "Level", "Project", "Original File", "Renamed File / Details"])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.Stretch)

        table_layout.addWidget(self.table)
        main_layout.addWidget(table_card)

    def connect_signals(self):
        log_bridge.log_record_emitted.connect(self.append_log_data)

    def load_log_file(self):
        """Loads historical log lines from logs/flowmate.log if available."""
        if not LOG_FILE.exists():
            return

        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines[-200:]: # load last 200 lines
                    self.append_log_data({
                        "timestamp": line[1:20] if len(line) > 20 else "",
                        "level": "INFO" if "INFO" in line else ("ERROR" if "ERROR" in line else "DEBUG"),
                        "message": line.strip(),
                        "original_file": "-",
                        "new_file": "-",
                        "project_name": "General"
                    })
        except Exception:
            pass

    def append_log_data(self, record: dict):
        self.log_data.append(record)
        self._add_row_to_table(record)

    def _add_row_to_table(self, record: dict):
        # Apply current search filter
        query = self.search_input.text().lower()
        level_filter = self.level_combo.currentText()

        if level_filter != "All Levels" and record["level"] != level_filter:
            return

        if query:
            full_str = f"{record['timestamp']} {record['level']} {record['project_name']} {record['original_file']} {record['new_file']} {record['message']}".lower()
            if query not in full_str:
                return

        row = self.table.rowCount()
        self.table.insertRow(row)

        item_ts = QTableWidgetItem(record.get("timestamp", ""))
        item_lvl = QTableWidgetItem(record.get("level", "INFO"))
        item_proj = QTableWidgetItem(record.get("project_name", "General"))
        item_orig = QTableWidgetItem(record.get("original_file", "-"))
        
        detail_text = record.get("new_file", "-")
        if detail_text == "-":
            detail_text = record.get("message", "")
        item_new = QTableWidgetItem(detail_text)

        if record.get("level") == "ERROR":
            item_lvl.setForeground(Qt.GlobalColor.red)
        elif record.get("level") == "WARNING":
            item_lvl.setForeground(Qt.GlobalColor.yellow)
        else:
            item_lvl.setForeground(Qt.GlobalColor.green)

        self.table.setItem(row, 0, item_ts)
        self.table.setItem(row, 1, item_lvl)
        self.table.setItem(row, 2, item_proj)
        self.table.setItem(row, 3, item_orig)
        self.table.setItem(row, 4, item_new)

    def _filter_table(self):
        self.table.setRowCount(0)
        for rec in self.log_data:
            self._add_row_to_table(rec)

    def _on_clear_logs(self):
        self.log_data.clear()
        self.table.setRowCount(0)

    def _on_export_logs(self):
        filepath, _ = QFileDialog.getSaveFileName(self, "Export Activity Log", "flowmate_logs.csv", "CSV Files (*.csv);;Text Files (*.txt)")
        if not filepath:
            return

        try:
            if filepath.endswith(".csv"):
                with open(filepath, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["Timestamp", "Level", "Project", "Original File", "New File / Message"])
                    for rec in self.log_data:
                        writer.writerow([
                            rec.get("timestamp"),
                            rec.get("level"),
                            rec.get("project_name"),
                            rec.get("original_file"),
                            rec.get("new_file") if rec.get("new_file") != "-" else rec.get("message")
                        ])
            else:
                with open(filepath, "w", encoding="utf-8") as f:
                    for rec in self.log_data:
                        f.write(f"[{rec.get('timestamp')}] [{rec.get('level')}] [{rec.get('project_name')}]: {rec.get('message')}\n")

            QMessageBox.information(self, "Export Successful", f"Logs exported successfully to:\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Export Failed", f"Failed to export logs: {e}")
