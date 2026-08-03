import os
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QStackedWidget, QSystemTrayIcon,
    QMenu, QMessageBox, QApplication, QStyle
)
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QIcon, QPixmap, QAction, QKeySequence, QShortcut, QDesktopServices

from core.app_state import AppState
from core.watcher import WatcherThread
from core.project_manager import Project
from core.logger import logger, log_activity
from ui.styles import DARK_THEME, LIGHT_THEME
from ui.widgets.sidebar import Sidebar
from ui.views.dashboard_view import DashboardView
from ui.views.projects_view import ProjectsView
from ui.views.batch_view import BatchView
from ui.views.logs_view import LogsView
from ui.views.settings_view import SettingsView

ASSETS_DIR = Path(__file__).parent.parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"

class MainWindow(QMainWindow):
    """Production Main Application Window for FlowMate."""

    def __init__(self):
        super().__init__()
        self.app_state = AppState()
        self.watcher_thread = None

        self.setWindowTitle("ClipPilot - Automated Video & File Pilot")
        
        # Load Window Dimensions
        width = self.app_state.settings_manager.get("window_width", 1200)
        height = self.app_state.settings_manager.get("window_height", 800)
        self.resize(width, height)
        self.setMinimumSize(950, 650)

        # Apply Saved Theme
        self.apply_theme(self.app_state.settings_manager.get("theme", "dark"))

        self.init_ui()
        self.init_system_tray()
        self.init_keyboard_shortcuts()
        self.connect_signals()

        # Auto-start watcher if enabled in settings
        if self.app_state.settings_manager.get("auto_start_watcher", False):
            self.start_watching()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Sidebar
        self.sidebar = Sidebar()
        main_layout.addWidget(self.sidebar)

        # Stacked Views Container
        self.stacked_widget = QStackedWidget()
        
        self.dashboard_view = DashboardView(self.app_state)
        self.projects_view = ProjectsView(self.app_state)
        self.batch_view = BatchView(self.app_state)
        self.logs_view = LogsView()
        self.settings_view = SettingsView(self.app_state)

        self.stacked_widget.addWidget(self.dashboard_view)
        self.stacked_widget.addWidget(self.projects_view)
        self.stacked_widget.addWidget(self.batch_view)
        self.stacked_widget.addWidget(self.logs_view)
        self.stacked_widget.addWidget(self.settings_view)

        main_layout.addWidget(self.stacked_widget, stretch=1)

        # Populate projects in sidebar
        self.update_sidebar_projects()

    def update_sidebar_projects(self):
        projects = list(self.app_state.project_manager.load_all_projects().values())
        self.sidebar.set_projects(projects, self.app_state.active_project.id)

    def init_system_tray(self):
        """Initializes Linux system tray icon & notification menu."""
        self.tray_icon = QSystemTrayIcon(self)

        if LOGO_PATH.exists():
            self.tray_icon.setIcon(QIcon(str(LOGO_PATH)))
            self.setWindowIcon(QIcon(str(LOGO_PATH)))
        else:
            # Fallback Qt standard icon
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)
            self.tray_icon.setIcon(icon)
            self.setWindowIcon(icon)

        tray_menu = QMenu()
        
        show_action = QAction("Show FlowMate", self)
        show_action.triggered.connect(self.show_normal_window)
        tray_menu.addAction(show_action)

        tray_menu.addSeparator()

        self.toggle_watch_action = QAction("Start Watching", self)
        self.toggle_watch_action.triggered.connect(self.toggle_watching)
        tray_menu.addAction(self.toggle_watch_action)

        tray_menu.addSeparator()

        exit_action = QAction("Exit FlowMate", self)
        exit_action.triggered.connect(self.quit_app)
        tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.activated.connect(self._on_tray_activated)
        self.tray_icon.show()

    def init_keyboard_shortcuts(self):
        """Sets up application keyboard shortcuts."""
        # Ctrl+S / Ctrl+T: Toggle Watcher
        sc_toggle = QShortcut(QKeySequence("Ctrl+S"), self)
        sc_toggle.activated.connect(self.toggle_watching)

        # Ctrl+O: Open Output Folder
        sc_open_out = QShortcut(QKeySequence("Ctrl+O"), self)
        sc_open_out.activated.connect(self.open_output_folder)

        # Ctrl+W: Open Watch Folder
        sc_open_watch = QShortcut(QKeySequence("Ctrl+W"), self)
        sc_open_watch.activated.connect(self.open_watch_folder)

        # Ctrl+L: View Logs
        sc_logs = QShortcut(QKeySequence("Ctrl+L"), self)
        sc_logs.activated.connect(lambda: self.sidebar.set_active_nav(2))

    def connect_signals(self):
        # Navigation
        self.sidebar.nav_changed.connect(self.stacked_widget.setCurrentIndex)
        self.sidebar.project_switched.connect(self._on_project_switched)

        # Dashboard View Requests
        self.dashboard_view.start_watcher_requested.connect(self.start_watching)
        self.dashboard_view.stop_watcher_requested.connect(self.stop_watching)
        self.dashboard_view.reset_counter_requested.connect(self.reset_counter)
        self.dashboard_view.scan_folder_requested.connect(self.scan_output_folder)
        self.dashboard_view.save_project_requested.connect(self.save_current_project)

        # Sync sidebar projects list when projects change
        self.app_state.active_project_changed.connect(lambda _: self.update_sidebar_projects())

        # Settings
        self.settings_view.theme_changed.connect(self.apply_theme)

    def apply_theme(self, theme_key: str):
        if theme_key == "light":
            self.setStyleSheet(LIGHT_THEME)
        else:
            self.setStyleSheet(DARK_THEME)

    def _on_project_switched(self, project_id: str):
        if self.app_state.is_watching:
            self.stop_watching()
        self.app_state.set_active_project(project_id)

    def save_current_project(self):
        proj = self.app_state.active_project
        if proj is not None:
            self.app_state.project_manager.save_project(proj)

    def start_watching(self):
        proj = self.app_state.active_project
        watch_path = proj.watch_dir

        if not watch_path:
            QMessageBox.warning(self, "Invalid Watch Folder", "Watch folder path is empty. Please select a valid directory.")
            return

        expanded = os.path.expanduser(watch_path)
        if not os.path.exists(expanded):
            try:
                os.makedirs(expanded, exist_ok=True)
            except Exception as e:
                QMessageBox.warning(self, "Invalid Watch Folder", f"Watch folder does not exist and could not be created:\n{expanded}\nError: {e}")
                return

        if self.watcher_thread and self.watcher_thread.isRunning():
            self.stop_watching()

        self.watcher_thread = WatcherThread(expanded, parent=self)
        self.watcher_thread.file_detected_signal.connect(self.on_file_downloaded)
        self.watcher_thread.error_signal.connect(self.on_watcher_error)
        self.watcher_thread.started_signal.connect(self._on_watcher_started)
        self.watcher_thread.stopped_signal.connect(self._on_watcher_stopped)
        
        self.watcher_thread.start()

    def stop_watching(self):
        if self.watcher_thread and self.watcher_thread.isRunning():
            self.watcher_thread.stop()
            self.watcher_thread = None

    def _on_watcher_started(self, watch_dir: str):
        self.app_state.is_watching = True
        self.app_state.watcher_status_changed.emit(True, watch_dir)
        self.toggle_watch_action.setText("Stop Watching")
        log_activity(f"Started monitoring folder: {watch_dir}", level="INFO", project_name=self.app_state.active_project.name)

    def _on_watcher_stopped(self):
        self.app_state.is_watching = False
        self.app_state.watcher_status_changed.emit(False, "")
        self.toggle_watch_action.setText("Start Watching")
        log_activity("Stopped monitoring directory.", level="INFO", project_name=self.app_state.active_project.name)

    def on_watcher_error(self, err_msg: str):
        QMessageBox.critical(self, "Watcher Error", err_msg)
        self.stop_watching()

    def on_file_downloaded(self, file_path: str):
        """Called when WatcherThread detects a newly completed download file."""
        proj = self.app_state.active_project
        result = self.app_state.renamer.process_downloaded_file(file_path, proj)

        if result:
            orig_name = result["original_name"]
            new_name = result["new_name"]
            ts = result["timestamp"]

            # Update Dashboard activity table
            self.dashboard_view.add_activity_log(ts, orig_name, new_name, status="SUCCESS")

            # Update stats UI
            self.app_state.emit_stats()

            # Desktop Notification if enabled
            if self.app_state.settings_manager.get("enable_desktop_notifications", True) and QSystemTrayIcon.isSystemTrayAvailable():
                self.tray_icon.showMessage(
                    "FlowMate File Renamed",
                    f"Renamed: {orig_name}\n→ {new_name}",
                    QSystemTrayIcon.MessageIcon.Information,
                    3000
                )

    def scan_output_folder(self):
        proj = self.app_state.active_project
        if proj is not None:
            counter = self.app_state.project_manager.detect_and_update_counter(proj)
            self.app_state.emit_stats()
            QMessageBox.information(
                self, "Smart Scan Complete",
                f"Output folder scanned successfully.\nNext counter set to: {counter:0{proj.padding_digits}d}"
            )

    def reset_counter(self):
        proj = self.app_state.active_project
        if proj is not None:
            proj.current_counter = 1
            self.app_state.project_manager.save_project(proj)
            self.app_state.emit_stats()
            log_activity("Counter reset to 1 by user.", level="INFO", project_name=proj.name)

    def open_watch_folder(self):
        path = os.path.expanduser(self.app_state.active_project.watch_dir)
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def open_output_folder(self):
        path = os.path.expanduser(self.app_state.active_project.output_dir)
        if path and os.path.exists(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def show_normal_window(self):
        self.showNormal()
        self.activateWindow()

    def toggle_watching(self):
        if self.app_state.is_watching:
            self.stop_watching()
        else:
            self.start_watching()

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            if self.isVisible():
                self.hide()
            else:
                self.show_normal_window()

    def closeEvent(self, event):
        if self.app_state.settings_manager.get("minimize_to_tray", True) and QSystemTrayIcon.isSystemTrayAvailable():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "FlowMate running in background",
                "FlowMate is still watching your downloads folder in the system tray.",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )
        else:
            self.quit_app()

    def quit_app(self):
        self.stop_watching()
        self.app_state.settings_manager.set("window_width", self.width())
        self.app_state.settings_manager.set("window_height", self.height())
        QApplication.quit()
