import sys
import signal
from pathlib import Path
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon, QPixmap
from ui.main_window import MainWindow
from core.logger import logger

ASSETS_DIR = Path(__file__).parent / "assets"
LOGO_PATH = ASSETS_DIR / "logo.png"

def main():
    logger.info("Initializing ClipPilot desktop application...")
    
    # Enable Ctrl+C SIGINT handling
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    app.setApplicationName("ClipPilot")
    app.setOrganizationName("ClipPilot")
    app.setDesktopFileName("ClipPilot.desktop")

    if LOGO_PATH.exists():
        app_icon = QIcon(str(LOGO_PATH))
        app.setWindowIcon(app_icon)

    window = MainWindow()
    if LOGO_PATH.exists():
        window.setWindowIcon(QIcon(str(LOGO_PATH)))
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
