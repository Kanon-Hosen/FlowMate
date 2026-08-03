import json
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))
from typing import Any, Dict
from core.logger import logger

CONFIG_DIR = Path(__file__).parent.parent / "config"
CONFIG_FILE = CONFIG_DIR / "app_config.json"

DEFAULT_APP_CONFIG: Dict[str, Any] = {
    "active_project_id": "default",
    "theme": "dark",
    "auto_start_watcher": False,
    "enable_desktop_notifications": True,
    "minimize_to_tray": True,
    "window_width": 1200,
    "window_height": 800
}

class SettingsManager:
    """Manages global application configuration persistence."""

    def __init__(self, config_path: Path = CONFIG_FILE):
        self.config_path = config_path
        self.config_path.parent.mkdir(exist_ok=True, parents=True)
        self.data: Dict[str, Any] = self.load()

    def load(self) -> Dict[str, Any]:
        """Loads settings from JSON file or creates defaults."""
        if not self.config_path.exists():
            logger.info("app_config.json missing. Creating default application configuration.")
            self.save_data(DEFAULT_APP_CONFIG)
            return DEFAULT_APP_CONFIG.copy()

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Ensure all default keys exist
                for key, value in DEFAULT_APP_CONFIG.items():
                    if key not in data:
                        data[key] = value
                return data
        except Exception as e:
            logger.error(f"Error reading app config: {e}. Reverting to defaults.")
            return DEFAULT_APP_CONFIG.copy()

    def save(self) -> bool:
        """Saves current memory settings to JSON."""
        return self.save_data(self.data)

    def save_data(self, data: Dict[str, Any]) -> bool:
        """Writes configuration dictionary to disk."""
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self.data = data
            return True
        except Exception as e:
            logger.error(f"Failed to write application settings: {e}")
            return False

    def get(self, key: str, default: Any = None) -> Any:
        return self.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.data[key] = value
        self.save()
