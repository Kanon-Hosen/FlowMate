import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QDialog, QLineEdit, QSpinBox, QComboBox,
    QMessageBox, QFrame, QFormLayout
)
from PySide6.QtCore import Signal, Qt
from core.app_state import AppState
from typing import Optional
from core.project_manager import Project
from ui.widgets.custom_controls import PathPickerRow

class CreateProjectDialog(QDialog):
    """Modal dialog for creating or editing a FlowMate Project."""

    def __init__(self, parent=None, project: Optional[Project] = None):
        super().__init__(parent)
        self.project = project
        self.setWindowTitle("Edit Project" if project else "Create New Project")
        self.setMinimumWidth(550)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(16)

        form_layout = QFormLayout()
        form_layout.setSpacing(12)

        self.name_input = QLineEdit(project.name if project else "")
        self.name_input.setPlaceholderText("e.g. YouTube Downloads Project")
        form_layout.addRow("Project Name:", self.name_input)

        self.desc_input = QLineEdit(project.description if project else "")
        self.desc_input.setPlaceholderText("Optional description...")
        form_layout.addRow("Description:", self.desc_input)

        self.watch_picker = PathPickerRow("Watch Folder:", "Select folder to monitor...")
        if project:
            self.watch_picker.set_path(project.watch_dir)
        else:
            self.watch_picker.set_path(str(Path.home() / "Downloads"))
        form_layout.addRow(self.watch_picker)

        self.output_picker = PathPickerRow("Output Folder:", "Select destination folder...")
        if project:
            self.output_picker.set_path(project.output_dir)
        else:
            self.output_picker.set_path(str(Path.home() / "Videos" / "FlowMate_Output"))
        form_layout.addRow(self.output_picker)

        self.start_counter_spin = QSpinBox()
        self.start_counter_spin.setRange(1, 999999)
        self.start_counter_spin.setValue(project.current_counter if project else 1)
        form_layout.addRow("Starting Counter:", self.start_counter_spin)

        self.padding_combo = QComboBox()
        self.padding_combo.addItem("3 Digits (001.mp4)", 3)
        self.padding_combo.addItem("4 Digits (0001.mp4)", 4)
        self.padding_combo.addItem("5 Digits (00001.mp4)", 5)
        if project:
            idx = self.padding_combo.findData(project.padding_digits)
            if idx >= 0:
                self.padding_combo.setCurrentIndex(idx)
        form_layout.addRow("Padding Format:", self.padding_combo)

        layout.addLayout(form_layout)

        # Dialog Buttons
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()

        cancel_btn = QPushButton("Cancel")
        cancel_btn.setObjectName("btnSecondary")
        cancel_btn.clicked.connect(self.reject)

        save_btn = QPushButton("Save Project")
        save_btn.setObjectName("btnPrimary")
        save_btn.clicked.connect(self.accept)

        btn_layout.addWidget(cancel_btn)
        btn_layout.addWidget(save_btn)

        layout.addLayout(btn_layout)

    def get_data(self) -> dict:
        return {
            "name": self.name_input.text().strip(),
            "description": self.desc_input.text().strip(),
            "watch_dir": self.watch_picker.get_path(),
            "output_dir": self.output_picker.get_path(),
            "start_counter": self.start_counter_spin.value(),
            "padding_digits": self.padding_combo.currentData()
        }

class ProjectsView(QWidget):
    """Projects View for managing multiple project workspaces."""

    project_selected = Signal(str)

    def __init__(self, app_state: AppState, parent=None):
        super().__init__(parent)
        self.app_state = app_state
        self.init_ui()
        self.app_state.active_project_changed.connect(lambda p: self.refresh_projects())

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setSpacing(20)

        # Header
        header_layout = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(2)

        title_label = QLabel("Projects")
        title_label.setObjectName("HeaderTitle")

        subtitle_label = QLabel("Manage your automated download project workspaces")
        subtitle_label.setStyleSheet("color: #64748B; font-size: 13px;")

        title_box.addWidget(title_label)
        title_box.addWidget(subtitle_label)

        header_layout.addLayout(title_box)
        header_layout.addStretch()

        new_project_btn = QPushButton("+ New Project")
        new_project_btn.setObjectName("btnPrimary")
        new_project_btn.clicked.connect(self._on_new_project)
        header_layout.addWidget(new_project_btn)

        main_layout.addLayout(header_layout)

        # Projects Table Card
        table_card = QFrame()
        table_card.setProperty("class", "CardWidget")
        table_layout = QVBoxLayout(table_card)
        table_layout.setContentsMargins(20, 20, 20, 20)

        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels([
            "Status", "Project Name", "Watch Folder", "Output Folder", "Counter", "Actions"
        ])
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)

        table_layout.addWidget(self.table)
        main_layout.addWidget(table_card)

        self.refresh_projects()

    def refresh_projects(self):
        projects = self.app_state.project_manager.load_all_projects()
        active_proj = self.app_state.active_project

        self.table.setRowCount(0)
        for proj_id, proj in projects.items():
            row = self.table.rowCount()
            self.table.insertRow(row)

            is_active = (proj_id == active_proj.id)
            status_item = QTableWidgetItem("★ Active" if is_active else "Inactive")
            if is_active:
                status_item.setForeground(Qt.GlobalColor.cyan)

            name_item = QTableWidgetItem(proj.name)
            watch_item = QTableWidgetItem(proj.watch_dir)
            output_item = QTableWidgetItem(proj.output_dir)
            
            formatted_counter = f"{proj.current_counter:0{proj.padding_digits}d}"
            counter_item = QTableWidgetItem(formatted_counter)

            self.table.setItem(row, 0, status_item)
            self.table.setItem(row, 1, name_item)
            self.table.setItem(row, 2, watch_item)
            self.table.setItem(row, 3, output_item)
            self.table.setItem(row, 4, counter_item)

            # Action Buttons Cell
            action_widget = QWidget()
            action_layout = QHBoxLayout(action_widget)
            action_layout.setContentsMargins(4, 2, 4, 2)
            action_layout.setSpacing(6)

            switch_btn = QPushButton("Select" if not is_active else "Current")
            switch_btn.setObjectName("btnSecondary" if not is_active else "btnPrimary")
            switch_btn.setEnabled(not is_active)
            switch_btn.clicked.connect(lambda _, pid=proj_id: self._on_switch_project(pid))

            edit_btn = QPushButton("Edit")
            edit_btn.setObjectName("btnSecondary")
            edit_btn.clicked.connect(lambda _, p=proj: self._on_edit_project(p))

            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("btnDanger")
            delete_btn.setEnabled(proj_id != "default")
            delete_btn.clicked.connect(lambda _, pid=proj_id: self._on_delete_project(pid))

            action_layout.addWidget(switch_btn)
            action_layout.addWidget(edit_btn)
            action_layout.addWidget(delete_btn)

            self.table.setCellWidget(row, 5, action_widget)

    def _on_new_project(self):
        dialog = CreateProjectDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            if not data["name"]:
                QMessageBox.warning(self, "Invalid Input", "Project Name is required.")
                return

            proj = self.app_state.project_manager.create_project(
                name=data["name"],
                watch_dir=data["watch_dir"],
                output_dir=data["output_dir"],
                padding_digits=data["padding_digits"],
                start_counter=data["start_counter"],
                description=data["description"]
            )
            self.app_state.set_active_project(proj.id)
            self.refresh_projects()

    def _on_edit_project(self, project: Project):
        dialog = CreateProjectDialog(self, project=project)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            project.name = data["name"]
            project.description = data["description"]
            project.watch_dir = data["watch_dir"]
            project.output_dir = data["output_dir"]
            project.current_counter = data["start_counter"]
            project.padding_digits = data["padding_digits"]
            
            self.app_state.project_manager.save_project(project)
            if self.app_state.active_project.id == project.id:
                self.app_state.active_project_changed.emit(project)
            self.refresh_projects()

    def _on_switch_project(self, project_id: str):
        self.app_state.set_active_project(project_id)
        self.refresh_projects()

    def _on_delete_project(self, project_id: str):
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete project '{project_id}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.app_state.project_manager.delete_project(project_id)
            if self.app_state.active_project.id == project_id:
                self.app_state.set_active_project("default")
            self.refresh_projects()
