import logging
import os
import subprocess
import time
from tornado import web
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from jupyter_server.extension.application import ExtensionApp


# Set up comprehensive logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Also log to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - Firefox Launcher - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class FirefoxLauncherHandler(APIHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xvfb_process = None
        self.vnc_process = None
        self.novnc_process = None
        logger.info("FirefoxLauncherHandler initialized")
        
    @web.authenticated
    def post(self):
        logger.info("=== POST request received for Firefox launcher ===")
        logger.info(f"Request headers: {dict(self.request.headers)}")
        logger.info(f"Request body: {self.request.body}")
        
        # Only spawn if not already running
        if not self._is_vnc_running():
            logger.info("VNC is not running, starting Firefox VNC setup...")
            try:
                logger.info("Starting Firefox VNC setup...")
                
                # Kill any existing processes first
                logger.info("Cleaning up existing processes...")
                self._cleanup_processes()
                
                # Start Xvfb on display :99
                logger.info("Starting Xvfb on display :99...")
                xvfb_cmd = ["Xvfb", ":99", "-screen", "0", "1280x720x24", "-ac", "+extension", "GLX"]
                logger.debug(f"Xvfb command: {' '.join(xvfb_cmd)}")
                
                self.xvfb_process = subprocess.Popen(
                    xvfb_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                logger.info(f"Xvfb process started with PID: {self.xvfb_process.pid}")
                
                # Wait a moment for Xvfb to start
                time.sleep(2)
                
                # Check if Xvfb started successfully
                if self.xvfb_process.poll() is not None:
                    stdout, stderr = self.xvfb_process.communicate()
                    logger.error(f"Xvfb failed to start: {stderr.decode()}")
                    logger.error(f"Xvfb stdout: {stdout.decode()}")
                    raise Exception(f"Xvfb failed: {stderr.decode()}")
                
                logger.info("Xvfb started successfully, starting VNC server...")
                
                # Start VNC server on display :99
                vnc_cmd = ["x11vnc", "-display", ":99", "-nopw", "-listen", "localhost", 
                          "-xkb", "-rfbport", "5901", "-forever", "-shared"]
                logger.debug(f"VNC command: {' '.join(vnc_cmd)}")
                
                self.vnc_process = subprocess.Popen(
                    vnc_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                logger.info(f"VNC process started with PID: {self.vnc_process.pid}")
                
                # Wait for VNC to start
                time.sleep(3)
                
                # Check if VNC started successfully
                if self.vnc_process.poll() is not None:
                    stdout, stderr = self.vnc_process.communicate()
                    logger.error(f"x11vnc failed to start: {stderr.decode()}")
                    logger.error(f"x11vnc stdout: {stdout.decode()}")
                    raise Exception(f"VNC failed: {stderr.decode()}")
                
                logger.info("VNC started successfully, starting noVNC web server...")
                
                # Start noVNC web server - check if novnc is available
                novnc_paths = ["/usr/share/novnc/", "/usr/local/share/novnc/", "/opt/novnc/"]
                novnc_path = None
                for path in novnc_paths:
                    logger.debug(f"Checking for noVNC at: {path}")
                    if os.path.exists(path):
                        novnc_path = path
                        logger.info(f"Found noVNC at: {novnc_path}")
                        break
                
                if not novnc_path:
                    logger.warning("noVNC not found, using websockify without web interface")
                    websockify_cmd = ["websockify", "6080", "localhost:5901"]
                else:
                    logger.info(f"Using noVNC web interface from: {novnc_path}")
                    websockify_cmd = ["websockify", f"--web={novnc_path}", "6080", "localhost:5901"]
                
                logger.debug(f"Websockify command: {' '.join(websockify_cmd)}")
                
                self.novnc_process = subprocess.Popen(
                    websockify_cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                logger.info(f"Websockify process started with PID: {self.novnc_process.pid}")
                
                # Wait for noVNC to start
                time.sleep(3)
                
                # Check if noVNC started successfully
                if self.novnc_process.poll() is not None:
                    stdout, stderr = self.novnc_process.communicate()
                    logger.error(f"websockify failed to start: {stderr.decode()}")
                    logger.error(f"websockify stdout: {stdout.decode()}")
                    raise Exception(f"noVNC failed: {stderr.decode()}")
                
                logger.info("Websockify started successfully, starting Firefox...")
                
                # Start Firefox on the virtual display
                firefox_cmd = ["firefox", "--new-instance", "--no-remote"]
                firefox_env = {**os.environ, "DISPLAY": ":99"}
                logger.debug(f"Firefox command: {' '.join(firefox_cmd)}")
                logger.debug(f"Firefox environment DISPLAY: {firefox_env.get('DISPLAY')}")
                
                firefox_process = subprocess.Popen(
                    firefox_cmd,
                    env=firefox_env,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
                logger.info(f"Firefox process started with PID: {firefox_process.pid}")
                
                # Wait a moment for Firefox to start
                time.sleep(3)
                
                # Verify all processes are still running
                processes_status = {
                    "Xvfb": self.xvfb_process.poll() is None,
                    "x11vnc": self.vnc_process.poll() is None,
                    "websockify": self.novnc_process.poll() is None,
                    "firefox": firefox_process.poll() is None
                }
                logger.info(f"Process status check: {processes_status}")
                
                # Check if ports are listening
                try:
                    vnc_port_check = subprocess.check_output(["lsof", "-i", ":5901"], stderr=subprocess.DEVNULL)
                    logger.info("VNC port 5901 is listening")
                except subprocess.CalledProcessError:
                    logger.warning("VNC port 5901 is not listening")
                
                try:
                    web_port_check = subprocess.check_output(["lsof", "-i", ":6080"], stderr=subprocess.DEVNULL)
                    logger.info("Web port 6080 is listening")
                except subprocess.CalledProcessError:
                    logger.warning("Web port 6080 is not listening")
                
                logger.info("Firefox with VNC launched successfully")
                
                # Determine the correct URL based on whether noVNC web interface is available
                if novnc_path:
                    vnc_url = "http://localhost:6080/vnc.html?autoconnect=true&resize=scale"
                else:
                    vnc_url = "http://localhost:6080"
                
                logger.info(f"Returning success response with URL: {vnc_url}")
                response_data = {"status": "started", "url": vnc_url}
                logger.debug(f"Response data: {response_data}")
                self.finish(response_data)
                
            except Exception as e:
                logger.error(f"Failed to launch Firefox: {e}", exc_info=True)
                self._cleanup_processes()
                self.set_status(500)
                error_response = {"error": str(e)}
                logger.debug(f"Error response: {error_response}")
                self.finish(error_response)
        else:
            logger.info("Firefox VNC setup is already running")
            vnc_url = "http://localhost:6080/vnc.html?autoconnect=true&resize=scale"
            response_data = {"status": "already running", "url": vnc_url}
            logger.debug(f"Already running response: {response_data}")
            self.finish(response_data)
    
    def _cleanup_processes(self):
        """Clean up any existing processes"""
        logger.info("Starting cleanup of existing processes...")
        try:
            # Kill existing processes
            commands = [
                ["pkill", "-f", "Xvfb.*:99"],
                ["pkill", "-f", "x11vnc.*5901"],
                ["pkill", "-f", "websockify.*6080"]
            ]
            
            for cmd in commands:
                try:
                    result = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                    logger.debug(f"Cleanup command {' '.join(cmd)}: return code {result.returncode}")
                except Exception as cmd_error:
                    logger.debug(f"Error running cleanup command {' '.join(cmd)}: {cmd_error}")
                    
            time.sleep(1)
            logger.info("Process cleanup completed")
        except Exception as e:
            logger.error(f"Error during cleanup: {e}", exc_info=True)

    def _is_vnc_running(self):
        logger.debug("Checking if VNC is running...")
        try:
            # Check if websockify is running on port 6080
            out = subprocess.check_output(["lsof", "-i", ":6080"], stderr=subprocess.DEVNULL)
            logger.debug(f"VNC running check output: {out.strip()}")
            is_running = bool(out.strip())
            logger.info(f"VNC is {'running' if is_running else 'not running'}")
            return is_running
        except subprocess.CalledProcessError:
            logger.debug("VNC is not running (lsof returned error)")
            return False


def setup_handlers(web_app):
    logger.info("Setting up Firefox launcher handlers...")
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    route_pattern = url_path_join(base_url, "jupyterlab-firefox-launcher", "launch")
    logger.info(f"Registering route: {route_pattern}")
    handlers = [(route_pattern, FirefoxLauncherHandler)]
    web_app.add_handlers(host_pattern, handlers)
    logger.info("Firefox launcher handlers registered successfully")


class FirefoxLauncherExtension(ExtensionApp):
    """JupyterLab Firefox Launcher Extension"""
    
    name = "jupyterlab_firefox_launcher"
    
    def initialize_handlers(self):
        """Initialize the extension handlers"""
        logger.info("Initializing Firefox launcher extension handlers...")
        setup_handlers(self.serverapp.web_app)
        logger.info("Firefox launcher extension initialized successfully")



