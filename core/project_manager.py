import os
import sys
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from core.logger import logger

PROJECTS_DIR = Path(__file__).parent.parent / "projects"
PROJECTS_DIR.mkdir(exist_ok=True, parents=True)

class Project:
    """Dataclass wrapper for a FlowMate project."""

    def __init__(
        self,
        project_id: str,
        name: str,
        watch_dir: str,
        output_dir: str,
        current_counter: int = 1,
        padding_digits: int = 3,
        file_extensions: Optional[List[str]] = None,
        description: str = "",
        name_template: str = "{counter}",
        min_file_size_mb: float = 0.0,
        files_today: int = 0,
        files_total: int = 0,
        last_active_date: Optional[str] = None,
        created_at: Optional[str] = None
    ):
        self.id = project_id
        self.name = name
        self.description = description
        self.watch_dir = watch_dir
        self.output_dir = output_dir
        self.current_counter = current_counter
        self.padding_digits = padding_digits
        self.file_extensions = file_extensions or [".mp4", ".webm", ".mkv", ".mov", ".avi"]
        self.name_template = name_template
        self.min_file_size_mb = min_file_size_mb
        self.files_today = files_today
        self.files_total = files_total
        self.last_active_date = last_active_date or datetime.now().strftime("%Y-%m-%d")
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "watch_dir": self.watch_dir,
            "output_dir": self.output_dir,
            "current_counter": self.current_counter,
            "padding_digits": self.padding_digits,
            "file_extensions": self.file_extensions,
            "name_template": self.name_template,
            "min_file_size_mb": self.min_file_size_mb,
            "files_today": self.files_today,
            "files_total": self.files_total,
            "last_active_date": self.last_active_date,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Project':
        return cls(
            project_id=data.get("id", "default"),
            name=data.get("name", "Untitled Project"),
            watch_dir=data.get("watch_dir", ""),
            output_dir=data.get("output_dir", ""),
            current_counter=data.get("current_counter", 1),
            padding_digits=data.get("padding_digits", 3),
            file_extensions=data.get("file_extensions", [".mp4", ".webm", ".mkv", ".mov", ".avi"]),
            description=data.get("description", ""),
            name_template=data.get("name_template", "{counter}"),
            min_file_size_mb=data.get("min_file_size_mb", 0.0),
            files_today=data.get("files_today", 0),
            files_total=data.get("files_total", 0),
            last_active_date=data.get("last_active_date", None),
            created_at=data.get("created_at", None)
        )

class ProjectManager:
    """Manages creation, loading, switching, and scanning of FlowMate projects."""

    def __init__(self, projects_dir: Path = PROJECTS_DIR):
        self.projects_dir = projects_dir
        self.projects: Dict[str, Project] = {}
        self.load_all_projects()

    def load_all_projects(self) -> Dict[str, Project]:
        """Loads all project JSON files from projects directory."""
        self.projects.clear()
        json_files = list(self.projects_dir.glob("*.json"))

        if not json_files:
            default_proj = Project(
                project_id="default",
                name="Default Project",
                watch_dir=str(Path.home() / "Downloads"),
                output_dir=str(Path.home() / "Videos" / "ClipPilot_Output"),
                current_counter=1,
                padding_digits=3
            )
            self.save_project(default_proj)
            self.projects["default"] = default_proj
            return self.projects

        for filepath in json_files:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    proj = Project.from_dict(data)
                    self.projects[proj.id] = proj
            except Exception as e:
                logger.error(f"Failed to load project file {filepath.name}: {e}")

        return self.projects

    def get_project(self, project_id: str) -> Optional[Project]:
        """Returns project instance by ID."""
        if project_id not in self.projects:
            self.load_all_projects()
        return self.projects.get(project_id)

    def save_project(self, project: Project) -> bool:
        """Persists a project instance to disk."""
        try:
            target_path = self.projects_dir / f"{project.id}.json"
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(project.to_dict(), f, indent=2)
            self.projects[project.id] = project
            logger.info(f"Saved project: {project.name} (ID: {project.id})")
            return True
        except Exception as e:
            logger.error(f"Failed to save project {project.id}: {e}")
            return False

    def create_project(self, name: str, watch_dir: str, output_dir: str, padding_digits: int = 3, start_counter: int = 1, description: str = "", name_template: str = "{counter}", min_file_size_mb: float = 0.0) -> Project:
        """Creates and saves a new project."""
        project_id = re.sub(r'[^a-z0-9_-]', '_', name.lower().strip()) or f"proj_{int(datetime.now().timestamp())}"
        
        base_id = project_id
        count = 1
        while (self.projects_dir / f"{project_id}.json").exists():
            project_id = f"{base_id}_{count}"
            count += 1

        new_proj = Project(
            project_id=project_id,
            name=name,
            watch_dir=watch_dir,
            output_dir=output_dir,
            current_counter=start_counter,
            padding_digits=padding_digits,
            description=description,
            name_template=name_template,
            min_file_size_mb=min_file_size_mb
        )

        self.detect_and_update_counter(new_proj)
        self.save_project(new_proj)
        return new_proj

    def delete_project(self, project_id: str) -> bool:
        """Deletes project file from disk."""
        if project_id == "default":
            logger.warning("Cannot delete default project.")
            return False
        
        filepath = self.projects_dir / f"{project_id}.json"
        try:
            if filepath.exists():
                filepath.unlink()
            if project_id in self.projects:
                del self.projects[project_id]
            logger.info(f"Deleted project: {project_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting project {project_id}: {e}")
            return False

    def detect_and_update_counter(self, project: Project) -> int:
        """
        Scans project's output folder for existing numbered files (e.g. 001.mp4, 002.mp4).
        Finds the highest existing counter and sets current_counter to highest + 1.
        """
        expanded = os.path.expanduser(project.output_dir)
        output_path = Path(expanded)
        if not output_path.exists() or not output_path.is_dir():
            logger.info(f"Output folder {project.output_dir} does not exist yet. Keeping counter = {project.current_counter}")
            return project.current_counter

        highest_num = 0
        number_pattern = re.compile(r'^(\d+)\.[a-zA-Z0-9]+$')

        try:
            for item in output_path.iterdir():
                if item.is_file():
                    match = number_pattern.match(item.name)
                    if match:
                        try:
                            num = int(match.group(1))
                            if num > highest_num:
                                highest_num = num
                        except ValueError:
                            pass
        except Exception as e:
            logger.error(f"Error scanning output folder {output_path}: {e}")

        if highest_num > 0:
            next_counter = highest_num + 1
            project.current_counter = next_counter
            self.save_project(project)
            logger.info(f"Smart counter updated for '{project.name}': highest found {highest_num:0{project.padding_digits}d}, next counter set to {next_counter}")
        else:
            logger.info(f"No numbered files found in output folder. Starting from counter {project.current_counter}")

        return project.current_counter
