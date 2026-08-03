import sys
import signal
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.logger import logger
from core.api_server import FlowMateAPIServer

def main():
    logger.info("Initializing FlowMate desktop application...")
    
    # Enable Ctrl+C SIGINT handling
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    app.setApplicationName("FlowMate")
    app.setOrganizationName("FlowMate")

    window = MainWindow()
    
    # Start Local API Server for Chrome Extension
    api_server = FlowMateAPIServer(window.app_state)
    api_server.start()

    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
