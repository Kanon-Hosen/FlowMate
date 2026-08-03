import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
from PySide6.QtCore import Qt

class StatCard(QFrame):
    """Modern Statistic Metric Display Card."""

    def __init__(self, title: str, initial_value: str = "0", parent=None):
        super().__init__(parent)
        self.setObjectName("StatCard")
        self.setMinimumHeight(100)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 16, 18, 16)
        layout.setSpacing(6)

        self.label_title = QLabel(title)
        self.label_title.setObjectName("StatLabel")

        self.label_value = QLabel(str(initial_value))
        self.label_value.setObjectName("StatValue")

        layout.addWidget(self.label_title)
        layout.addWidget(self.label_value)
        layout.addStretch()

    def set_value(self, value: str):
        """Updates displayed value."""
        self.label_value.setText(str(value))
