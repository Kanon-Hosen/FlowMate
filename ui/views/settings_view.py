import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QComboBox,
    QPushButton, QFrame, QMessageBox, QFormLayout
)
from PySide6.QtCore import Signal
from core.app_state import AppState

class SettingsView(QWidget):
    """Global Application Settings View."""

    theme_changed = Signal(str)

    def __init__(self, app_state: AppState, parent=None):
        super().__init__(parent)
        self.app_state = app_state
        self.init_ui()
        self.load_settings()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        title_label = QLabel("Settings")
        title_label.setObjectName("HeaderTitle")

        subtitle_label = QLabel("Configure application preferences and behavior")
        subtitle_label.setStyleSheet("color: #64748B; font-size: 13px;")

        title_box.addWidget(title_label)
        title_box.addWidget(subtitle_label)

        header_layout.addLayout(title_box)
        header_layout.addStretch()

        main_layout.addLayout(header_layout)

        # Settings Form Card
        card = QFrame()
        card.setProperty("class", "CardWidget")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(24, 24, 24, 24)
        card_layout.setSpacing(20)

        sec_title = QLabel("APPEARANCE & SYSTEM PREFERENCES")
        sec_title.setObjectName("SectionTitle")
        card_layout.addWidget(sec_title)

        form_layout = QFormLayout()
        form_layout.setSpacing(16)

        # Theme Selector
        self.theme_combo = QComboBox()
        self.theme_combo.addItem("Dark Theme (Default)", "dark")
        self.theme_combo.addItem("Light Theme", "light")
        self.theme_combo.currentIndexChanged.connect(self._on_theme_changed)
        form_layout.addRow("Application Theme:", self.theme_combo)

        # Auto-start watcher
        self.autostart_cb = QCheckBox("Automatically start folder watching when FlowMate launches")
        self.autostart_cb.toggled.connect(lambda v: self.app_state.settings_manager.set("auto_start_watcher", v))
        form_layout.addRow("Auto Watcher:", self.autostart_cb)

        # Desktop Notifications
        self.notify_cb = QCheckBox("Show Linux desktop notifications when files are renamed & moved")
        self.notify_cb.toggled.connect(lambda v: self.app_state.settings_manager.set("enable_desktop_notifications", v))
        form_layout.addRow("Notifications:", self.notify_cb)

        # Minimize to Tray
        self.tray_cb = QCheckBox("Minimize application to system tray on window close")
        self.tray_cb.toggled.connect(lambda v: self.app_state.settings_manager.set("minimize_to_tray", v))
        form_layout.addRow("System Tray:", self.tray_cb)

        card_layout.addLayout(form_layout)
        main_layout.addWidget(card)

        main_layout.addStretch()

    def load_settings(self):
        settings = self.app_state.settings_manager
        
        theme = settings.get("theme", "dark")
        idx = self.theme_combo.findData(theme)
        if idx >= 0:
            self.theme_combo.setCurrentIndex(idx)

        self.autostart_cb.setChecked(settings.get("auto_start_watcher", False))
        self.notify_cb.setChecked(settings.get("enable_desktop_notifications", True))
        self.tray_cb.setChecked(settings.get("minimize_to_tray", True))

    def _on_theme_changed(self, index: int):
        theme_key = self.theme_combo.itemData(index)
        if theme_key:
            self.app_state.settings_manager.set("theme", theme_key)
            self.theme_changed.emit(theme_key)
