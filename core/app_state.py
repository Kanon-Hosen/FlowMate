import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from typing import Optional
from PySide6.QtCore import QObject, Signal
from core.settings import SettingsManager
from core.project_manager import ProjectManager, Project
from core.renamer import FileRenamer

class AppState(QObject):
    """
    Central Application State holding managers, active project, and emitting global signals.
    """
    active_project_changed = Signal(Project)
    stats_updated = Signal(dict)
    watcher_status_changed = Signal(bool, str) # (is_watching, watch_dir)

    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager()
        self.project_manager = ProjectManager()
        self.renamer = FileRenamer(self.project_manager)

        active_id = self.settings_manager.get("active_project_id", "default")
        self.active_project: Project = self.project_manager.get_project(active_id) or self.project_manager.get_project("default")
        
        self.is_watching: bool = False

    def set_active_project(self, project_id: str) -> Optional[Project]:
        """Switches active project and notifies listeners."""
        project = self.project_manager.get_project(project_id)
        if project:
            self.active_project = project
            self.settings_manager.set("active_project_id", project.id)
            # Smart scan output folder when switching project
            self.project_manager.detect_and_update_counter(project)
            self.active_project_changed.emit(project)
            self.emit_stats()
            return project
        return None

    def emit_stats(self):
        """Emits current active project statistics."""
        if self.active_project:
            self.stats_updated.emit({
                "files_today": self.active_project.files_today,
                "files_total": self.active_project.files_total,
                "current_counter": self.active_project.current_counter,
                "padding_digits": self.active_project.padding_digits
            })
