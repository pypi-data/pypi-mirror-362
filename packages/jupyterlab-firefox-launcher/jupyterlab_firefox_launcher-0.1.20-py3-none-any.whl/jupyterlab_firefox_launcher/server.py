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

# Log environment information
logger.info("=== Firefox Launcher Extension Starting ===")
logger.info(f"Python executable: {os.sys.executable}")
logger.info(f"Working directory: {os.getcwd()}")
logger.info(f"User: {os.getenv('USER', 'unknown')}")
logger.info(f"Display: {os.getenv('DISPLAY', 'not set')}")
logger.info(f"JUPYTERHUB_USER: {os.getenv('JUPYTERHUB_USER', 'not set')}")
logger.info(f"JUPYTERHUB_SERVICE_PREFIX: {os.getenv('JUPYTERHUB_SERVICE_PREFIX', 'not set')}")
logger.info(f"HOME: {os.getenv('HOME', 'not set')}")

# Check if we're in a JupyterHub environment
IS_JUPYTERHUB = bool(os.getenv('JUPYTERHUB_USER'))
if IS_JUPYTERHUB:
    logger.info("Running in JupyterHub environment")
else:
    logger.info("Running in standalone Jupyter environment")


class FirefoxLauncherHandler(APIHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xvfb_process = None
        self.vnc_process = None
        self.novnc_process = None
        logger.info("FirefoxLauncherHandler initialized")
        
    @web.authenticated
    def get(self):
        """Handle GET requests for debugging"""
        logger.info("=== GET request received for Firefox launcher (debug) ===")
        logger.info(f"Request headers: {dict(self.request.headers)}")
        self.finish({
            "message": "Firefox launcher endpoint is working",
            "method": "GET",
            "available_methods": ["GET", "POST"],
            "environment": "JupyterHub" if IS_JUPYTERHUB else "Standalone",
            "user": os.getenv('JUPYTERHUB_USER', os.getenv('USER', 'unknown'))
        })
    
    @web.authenticated
    def post(self):
        logger.info("=== POST request received for Firefox launcher ===")
        logger.info(f"Request headers: {dict(self.request.headers)}")
        logger.info(f"Request body: {self.request.body}")
        
        # Check environment
        if IS_JUPYTERHUB:
            logger.info("Detected JupyterHub environment")
            # In JupyterHub, we need to check if we have the right permissions and environment
            user = os.getenv('JUPYTERHUB_USER', 'unknown')
            logger.info(f"JupyterHub user: {user}")
            
            # Check if we can run GUI applications
            if not os.getenv('DISPLAY'):
                logger.warning("No DISPLAY environment variable set")
                # We might need to create a virtual display
        
        # Check system dependencies
        dependencies_ok, missing_deps = self._check_dependencies()
        if not dependencies_ok:
            logger.error(f"Missing system dependencies: {missing_deps}")
            self.set_status(500)
            self.finish({
                "error": f"Missing system dependencies: {', '.join(missing_deps)}",
                "dependencies": missing_deps
            })
            return
        
        # Only spawn if not already running
        if not self._is_vnc_running():
            logger.info("VNC is not running, starting Firefox VNC setup...")
            try:
                self._launch_firefox_vnc()
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
    
    def _check_dependencies(self):
        """Check if all required system dependencies are available"""
        logger.info("Checking system dependencies...")
        dependencies = ['firefox', 'Xvfb', 'x11vnc', 'websockify']
        missing = []
        
        for dep in dependencies:
            try:
                result = subprocess.run(['which', dep], capture_output=True, text=True)
                if result.returncode == 0:
                    logger.debug(f"✓ Found {dep} at {result.stdout.strip()}")
                else:
                    logger.warning(f"✗ Missing {dep}")
                    missing.append(dep)
            except Exception as e:
                logger.error(f"Error checking for {dep}: {e}")
                missing.append(dep)
        
        if missing:
            logger.error(f"Missing dependencies: {missing}")
            return False, missing
        else:
            logger.info("All dependencies found")
            return True, []
    
    def _launch_firefox_vnc(self):
        """Launch the complete Firefox VNC setup"""
        logger.info("Starting Firefox VNC setup...")
        
        # Kill any existing processes first
        logger.info("Cleaning up existing processes...")
        self._cleanup_processes()
        
        # Determine display number - use a user-specific one for JupyterHub
        if IS_JUPYTERHUB:
            user = os.getenv('JUPYTERHUB_USER', 'default')
            # Use hash of username to get consistent display number for this user
            display_num = 90 + (hash(user) % 10)  # 90-99 range
        else:
            display_num = 99
        
        display = f":{display_num}"
        logger.info(f"Using display: {display}")
        
        # Start Xvfb on the selected display
        logger.info(f"Starting Xvfb on display {display}...")
        xvfb_cmd = ["Xvfb", display, "-screen", "0", "1280x720x24", "-ac", "+extension", "GLX"]
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
        
        # Determine VNC port - use user-specific port for JupyterHub
        if IS_JUPYTERHUB:
            user = os.getenv('JUPYTERHUB_USER', 'default')
            vnc_port = 5900 + (hash(user) % 100)  # 5900-5999 range
        else:
            vnc_port = 5901
        
        logger.info(f"Using VNC port: {vnc_port}")
        
        # Start VNC server on the selected display and port
        vnc_cmd = ["x11vnc", "-display", display, "-nopw", "-listen", "localhost", 
                  "-xkb", "-rfbport", str(vnc_port), "-forever", "-shared"]
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
        
        # Determine web port - use user-specific port for JupyterHub
        if IS_JUPYTERHUB:
            user = os.getenv('JUPYTERHUB_USER', 'default')
            web_port = 6080 + (hash(user) % 100)  # 6080-6179 range
        else:
            web_port = 6080
        
        logger.info(f"Using web port: {web_port}")
        
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
            websockify_cmd = ["websockify", str(web_port), f"localhost:{vnc_port}"]
        else:
            logger.info(f"Using noVNC web interface from: {novnc_path}")
            websockify_cmd = ["websockify", f"--web={novnc_path}", str(web_port), f"localhost:{vnc_port}"]
        
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
        firefox_env = {**os.environ, "DISPLAY": display}
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
            vnc_port_check = subprocess.check_output(["lsof", "-i", f":{vnc_port}"], stderr=subprocess.DEVNULL)
            logger.info(f"VNC port {vnc_port} is listening")
        except subprocess.CalledProcessError:
            logger.warning(f"VNC port {vnc_port} is not listening")
        
        try:
            web_port_check = subprocess.check_output(["lsof", "-i", f":{web_port}"], stderr=subprocess.DEVNULL)
            logger.info(f"Web port {web_port} is listening")
        except subprocess.CalledProcessError:
            logger.warning(f"Web port {web_port} is not listening")
        
        logger.info("Firefox with VNC launched successfully")
        
        # Determine the correct URL based on whether noVNC web interface is available
        if novnc_path:
            vnc_url = f"http://localhost:{web_port}/vnc.html?autoconnect=true&resize=scale"
        else:
            vnc_url = f"http://localhost:{web_port}"
        
        logger.info(f"Returning success response with URL: {vnc_url}")
        response_data = {"status": "started", "url": vnc_url}
        logger.debug(f"Response data: {response_data}")
        self.finish(response_data)
    
    def _cleanup_processes(self):
        """Clean up any existing processes"""
        logger.info("Starting cleanup of existing processes...")
        try:
            # Determine ports to clean up
            if IS_JUPYTERHUB:
                user = os.getenv('JUPYTERHUB_USER', 'default')
                display_num = 90 + (hash(user) % 10)
                vnc_port = 5900 + (hash(user) % 100)
                web_port = 6080 + (hash(user) % 100)
            else:
                display_num = 99
                vnc_port = 5901
                web_port = 6080
            
            # Kill existing processes
            commands = [
                ["pkill", "-f", f"Xvfb.*:{display_num}"],
                ["pkill", "-f", f"x11vnc.*{vnc_port}"],
                ["pkill", "-f", f"websockify.*{web_port}"]
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
        
        # For JupyterHub, check user-specific port range
        if IS_JUPYTERHUB:
            user = os.getenv('JUPYTERHUB_USER', 'default')
            web_port = 6080 + (hash(user) % 100)  # 6080-6179 range
        else:
            web_port = 6080
        
        try:
            # Check if websockify is running on the expected port
            out = subprocess.check_output(["lsof", "-i", f":{web_port}"], stderr=subprocess.DEVNULL)
            logger.debug(f"VNC running check output for port {web_port}: {out.strip()}")
            is_running = bool(out.strip())
            logger.info(f"VNC is {'running' if is_running else 'not running'} on port {web_port}")
            return is_running
        except subprocess.CalledProcessError:
            logger.debug(f"VNC is not running on port {web_port} (lsof returned error)")
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



