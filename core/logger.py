import logging
import os
import sys
from datetime import datetime
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from typing import List, Dict, Any, Optional
from PySide6.QtCore import QObject, Signal

LOG_DIR = Path(__file__).parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True, parents=True)
LOG_FILE = LOG_DIR / "flowmate.log"

class LogSignalBridge(QObject):
    """Bridge for emitting log records across Qt threads safely."""
    log_record_emitted = Signal(dict)

# Global bridge instance
log_bridge = LogSignalBridge()

class QtSignalLogHandler(logging.Handler):
    """Custom logging handler emitting formatted dicts to Qt LogSignalBridge."""

    def emit(self, record: logging.LogRecord) -> None:
        try:
            log_data = {
                "timestamp": datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S"),
                "level": record.levelname,
                "message": record.getMessage(),
                "original_file": getattr(record, "original_file", "-"),
                "new_file": getattr(record, "new_file", "-"),
                "project_name": getattr(record, "project_name", "General")
            }
            log_bridge.log_record_emitted.emit(log_data)
        except Exception:
            self.handleError(record)

def setup_logger(name: str = "FlowMate") -> logging.Logger:
    """Configures and returns the application logger."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # File Handler
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Stream Handler (stdout)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(logging.INFO)
        stream_formatter = logging.Formatter("[%(levelname)s] %(message)s")
        stream_handler.setFormatter(stream_formatter)
        logger.addHandler(stream_handler)

        # Qt Signal Handler for UI
        qt_handler = QtSignalLogHandler()
        qt_handler.setLevel(logging.INFO)
        logger.addHandler(qt_handler)

    return logger

logger = setup_logger()

def log_activity(msg: str, level: str = "INFO", original_file: str = "-", new_file: str = "-", project_name: str = "General") -> None:
    """Helper method to log structured file renaming activity."""
    extra = {
        "original_file": original_file,
        "new_file": new_file,
        "project_name": project_name
    }
    lvl = getattr(logging, level.upper(), logging.INFO)
    logger.log(lvl, msg, extra=extra)
