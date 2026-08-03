import json
import threading
from typing import Any, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from core.logger import logger

class FlowMateAPIHandler(BaseHTTPRequestHandler):
    """Local HTTP API handler providing FlowMate state to the Chrome Extension."""

    app_state: Any = None  # Injected by APIServer

    def _set_cors_headers(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_OPTIONS(self):
        self._set_cors_headers()

    def do_GET(self):
        if not FlowMateAPIHandler.app_state:
            self._set_cors_headers()
            self.wfile.write(json.dumps({"error": "AppState not initialized"}).encode())
            return

        state = FlowMateAPIHandler.app_state
        proj = state.active_project

        if self.path == "/status" or self.path == "/api/status":
            self._set_cors_headers()
            resp = {
                "connected": True,
                "version": "2.0.0",
                "is_watching": state.is_watching,
                "active_project": {
                    "id": proj.id if proj else "default",
                    "name": proj.name if proj else "Default",
                    "watch_dir": proj.watch_dir if proj else "",
                    "output_dir": proj.output_dir if proj else "",
                    "current_counter": proj.current_counter if proj else 1,
                    "padding_digits": proj.padding_digits if proj else 3,
                    "name_template": getattr(proj, "name_template", "{counter}") if proj else "{counter}",
                    "files_today": proj.files_today if proj else 0,
                    "files_total": proj.files_total if proj else 0
                } if proj else None,
                "all_projects": [
                    {"id": p.id, "name": p.name}
                    for p in state.project_manager.projects.values()
                ]
            }
            self.wfile.write(json.dumps(resp).encode())
        else:
            self._set_cors_headers()
            self.wfile.write(json.dumps({"status": "FlowMate API Server Running"}).encode())

    def do_POST(self):
        if not FlowMateAPIHandler.app_state:
            self._set_cors_headers()
            self.wfile.write(json.dumps({"error": "AppState not initialized"}).encode())
            return

        state = FlowMateAPIHandler.app_state

        if self.path == "/api/switch_project":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length).decode()
            try:
                data = json.loads(body)
                proj_id = data.get("project_id")
                if proj_id and proj_id in state.project_manager.projects:
                    state.set_active_project(proj_id)
                    self._set_cors_headers()
                    self.wfile.write(json.dumps({"success": True, "active_project": state.active_project.name}).encode())
                    return
            except Exception as e:
                logger.error(f"API Switch project error: {e}")

        self._set_cors_headers()
        self.wfile.write(json.dumps({"success": False}).encode())

    def log_message(self, format, *args):
        pass  # Suppress HTTP server console clutter


class FlowMateAPIServer:
    """Threaded HTTP API Server listening on port 18420 for browser extension requests."""

    def __init__(self, app_state, host: str = "127.0.0.1", port: int = 18420):
        self.app_state = app_state
        self.host = host
        self.port = port
        FlowMateAPIHandler.app_state = app_state
        self.httpd = None
        self.thread = None

    def start(self):
        try:
            self.httpd = HTTPServer((self.host, self.port), FlowMateAPIHandler)
            self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
            self.thread.start()
            logger.info(f"FlowMate Extension Local API Server listening on http://{self.host}:{self.port}")
        except Exception as e:
            logger.error(f"Failed to start FlowMate API Server on port {self.port}: {e}")

    def stop(self):
        if self.httpd:
            self.httpd.shutdown()
            self.httpd.server_close()
            logger.info("FlowMate API Server stopped.")
