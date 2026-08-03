import os
import sys
import shutil
from pathlib import Path
from typing import List, Dict, Any, Optional

root_dir = Path(__file__).resolve().parent.parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QFileDialog, QMessageBox, QHeaderView,
    QFrame
)
from core.app_state import AppState
from core.naming_engine import render_filename_template
from core.logger import log_activity, logger

class DropFrame(QFrame):
    """Custom Drag & Drop Dropzone for batch file selection."""
    files_dropped = Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setObjectName("DropFrame")
        self.setStyleSheet("""
            #DropFrame {
                border: 2px dashed #334155;
                border-radius: 12px;
                background-color: #0F172A;
                padding: 24px;
            }
            #DropFrame:hover {
                border-color: #6366F1;
                background-color: rgba(99, 102, 241, 0.05);
            }
        """)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_icon = QLabel("📥")
        self.label_icon.setStyleSheet("font-size: 32px;")
        self.label_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_text = QLabel("Drag & Drop Video Files / Folders Here")
        self.label_text.setStyleSheet("font-size: 15px; font-weight: 700; color: #F8FAFC;")
        self.label_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label_sub = QLabel("Or click below to select files from your computer")
        self.label_sub.setStyleSheet("font-size: 12px; color: #94A3B8;")
        self.label_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(self.label_icon)
        layout.addWidget(self.label_text)
        layout.addWidget(self.label_sub)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        paths = [url.toLocalFile() for url in urls if url.toLocalFile()]
        if paths:
            self.files_dropped.emit(paths)


class BatchView(QWidget):
    """
    FlowMate v2.0 Pro Batch Renamer Lab
    Allows users to drag & drop existing media files, simulate new names, and batch rename them.
    """

    def __init__(self, app_state: AppState, parent=None):
        super().__init__(parent)
        self.app_state = app_state
        self.file_items: List[Dict[str, Any]] = []
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # Header Section
        header_box = QHBoxLayout()
        title_box = QVBoxLayout()
        title_box.setSpacing(4)

        header_title = QLabel("Batch Renamer Lab")
        header_title.setObjectName("HeaderTitle")

        subtitle = QLabel("Drag and drop existing files or folders to batch rename using active project rules.")
        subtitle.setStyleSheet("color: #94A3B8; font-size: 13px;")

        title_box.addWidget(header_title)
        title_box.addWidget(subtitle)

        header_box.addLayout(title_box)
        header_box.addStretch()

        # Action Buttons
        self.btn_add_files = QPushButton("📁 Add Files")
        self.btn_add_files.setObjectName("btnSecondary")
        self.btn_add_files.clicked.connect(self._browse_files)

        self.btn_clear = QPushButton("🗑️ Clear List")
        self.btn_clear.setObjectName("btnSecondary")
        self.btn_clear.clicked.connect(self._clear_list)

        self.btn_execute = QPushButton("⚡ Execute Batch Rename")
        self.btn_execute.setObjectName("btnPrimary")
        self.btn_execute.clicked.connect(self._execute_batch)

        header_box.addWidget(self.btn_add_files)
        header_box.addWidget(self.btn_clear)
        header_box.addWidget(self.btn_execute)

        layout.addLayout(header_box)

        # Dropzone Target Frame
        self.drop_frame = DropFrame()
        self.drop_frame.files_dropped.connect(self._on_files_dropped)
        layout.addWidget(self.drop_frame)

        # Simulation Table
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Original Filename", "New Simulated Filename", "Source Location", "Status"])
        
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Interactive)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 240)
        self.table.setColumnWidth(2, 220)
        self.table.setColumnWidth(3, 110)

        layout.addWidget(self.table)

    def _browse_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Files to Batch Rename", str(Path.home()),
            "Media Files (*.mp4 *.webm *.mkv *.mov *.avi *.png *.jpg *.zip);;All Files (*)"
        )
        if files:
            self._on_files_dropped(files)

    def _on_files_dropped(self, paths: List[str]):
        new_files = []
        for p in paths:
            path_obj = Path(p)
            if path_obj.is_dir():
                for sub_item in path_obj.rglob("*"):
                    if sub_item.is_file() and not sub_item.name.startswith("."):
                        new_files.append(str(sub_item))
            elif path_obj.is_file():
                new_files.append(str(path_obj))

        proj = self.app_state.active_project
        counter = proj.current_counter if proj is not None else 1
        template = getattr(proj, "name_template", "{counter}") if proj is not None else "{counter}"
        padding = proj.padding_digits if proj is not None else 3
        proj_name = proj.name if proj is not None else "Project"

        for f_path in new_files:
            if any(item["src_path"] == f_path for item in self.file_items):
                continue
            
            src_obj = Path(f_path)
            simulated_name = render_filename_template(
                template=template,
                counter=counter,
                padding_digits=padding,
                project_name=proj_name,
                original_filename=src_obj.name,
                extension=src_obj.suffix
            )
            counter += 1

            self.file_items.append({
                "src_path": f_path,
                "orig_name": src_obj.name,
                "simulated_name": simulated_name,
                "status": "Ready"
            })

        self._refresh_table()

    def _refresh_table(self):
        self.table.setUpdatesEnabled(False)
        try:
            self.table.setRowCount(len(self.file_items))
            for row, item in enumerate(self.file_items):
                item_orig = QTableWidgetItem(item["orig_name"])
                item_sim = QTableWidgetItem(item["simulated_name"])
                item_sim.setForeground(Qt.GlobalColor.green)
                item_loc = QTableWidgetItem(item["src_path"])
                item_status = QTableWidgetItem(item["status"])
                item_status.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                self.table.setItem(row, 0, item_orig)
                self.table.setItem(row, 1, item_sim)
                self.table.setItem(row, 2, item_loc)
                self.table.setItem(row, 3, item_status)
        finally:
            self.table.setUpdatesEnabled(True)

    def _clear_list(self):
        self.file_items.clear()
        self._refresh_table()

    def _execute_batch(self):
        if not self.file_items:
            QMessageBox.information(self, "Batch Empty", "Please drag and drop files to batch rename first.")
            return

        proj = self.app_state.active_project
        if proj is None:
            QMessageBox.warning(self, "No Project Active", "Please select an active project first.")
            return

        dest_dir = Path(os.path.expanduser(proj.output_dir))
        dest_dir.mkdir(parents=True, exist_ok=True)

        success_count = 0
        for item in self.file_items:
            if item["status"] == "Done":
                continue

            src = Path(item["src_path"])
            if not src.exists():
                item["status"] = "Not Found"
                continue

            target_path = dest_dir / item["simulated_name"]
            
            # Prevent accidental overwrite
            counter = proj.current_counter
            template = getattr(proj, "name_template", "{counter}")
            padding = proj.padding_digits
            
            while target_path.exists():
                counter += 1
                new_sim = render_filename_template(
                    template=template,
                    counter=counter,
                    padding_digits=padding,
                    project_name=proj.name,
                    original_filename=src.name,
                    extension=src.suffix
                )
                target_path = dest_dir / new_sim

            try:
                shutil.move(str(src), str(target_path))
                item["status"] = "Done"
                success_count += 1

                # Update stats
                proj.current_counter += 1
                proj.files_today += 1
                proj.files_total += 1
                log_activity(f"Batch Renamed: '{src.name}' -> '{target_path.name}'", level="INFO", project_name=proj.name)
            except Exception as e:
                item["status"] = "Failed"
                logger.error(f"Batch rename error for {src.name}: {e}")

        self.app_state.project_manager.save_project(proj)
        self.app_state.emit_stats()
        self._refresh_table()

        QMessageBox.information(
            self, "Batch Rename Complete",
            f"Successfully batch renamed {success_count} files into:\n{dest_dir}"
        )
