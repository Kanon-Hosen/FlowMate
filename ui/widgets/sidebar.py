import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from PySide6.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QButtonGroup, QComboBox
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPixmap, QFont

ASSETS_DIR = Path(__file__).parent.parent.parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"

class Sidebar(QFrame):
    """Modern Left Navigation Sidebar for FlowMate."""

    nav_changed = Signal(int) # index: 0=Dashboard, 1=Projects, 2=Settings, 3=Logs
    project_switched = Signal(str) # project_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Sidebar")
        self.setFixedWidth(240)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(16, 24, 16, 24)
        layout.setSpacing(12)

        # App Brand Header
        header_layout = QHBoxLayout()
        header_layout.setSpacing(12)

        self.logo_label = QLabel()
        if LOGO_PATH.exists():
            pixmap = QPixmap(str(LOGO_PATH)).scaled(40, 40, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.logo_label.setPixmap(pixmap)
        else:
            self.logo_label.setText("⚡")
            self.logo_label.setStyleSheet("font-size: 24px;")

        title_box = QVBoxLayout()
        title_box.setSpacing(2)
        app_name = QLabel("FlowMate")
        app_name.setFont(QFont("Segoe UI", 16, QFont.Bold))
        app_name.setStyleSheet("color: #F8FAFC;")

        app_subtitle = QLabel("Auto Renamer")
        app_subtitle.setStyleSheet("color: #64748B; font-size: 11px;")

        title_box.addWidget(app_name)
        title_box.addWidget(app_subtitle)

        header_layout.addWidget(self.logo_label)
        header_layout.addLayout(title_box)
        header_layout.addStretch()

        layout.addLayout(header_layout)
        layout.addSpacing(16)

        # Quick Project Selector Card
        proj_label = QLabel("ACTIVE PROJECT")
        proj_label.setStyleSheet("font-size: 10px; font-weight: 700; color: #64748B; letter-spacing: 0.5px;")
        layout.addWidget(proj_label)

        self.project_combo = QComboBox()
        self.project_combo.currentIndexChanged.connect(self._on_project_combo_changed)
        layout.addWidget(self.project_combo)

        layout.addSpacing(20)

        # Navigation Buttons
        nav_label = QLabel("NAVIGATION")
        nav_label.setStyleSheet("font-size: 10px; font-weight: 700; color: #64748B; letter-spacing: 0.5px;")
        layout.addWidget(nav_label)

        self.btn_group = QButtonGroup(self)
        self.btn_group.setExclusive(True)

        nav_items = [
            (" Dashboard", 0),
            (" Projects", 1),
            (" Logs & Activity", 2),
            (" Settings", 3)
        ]

        self.buttons = []
        for text, index in nav_items:
            btn = QPushButton(text)
            btn.setObjectName("SidebarNavButton")
            btn.setCheckable(True)
            self.btn_group.addButton(btn, index)
            layout.addWidget(btn)
            self.buttons.append(btn)

        self.buttons[0].setChecked(True)
        self.btn_group.idClicked.connect(self.nav_changed.emit)

        layout.addStretch()

        # Footer
        footer_label = QLabel("FlowMate v1.0.0 Pro")
        footer_label.setStyleSheet("color: #475569; font-size: 11px; text-align: center;")
        footer_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer_label)

    def set_projects(self, projects: list, active_project_id: str):
        """Populates projects combobox."""
        self.project_combo.blockSignals(True)
        self.project_combo.clear()
        
        active_idx = 0
        for idx, proj in enumerate(projects):
            self.project_combo.addItem(proj.name, proj.id)
            if proj.id == active_project_id:
                active_idx = idx

        self.project_combo.setCurrentIndex(active_idx)
        self.project_combo.blockSignals(False)

    def _on_project_combo_changed(self, index: int):
        project_id = self.project_combo.itemData(index)
        if project_id:
            self.project_switched.emit(project_id)

    def set_active_nav(self, index: int):
        if 0 <= index < len(self.buttons):
            self.buttons[index].setChecked(True)
