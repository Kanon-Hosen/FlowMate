import sys
import signal
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.logger import logger

def main():
    logger.info("Initializing ClipPilot desktop application...")
    
    # Enable Ctrl+C SIGINT handling
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    app.setApplicationName("ClipPilot")
    app.setOrganizationName("ClipPilot")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
