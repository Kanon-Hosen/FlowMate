from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QLineEdit, QComboBox, QCheckBox, QGroupBox, QFrame
)
from PySide6.QtCore import Signal, Qt

class PathSelectorWidget(QWidget):
    """Custom widget for selecting directories with input and browse button."""

    path_changed = Signal(str)

    def __init__(self, label_text: str, placeholder: str = "Select a folder...", parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QLabel(label_text)
        self.label.setStyleSheet("font-weight: bold; color: #94A3B8;")
        layout.addWidget(self.label)

        input_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setPlaceholderText(placeholder)
        self.path_input.textChanged.connect(self.path_changed.emit)

        self.browse_btn = QPushButton("Browse...")
        input_layout.addWidget(self.path_input)
        input_layout.addWidget(self.browse_btn)

        layout.addLayout(input_layout)

    def get_path(self) -> str:
        return self.path_input.text().strip()

    def set_path(self, path: str):
        self.path_input.setText(path)

class RuleItemWidget(QGroupBox):
    """Widget representing a single rename rule configuration."""

    rule_updated = Signal()

    def __init__(self, rule_data: dict, parent=None):
        super().__init__(rule_data.get("name", "Rename Rule"), parent)
        self.rule_id = rule_data.get("id", "rule-1")
        
        layout = QVBoxLayout(self)

        # Active Checkbox
        self.enable_cb = QCheckBox("Enable Rule")
        self.enable_cb.setChecked(rule_data.get("enabled", True))
        layout.addWidget(self.enable_cb)

        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Extensions Filter (e.g. .jpg, .png):"))
        self.ext_input = QLineEdit(rule_data.get("extension_filter", ""))
        filter_layout.addWidget(self.ext_input)
        layout.addLayout(filter_layout)

        # Prefix & Suffix
        presuf_layout = QHBoxLayout()
        presuf_layout.addWidget(QLabel("Prefix:"))
        self.prefix_input = QLineEdit(rule_data.get("prefix", ""))
        presuf_layout.addWidget(self.prefix_input)

        presuf_layout.addWidget(QLabel("Suffix:"))
        self.suffix_input = QLineEdit(rule_data.get("suffix", ""))
        presuf_layout.addWidget(self.suffix_input)
        layout.addLayout(presuf_layout)

        # Case Transformation
        case_layout = QHBoxLayout()
        case_layout.addWidget(QLabel("Letter Case:"))
        self.case_combo = QComboBox()
        self.case_combo.addItems(["none", "lowercase", "uppercase", "titlecase"])
        self.case_combo.setCurrentText(rule_data.get("case_transform", "none"))
        case_layout.addWidget(self.case_combo)

        # Space replacement
        case_layout.addWidget(QLabel("Replace Spaces With:"))
        self.space_input = QLineEdit(rule_data.get("replace_spaces_with", "_"))
        case_layout.addWidget(self.space_input)
        layout.addLayout(case_layout)

    def get_data(self) -> dict:
        return {
            "id": self.rule_id,
            "name": self.title(),
            "enabled": self.enable_cb.isChecked(),
            "extension_filter": self.ext_input.text().strip(),
            "prefix": self.prefix_input.text(),
            "suffix": self.suffix_input.text(),
            "replace_spaces_with": self.space_input.text(),
            "case_transform": self.case_combo.currentText()
        }
