<div align="center">

# ⚡ FlowMate v2.0 Pro

### *Automated Sequential Video Renamer & File Management Engine*

[![Version 2.0.0](https://img.shields.io/badge/Version-v2.0.0%20Pro-6366F1?style=for-the-badge&logo=rocket&logoColor=white)](https://github.com/Kanon-Hosen/FlowMate)
[![Python 3.12+](https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PySide6](https://img.shields.io/badge/GUI-PySide6%20%2F%20Qt%206-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PySide6/)
[![Platform](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-0078D6?style=for-the-badge&logo=apple&logoColor=white)](#-installation)
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

*FlowMate v2.0 Pro automatically detects completed browser downloads (Google Chrome, Edge, Firefox), parses dynamic naming templates, renames files sequentially (e.g. `Shorts_2026-08-04_001.mp4`), and offers a Drag-and-Drop Batch Lab for offline media libraries.*

[Key Features](#-key-features) •
[Dynamic Templates](#-dynamic-naming-templates) •
[Batch Lab](#-batch-renamer-lab) •
[Quick Start](#-quick-start) •
[Architecture](#-architecture) •
[License](#-license)

---

</div>

## 📖 Overview

When producing video content, downloading multiple video clips manually one-by-one from web tools or Google Chrome often leads to messy download folders filled with unorganized default filenames (e.g. `download (1).mp4`, `videoplayback.mp4`).

**FlowMate v2.0 Pro** solves this workflow bottleneck. Operating silently in the background, FlowMate monitors your browser download directory, waits for file write completion to ensure zero data corruption, parses custom naming patterns, automatically renames the files in numeric sequence (`001.mp4`, `Shorts_2026-08-04_001.mp4`...), and instantly relocates them into designated output project folders.

---

## ✨ Key Features (v2.0 Pro)

- **🏷️ Dynamic Naming Templates**: Support tokenized placeholders like `{project}_{date}_{counter}.mp4` with a live preview.
- **📦 Batch Drag-and-Drop Lab**: Drag and drop existing media files or entire folders to simulate and bulk-rename offline files in seconds.
- **⚡ Real-time Directory Monitoring**: Powered by native OS file system events (`watchdog`) to instantly detect new downloads without high CPU polling.
- **🛡️ Thread-Safe & Atomic File Locking**: Includes multi-stage size stabilization and OS file handle verification to prevent race conditions during large file downloads.
- **🔢 Minimum File Size Filtering**: Skip incomplete, tiny, or junk thumbnail files below a specified MB threshold.
- **⚙️ OS Autostart Integration**: Easily configure FlowMate to launch automatically on Linux or Windows system boot.
- **🔔 System Tray Integration**: Minimizes to Linux / Windows system tray for uninterrupted background operation with desktop notifications.
- **🎨 Modern Dark Theme UX**: Fluent-inspired dark UI with custom typography (`Ubuntu` / `Inter`), glassmorphism card widgets, and glowing status badges.

---

## 🏷️ Dynamic Naming Templates

FlowMate v2.0 Pro allows you to define flexible filename formatting patterns per project:

| Token | Description | Example Output |
| :--- | :--- | :--- |
| `{counter}` | Formatted numeric sequence | `001`, `002` |
| `{project}` | Active project title | `YouTube_Shorts` |
| `{date}` | Current date timestamp | `2026-08-04` |
| `{time}` | Current time timestamp | `14-30-05` |
| `{original}` | Original base filename | `raw_clip` |
| `{ext}` | Clean file extension | `mp4` |

**Example Template**: `{project}_{date}_{counter}`  
**Result**: `YouTube_Shorts_2026-08-04_001.mp4`

---

## 📦 Batch Renamer Lab

Got existing folders of unorganized video clips?
1. Click **Batch Lab** in the navigation sidebar.
2. Drag and drop any folder or selection of files into the dropzone.
3. Review the **Live Simulation Table** showing original vs. new filenames.
4. Click **⚡ Execute Batch Rename** to rename and organize them instantly!

---

## 🚀 Quick Start

### 🐧 Linux (Zorin OS 18 / Ubuntu / Mint / Debian)

#### 1. Clone the Repository
```bash
git clone https://github.com/Kanon-Hosen/FlowMate.git
cd FlowMate
```

#### 2. Run Automated Setup
```bash
chmod +x setup.sh
./setup.sh
```

#### 3. Launch FlowMate
```bash
python3 main.py
```
*(Or double-click the **FlowMate** desktop shortcut created by `setup.sh` on your desktop!)*

---

### 🪟 Windows (10 / 11)

#### Option A: Run via Python
```cmd
git clone https://github.com/Kanon-Hosen/FlowMate.git
cd FlowMate
pip install -r requirements.txt
python main.py
```

#### Option B: Build Standalone `.exe` (No Python Required)
1. Double-click `build_windows.bat` in the project root.
2. Your standalone executable will be generated at `dist/FlowMate.exe`.

---

### 🍎 macOS (Apple Silicon M1/M2/M3/M4 & Intel)

#### Option A: Run via Python
```bash
git clone https://github.com/Kanon-Hosen/FlowMate.git
cd FlowMate
pip3 install -r requirements.txt
python3 main.py
```

#### Option B: Build Standalone `FlowMate.app`
1. Run `./build_mac.sh` in the terminal.
2. Double-click `dist/FlowMate.app` to launch!

---

## 🏗️ Architecture & Project Structure

FlowMate v2.0 Pro enforces a strict modular MVC architecture for high reliability:

```
FlowMate/
├── main.py                    # Application Entry Point & Qt Event Loop
├── setup.sh                   # Automated Linux Installer Script
├── build_windows.bat          # Standalone Windows PyInstaller Script
├── build_mac.sh               # Standalone macOS PyInstaller Script
├── requirements.txt           # Python Package Dependencies
│
├── core/                      # Engine & Business Logic Layer
│   ├── app_state.py           # Central Application State & Qt Signal Bus
│   ├── naming_engine.py       # [v2.0] Dynamic Tokenized Filename Parser
│   ├── watcher.py             # QThread Watchdog Directory Observer
│   ├── renamer.py             # Atomic File Locking & Sequential Renamer
│   ├── project_manager.py     # JSON Project Workspace Persistence
│   ├── settings.py            # User Preferences Storage
│   └── logger.py              # File & Qt Real-time Log Handlers
│
├── ui/                        # User Interface Layer (PySide6)
│   ├── main_window.py         # Primary Desktop Shell Window
│   ├── styles.py              # QSS Modern Dark Theme Design System
│   ├── views/                 # View Screens
│   │   ├── dashboard_view.py  # Active Project Dashboard & Live Template Preview
│   │   ├── batch_view.py      # [v2.0] Drag & Drop Batch Renamer Lab
│   │   ├── projects_view.py   # Multi-Project Workspace Manager
│   │   ├── logs_view.py       # Live Activity & File Rename Audits
│   │   └── settings_view.py   # System Preferences & OS Autostart
│   └── widgets/               # Reusable Custom Controls & Sidebar
│
├── assets/                    # Application Branding & Icons
│   └── logo.png
└── projects/                  # Saved Project JSON Workspace Files
```

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

Crafted with ❤️ by **[Kanon Hosen](https://github.com/Kanon-Hosen)**

*Star ⭐ this repository if FlowMate saved you time!*

</div>
