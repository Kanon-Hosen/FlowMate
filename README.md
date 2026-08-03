# FlowMate ⚡

**FlowMate** is a production-grade, asynchronous Linux desktop application designed for **Zorin OS 18 / Ubuntu Linux**. It automatically detects completed Google Chrome downloads, sequentially renames video clips or files (e.g. `001.mp4`, `002.mp4`, `003.mp4`...), and moves them cleanly into your output project directory.

![FlowMate Header](assets/logo.png)

---

## 🎯 Purpose & Features

When downloading numerous video clips (e.g., from Google Flow or Chrome), manual file organizing is tedious. **FlowMate** automates this completely:

- **Chrome Download Detection**: Ignores temporary `.crdownload`, `.tmp`, and `.part` files during download and triggers instantly when Chrome finishes writing.
- **Smart Counter Engine**: Scans your destination folder on startup to detect the highest existing number (e.g. `003.mp4`) and automatically continues numbering (`004.mp4`).
- **Conflict Prevention**: Never overwrites existing files. If `004.mp4` exists, it advances the counter automatically.
- **Threaded & Non-Blocking**: Built with `QThread` and asynchronous `Watchdog` event monitoring to guarantee a 100% smooth, responsive UI.
- **Zorin OS / Fluent Design UI**: Modern dark and light themes, responsive card layouts, statistics metrics, and activity tables.
- **Project Support**: Create, manage, and switch between separate project workspaces, each with custom watch paths, destination folders, and counters.
- **System Tray & Linux Desktop Notifications**: Native Linux notifications when files are renamed, with background tray monitoring.
- **Activity Logging & Export**: Real-time logging table with search filtering and CSV/TXT log export capabilities.
- **Keyboard Shortcuts**: Built-in hotkeys for fast control.

---

## 🖥️ System Requirements

- **Operating System**: Zorin OS 18 / Ubuntu 22.04 LTS+ / Any Modern Linux Desktop
- **Python**: Python 3.12+
- **GUI Framework**: PySide6 (Qt 6 for Python)
- **Watcher Engine**: Watchdog

---

## 📦 Installation & Setup

1. **Clone or Navigate to the Repository**:
   ```bash
   cd FlowMate
   ```

2. **Set up Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Running FlowMate

Launch FlowMate using Python:

```bash
python main.py
```

Or using the virtual environment directly:

```bash
./.venv/bin/python main.py
```

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Description |
| :--- | :--- |
| `Ctrl + S` | Toggle Start / Stop Watching |
| `Ctrl + O` | Open Output Folder in File Manager |
| `Ctrl + W` | Open Watch Folder in File Manager |
| `Ctrl + L` | Switch to Logs View |

---

## 📁 Project Architecture

```text
FlowMate/
├── main.py                    # Application bootstrap & Qt loop initializer
├── requirements.txt           # Project dependencies (PySide6, watchdog)
├── README.md                  # Project documentation
│
├── config/
│   └── app_config.json        # Application configuration & theme options
│
├── core/
│   ├── app_state.py           # Central application state & global signal bus
│   ├── logger.py              # Thread-safe logging & Qt bridge
│   ├── project_manager.py     # Project persistence & smart counter scanner
│   ├── renamer.py             # File renaming engine & file lock checker
│   ├── settings.py            # Global settings manager
│   └── watcher.py             # QThread async Watchdog directory observer
│
├── ui/
│   ├── styles.py              # Fluent & Zorin OS dark/light stylesheets
│   ├── main_window.py         # Main window, system tray, & shortcut manager
│   ├── views/
│   │   ├── dashboard_view.py  # Dashboard view with stats & activity log
│   │   ├── projects_view.py   # Workspace & project manager view
│   │   ├── logs_view.py       # Log search, filter, & export view
│   │   └── settings_view.py   # Global settings & theme customization
│   └── widgets/
│       ├── sidebar.py         # Sidebar navigation & quick project switcher
│       ├── stat_card.py       # Reusable metric card widget
│       └── custom_controls.py # Path picker, buttons, & status badges
│
├── assets/
│   ├── logo.png               # High-res FlowMate application icon
│   └── icons/                 # UI icons
│
├── logs/                      # Application activity logs
└── projects/                  # Saved project workspace configuration files
```

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
