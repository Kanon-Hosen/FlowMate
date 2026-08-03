import os
import sys
import time
import threading
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

from typing import Optional, Dict, Any
from PySide6.QtCore import QThread, Signal
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from core.logger import logger

class DownloadEventHandler(FileSystemEventHandler):
    """
    Watchdog event handler monitoring Chrome download events.
    Detects both newly created files and renamed files (.crdownload -> final extension).
    Includes debouncing to prevent double processing.
    """

    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self._recent_events: Dict[str, float] = {}
        self._lock = threading.Lock()

    def _should_process(self, path: str) -> bool:
        if not path or path.endswith(".crdownload") or path.endswith(".tmp") or path.endswith(".part"):
            return False

        now = time.time()
        with self._lock:
            self._recent_events = {p: t for p, t in self._recent_events.items() if now - t < 5.0}

            if path in self._recent_events:
                if now - self._recent_events[path] < 0.5:
                    return False

            self._recent_events[path] = now
            return True

    def on_created(self, event):
        if event.is_directory:
            return
        path = str(event.src_path)
        if self._should_process(path):
            logger.info(f"Watchdog detected new file creation: {path}")
            self.callback(path)

    def on_moved(self, event):
        if event.is_directory:
            return
        dest_path = str(event.dest_path)
        if self._should_process(dest_path):
            logger.info(f"Watchdog detected Chrome download completion move: {event.src_path} -> {dest_path}")
            self.callback(dest_path)

class WatcherThread(QThread):
    """
    QThread worker running watchdog Observer in background to keep UI 100% responsive.
    """
    file_detected_signal = Signal(str)
    started_signal = Signal(str)
    stopped_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, watch_dir: str, parent=None):
        super().__init__(parent)
        self.watch_dir = watch_dir
        self.observer: Any = None
        self._is_running = False

    def run(self):
        """Runs the watchdog observer loop."""
        expanded = os.path.expanduser(self.watch_dir)
        target_path = Path(expanded)

        if not target_path.exists() or not target_path.is_dir():
            err = f"Watch directory does not exist or is invalid: {self.watch_dir}"
            logger.error(err)
            self.error_signal.emit(err)
            return

        try:
            handler = DownloadEventHandler(self._on_event)
            obs = Observer()
            self.observer = obs
            obs.schedule(handler, str(target_path), recursive=False)
            obs.start()
            self._is_running = True
            logger.info(f"WatcherThread monitoring directory: {expanded}")
            self.started_signal.emit(expanded)

            while self._is_running:
                time.sleep(0.4)

        except Exception as e:
            err = f"Error in directory watcher thread: {e}"
            logger.error(err)
            self.error_signal.emit(err)
        finally:
            if self.observer is not None and getattr(self.observer, "is_alive", lambda: False)():
                self.observer.stop()
                self.observer.join()
            self._is_running = False
            self.stopped_signal.emit()

    def _on_event(self, path: str):
        """Dispatches event to Qt main thread via signal."""
        self.file_detected_signal.emit(path)

    def stop(self):
        """Stops the watcher thread cleanly."""
        self._is_running = False
        if self.observer is not None and getattr(self.observer, "is_alive", lambda: False)():
            self.observer.stop()
        self.wait(2000)
