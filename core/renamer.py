import os
import shutil
import sys
import time
from datetime import datetime
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from typing import Optional, Dict, Any
from core.logger import logger, log_activity
from core.project_manager import Project, ProjectManager
from core.naming_engine import render_filename_template

IGNORED_EXTENSIONS = {".crdownload", ".tmp", ".part", ".download"}

class FileRenamer:
    """Core file renaming and relocation engine for FlowMate."""

    def __init__(self, project_manager: ProjectManager):
        self.project_manager = project_manager

    @staticmethod
    def is_file_locked_or_incomplete(file_path: Path, wait_timeout: float = 12.0) -> bool:
        """
        Ensures Google Chrome or the OS has finished downloading/writing the file.
        Verifies file extension, size stabilization, and OS write handle release.
        """
        if file_path.suffix.lower() in IGNORED_EXTENSIONS:
            return True

        if not file_path.exists():
            return True

        start_time = time.time()
        last_size = -1
        poll_interval = 0.05  # Adaptive micro-poll (50ms)

        while time.time() - start_time < wait_timeout:
            try:
                if not file_path.exists():
                    return True

                current_size = file_path.stat().st_size
                if current_size > 0 and current_size == last_size:
                    # Test if OS write lock is released
                    try:
                        with open(file_path, "rb+") as f:
                            pass
                        return False
                    except (PermissionError, OSError):
                        pass

                last_size = current_size
                time.sleep(poll_interval)
                poll_interval = min(0.3, poll_interval * 1.3)  # Gentle ramp-up up to 300ms max
            except Exception:
                time.sleep(0.1)

        return True

    def process_downloaded_file(self, file_path_str: str, project: Project) -> Optional[Dict[str, Any]]:
        """
        Processes a newly detected download file:
        1. Checks extension & Chrome completion.
        2. Generates sequential filename (e.g., 001.mp4).
        3. Moves file to output directory safely without overwriting.
        4. Increments project counter and saves state.
        """
        expanded_src = os.path.expanduser(file_path_str)
        src_path = Path(expanded_src)

        # 1. Skip temporary / incomplete download files
        if src_path.suffix.lower() in IGNORED_EXTENSIONS:
            logger.debug(f"Ignoring temporary download file: {src_path.name}")
            return None

        # 2. Extension filter check if configured
        if project.file_extensions and "*" not in project.file_extensions:
            valid_exts = [e.lower() if e.startswith(".") else f".{e.lower()}" for e in project.file_extensions]
            if src_path.suffix.lower() not in valid_exts:
                logger.info(f"Skipping '{src_path.name}' - extension '{src_path.suffix}' not in allowed list {valid_exts}")
                return None

        # 3. Wait for file write stabilization & lock release
        if self.is_file_locked_or_incomplete(src_path):
            logger.warning(f"File '{src_path.name}' is locked or incomplete. Skipping.")
            return None

        # 3.5 Check Minimum File Size Filter
        if getattr(project, "min_file_size_mb", 0.0) > 0.0:
            file_size_mb = src_path.stat().st_size / (1024 * 1024)
            if file_size_mb < project.min_file_size_mb:
                logger.info(f"Skipping '{src_path.name}' ({file_size_mb:.2f} MB) - smaller than minimum threshold ({project.min_file_size_mb} MB)")
                return None

        # 4. Prepare Destination Folder
        expanded_dest = os.path.expanduser(project.output_dir)
        dest_dir = Path(expanded_dest)
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            err_msg = f"Permission error or failed to create output directory {project.output_dir}: {e}"
            logger.error(err_msg)
            log_activity(err_msg, level="ERROR", original_file=src_path.name, project_name=project.name)
            return None

        # 5. Generate unique dynamic filename from template
        ext = src_path.suffix
        counter = project.current_counter
        padding = project.padding_digits
        template = getattr(project, "name_template", "{counter}")

        formatted_name = render_filename_template(
            template=template,
            counter=counter,
            padding_digits=padding,
            project_name=project.name,
            original_filename=src_path.name,
            extension=ext
        )
        dest_path = dest_dir / formatted_name

        # Prevent overwrite by advancing counter if target already exists
        while dest_path.exists():
            logger.info(f"Target file {dest_path.name} already exists. Advancing counter from {counter} to {counter + 1}")
            counter += 1
            formatted_name = render_filename_template(
                template=template,
                counter=counter,
                padding_digits=padding,
                project_name=project.name,
                original_filename=src_path.name,
                extension=ext
            )
            dest_path = dest_dir / formatted_name

        # 6. Execute File Transfer (Move)
        try:
            shutil.move(str(src_path), str(dest_path))
            
            # Check Daily Stats Reset
            today_str = datetime.now().strftime("%Y-%m-%d")
            if getattr(project, "last_active_date", None) != today_str:
                project.files_today = 0
                project.last_active_date = today_str

            # Update Project Counter & Stats
            project.current_counter = counter + 1
            project.files_today += 1
            project.files_total += 1
            self.project_manager.save_project(project)

            original_name = src_path.name
            new_name = dest_path.name

            msg = f"Successfully renamed & moved: '{original_name}' -> '{new_name}'"
            log_activity(msg, level="INFO", original_file=original_name, new_file=new_name, project_name=project.name)

            return {
                "status": "success",
                "original_path": str(src_path),
                "original_name": original_name,
                "new_path": str(dest_path),
                "new_name": new_name,
                "counter_used": counter,
                "next_counter": project.current_counter,
                "project_id": project.id,
                "project_name": project.name,
                "timestamp": time.strftime("%H:%M:%S")
            }

        except Exception as e:
            err_msg = f"Failed to move file '{src_path.name}': {e}"
            logger.error(err_msg)
            log_activity(err_msg, level="ERROR", original_file=src_path.name, project_name=project.name)
            return None
