import logging
import os
import subprocess
from tornado import web
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from jupyter_server.extension.application import ExtensionApp


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class FirefoxLauncherHandler(APIHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vnc_process = None
        self.novnc_process = None
        
    @web.authenticated
    def post(self):
        # Only spawn if not already running
        if not self._is_vnc_running():
            try:
                # Start Xvfb on display :99
                xvfb_process = subprocess.Popen(
                    ["Xvfb", ":99", "-screen", "0", "1024x768x24"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                # Wait a moment for Xvfb to start
                import time
                time.sleep(1)
                
                # Start VNC server on display :99
                self.vnc_process = subprocess.Popen(
                    ["x11vnc", "-display", ":99", "-nopw", "-listen", "localhost", "-xkb", "-rfbport", "5901"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                # Wait for VNC to start
                time.sleep(1)
                
                # Start noVNC web server
                self.novnc_process = subprocess.Popen(
                    ["websockify", "--web=/usr/share/novnc/", "6080", "localhost:5901"],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                # Wait for noVNC to start
                time.sleep(1)
                
                # Start Firefox on the virtual display
                subprocess.Popen(
                    ["firefox"],
                    env={**os.environ, "DISPLAY": ":99"},
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                
                logger.info("Firefox with VNC launched successfully")
                self.finish({"status": "started", "url": "http://localhost:6080/vnc.html?autoconnect=true"})
            except Exception as e:
                logger.error(f"Failed to launch Firefox: {e}")
                self.set_status(500)
                self.finish({"error": str(e)})
        else:
            logger.info("Firefox VNC setup is already running")
            self.finish({"status": "already running", "url": "http://localhost:6080/vnc.html?autoconnect=true"})

    def _is_vnc_running(self):
        try:
            # Check if VNC server is running on port 5901
            out = subprocess.check_output(["lsof", "-i", ":5901"])
            logger.debug(f"VNC running check output: {out.strip()}")
            return bool(out.strip())
        except subprocess.CalledProcessError:
            logger.debug("VNC is not running")
            return False


def setup_handlers(web_app):
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupyterlab-firefox-launcher", "launch")
    handlers = [(route_pattern, FirefoxLauncherHandler)]
    web_app.add_handlers(host_pattern, handlers)


class FirefoxLauncherExtension(ExtensionApp):
    """JupyterLab Firefox Launcher Extension"""
    
    name = "jupyterlab_firefox_launcher"
    
    def initialize_handlers(self):
        """Initialize the extension handlers"""
        setup_handlers(self.serverapp.web_app)



