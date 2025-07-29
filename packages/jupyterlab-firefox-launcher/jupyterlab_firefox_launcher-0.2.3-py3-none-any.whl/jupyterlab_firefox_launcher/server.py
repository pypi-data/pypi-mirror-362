import os
import subprocess
import time
from tornado import web
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join


class FirefoxLauncherHandler(APIHandler):
    @web.authenticated
    def post(self):
        """Start Firefox with Xpra and return the proxy URL"""
        try:
            # Check if Xpra is already running
            if self._is_xpra_running():
                port = self._get_xpra_port()
                url = f"/proxy/{port}/"
                self.finish({"status": "already_running", "url": url})
                return
            
            # Start Xpra with Firefox
            if self._start_xpra_firefox():
                port = self._get_xpra_port()
                url = f"/proxy/{port}/"
                self.finish({"status": "started", "url": url})
            else:
                self.set_status(500)
                self.finish({"status": "error", "error": "Failed to start Firefox"})
                
        except Exception as e:
            self.set_status(500)
            self.finish({"status": "error", "error": str(e)})
    
    def _is_xpra_running(self):
        """Check if Xpra is running"""
        try:
            subprocess.check_output(["pgrep", "-f", "xpra"])
            return True
        except subprocess.CalledProcessError:
            return False
    
    def _get_xpra_port(self):
        """Get the port Xpra is running on"""
        try:
            with open('/tmp/xpra-port', 'r') as f:
                return int(f.read().strip())
        except:
            return 15000
    
    def _start_xpra_firefox(self):
        """Start Xpra with Firefox"""
        try:
            script_path = os.path.join(os.path.dirname(__file__), '..', 'launch-firefox-xpra.sh')
            script_path = os.path.abspath(script_path)
            
            # Start the script in background
            process = subprocess.Popen(
                [script_path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            # Wait a bit for startup
            time.sleep(3)
            
            # Check if it started successfully
            return self._is_xpra_running()
            
        except Exception as e:
            self.log.error(f"Failed to start Xpra: {e}")
            return False


def setup_handlers(web_app):
    """Setup the API handlers"""
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupyterlab-firefox-launcher", "launch")
    handlers = [(route_pattern, FirefoxLauncherHandler)]
    web_app.add_handlers(host_pattern, handlers)


def load_jupyter_server_extension(app):
    """Called when the extension is loaded"""
    setup_handlers(app.web_app)
    app.log.info("Loaded jupyterlab_firefox_launcher extension")


def _jupyter_server_extension_paths():
    return [{
        "module": "jupyterlab_firefox_launcher"
    }]

