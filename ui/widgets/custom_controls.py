import os
import sys
import subprocess
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PySide6.QtCore import Signal, QUrl
from PySide6.QtGui import QDesktopServices

class PathPickerRow(QWidget):
    """Path selection row containing label, input box, Browse button, and Open Folder button."""

    path_changed = Signal(str)

    def __init__(self, title: str, placeholder: str = "Select directory path...", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)

        self.label = QLabel(title)
        self.label.setStyleSheet("font-weight: 700; color: #94A3B8;")
        layout.addWidget(self.label)

        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(8)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText(placeholder)
        self.line_edit.textChanged.connect(self.path_changed.emit)

        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.setObjectName("btnSecondary")
        self.browse_btn.clicked.connect(self._on_browse)

        self.open_btn = QPushButton("Open Folder")
        self.open_btn.setObjectName("btnSecondary")
        self.open_btn.clicked.connect(self._on_open_folder)

        controls_layout.addWidget(self.line_edit, stretch=1)
        controls_layout.addWidget(self.browse_btn)
        controls_layout.addWidget(self.open_btn)

        layout.addLayout(controls_layout)

    def get_path(self) -> str:
        return self.line_edit.text().strip()

    def set_path(self, path: str):
        self.line_edit.setText(path)

    def _on_browse(self):
        current_path = os.path.expanduser(self.get_path() or str(Path.home()))
        folder = QFileDialog.getExistingDirectory(self, f"Select {self.label.text()}", current_path)
        if folder:
            self.set_path(folder)

    def _on_open_folder(self):
        raw_path = self.get_path()
        if not raw_path:
            QMessageBox.warning(self, "Invalid Directory", "Please select or enter a directory path.")
            return

        expanded_path = os.path.expanduser(raw_path)

        if not os.path.exists(expanded_path):
            reply = QMessageBox.question(
                self, "Directory Missing",
                f"Directory does not exist:\n{expanded_path}\n\nWould you like to create it now?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                try:
                    os.makedirs(expanded_path, exist_ok=True)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Failed to create directory: {e}")
                    return
            else:
                return

        try:
            QDesktopServices.openUrl(QUrl.fromLocalFile(expanded_path))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to open directory: {e}")

class StatusBadge(QLabel):
    """Pill badge showing Watching or Stopped status."""

    def __init__(self, is_watching: bool = False, parent=None):
        super().__init__(parent)
        self.set_status(is_watching)

    def set_status(self, is_watching: bool):
        if is_watching:
            self.setText("● WATCHING")
            self.setObjectName("StatusBadgeWatching")
        else:
            self.setText("● STOPPED")
            self.setObjectName("StatusBadgeStopped")
        self.setStyle(self.style())
