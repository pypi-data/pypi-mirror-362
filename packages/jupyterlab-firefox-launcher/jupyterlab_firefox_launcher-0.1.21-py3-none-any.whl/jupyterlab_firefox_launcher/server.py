import os
import subprocess
import time
import logging
from tornado import web
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from jupyter_server.extension.application import ExtensionApp

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Firefox Launcher')

# Check if we're running in JupyterHub
IS_JUPYTERHUB = bool(os.getenv('JUPYTERHUB_USER'))

class FirefoxLauncherHandler(APIHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xvfb_process = None
        self.vnc_process = None
        self.novnc_process = None
        logger.info("FirefoxLauncherHandler initialized")

    @web.authenticated
    def get(self):
        """Debug endpoint to check server status"""
        logger.info("=== GET request received for Firefox launcher (debug) ===")
        logger.info(f"Request headers: {dict(self.request.headers)}")
        
        debug_info = {
            "status": "server_running",
            "is_jupyterhub": IS_JUPYTERHUB,
            "user": os.getenv('JUPYTERHUB_USER', 'N/A'),
            "service_prefix": os.getenv('JUPYTERHUB_SERVICE_PREFIX', 'N/A'),
            "python_executable": os.sys.executable,
            "working_directory": os.getcwd()
        }
        self.finish(debug_info)

    @web.authenticated
    def post(self):
        """Launch Firefox with VNC access"""
        logger.info("=== POST request received for Firefox launcher ===")
        logger.info(f"Request headers: {dict(self.request.headers)}")
        logger.info(f"Request body: {self.request.body}")
        
        if IS_JUPYTERHUB:
            logger.info("Detected JupyterHub environment")
            user = os.getenv('JUPYTERHUB_USER', 'default')
            logger.info(f"JupyterHub user: {user}")
        
        # Check if DISPLAY is set
        if not os.getenv('DISPLAY'):
            logger.warning("No DISPLAY environment variable set")
        
        # Check if Firefox VNC setup is already running
        if not self._is_vnc_running():
            try:
                self._setup_firefox_vnc()
            except Exception as e:
                logger.error(f"Failed to setup Firefox VNC: {str(e)}")
                error_response = {"status": "error", "error": str(e)}
                self.set_status(500)
                self.finish(error_response)
        else:
            logger.info("Firefox VNC setup is already running")
            
            # Determine web port and URL for already running instance
            if IS_JUPYTERHUB:
                user = os.getenv('JUPYTERHUB_USER', 'default')
                web_port = 6080 + (hash(user) % 100)
                service_prefix = os.getenv('JUPYTERHUB_SERVICE_PREFIX', '').rstrip('/')
                if service_prefix:
                    vnc_url = f"{service_prefix}/proxy/{web_port}/vnc.html?autoconnect=true&resize=scale"
                else:
                    vnc_url = f"http://localhost:{web_port}/vnc.html?autoconnect=true&resize=scale"
            else:
                web_port = 6080
                vnc_url = f"http://localhost:{web_port}/vnc.html?autoconnect=true&resize=scale"
            
            response_data = {"status": "already running", "url": vnc_url}
            logger.debug(f"Already running response: {response_data}")
            self.finish(response_data)

    def _is_vnc_running(self):
        """Check if VNC services are running"""
        logger.debug("Checking if VNC is running...")
        
        # Determine port to check
        if IS_JUPYTERHUB:
            user = os.getenv('JUPYTERHUB_USER', 'default')
            web_port = 6080 + (hash(user) % 100)
        else:
            web_port = 6080
        
        try:
            result = subprocess.run(["lsof", "-i", f":{web_port}"], 
                                  capture_output=True, text=True, check=True)
            logger.debug(f"VNC is running on port {web_port}")
            return True
        except subprocess.CalledProcessError:
            logger.debug(f"VNC is not running on port {web_port} (lsof returned error)")
            return False

    def _setup_firefox_vnc(self):
        """Set up Firefox with VNC access"""
        logger.info("Starting Firefox VNC setup...")
        
        # Check system dependencies
        logger.info("Checking system dependencies...")
        dependencies = ["firefox", "Xvfb", "x11vnc", "websockify"]
        for dep in dependencies:
            try:
                result = subprocess.run(["which", dep], capture_output=True, check=True)
                dep_path = result.stdout.decode().strip()
                logger.debug(f"✓ Found {dep} at {dep_path}")
            except subprocess.CalledProcessError:
                raise Exception(f"Required dependency '{dep}' not found. Please install it.")
        
        logger.info("All dependencies found")
        
        # Clean up any existing processes first
        self._cleanup_processes()
        
        # Determine display number - use user-specific display for JupyterHub
        if IS_JUPYTERHUB:
            user = os.getenv('JUPYTERHUB_USER', 'default')
            display_num = 90 + (hash(user) % 10)  # :90-:99 range
        else:
            display_num = 99
        
        display = f":{display_num}"
        logger.info(f"Using display: {display}")
        
        # Start Xvfb (Virtual Display)
        logger.info(f"Starting Xvfb on display {display}...")
        xvfb_cmd = ["Xvfb", display, "-screen", "0", "1280x720x24", "-ac", "+extension", "GLX"]
        logger.debug(f"Xvfb command: {' '.join(xvfb_cmd)}")
        
        self.xvfb_process = subprocess.Popen(
            xvfb_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info(f"Xvfb process started with PID: {self.xvfb_process.pid}")
        
        # Wait for Xvfb to start
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
            vnc_port = 5900
        
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
        
        # Determine the correct URL - for JupyterHub we need to use the proxy
        if IS_JUPYTERHUB:
            # In JupyterHub, we need to use the service prefix to create a proxied URL
            service_prefix = os.getenv('JUPYTERHUB_SERVICE_PREFIX', '').rstrip('/')
            if service_prefix:
                # Use JupyterHub's proxy system
                if novnc_path:
                    vnc_url = f"{service_prefix}/proxy/{web_port}/vnc.html?autoconnect=true&resize=scale"
                else:
                    vnc_url = f"{service_prefix}/proxy/{web_port}/"
            else:
                # Fallback to localhost
                if novnc_path:
                    vnc_url = f"http://localhost:{web_port}/vnc.html?autoconnect=true&resize=scale"
                else:
                    vnc_url = f"http://localhost:{web_port}"
        else:
            # Standalone Jupyter
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
        logger.info("Cleaning up existing processes...")
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
                vnc_port = 5900
                web_port = 6080
            
            # Kill processes by pattern (more reliable)
            cleanup_commands = [
                ["pkill", "-f", f"Xvfb.*:{display_num}"],
                ["pkill", "-f", f"x11vnc.*{vnc_port}"],
                ["pkill", "-f", f"websockify.*{web_port}"]
            ]
            
            for cmd in cleanup_commands:
                try:
                    result = subprocess.run(cmd, capture_output=True, timeout=5)
                    logger.debug(f"Cleanup command {' '.join(cmd)}: return code {result.returncode}")
                except subprocess.TimeoutExpired:
                    logger.warning(f"Cleanup command {' '.join(cmd)} timed out")
                except Exception as e:
                    logger.debug(f"Cleanup command {' '.join(cmd)} failed: {e}")
            
            # Wait for processes to terminate
            time.sleep(1)
            
        except Exception as e:
            logger.warning(f"Error during cleanup: {e}")
        
        logger.info("Process cleanup completed")


def setup_handlers(web_app):
    """Set up the Firefox launcher handlers"""
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
        logger.info("=== Firefox Launcher Extension Starting ===")
        logger.info(f"Python executable: {os.sys.executable}")
        logger.info(f"Working directory: {os.getcwd()}")
        logger.info(f"User: {os.getenv('USER', 'unknown')}")
        logger.info(f"Display: {os.getenv('DISPLAY', 'not set')}")
        logger.info(f"JUPYTERHUB_USER: {os.getenv('JUPYTERHUB_USER', 'not set')}")
        logger.info(f"JUPYTERHUB_SERVICE_PREFIX: {os.getenv('JUPYTERHUB_SERVICE_PREFIX', 'not set')}")
        logger.info(f"HOME: {os.getenv('HOME', 'not set')}")
        
        if IS_JUPYTERHUB:
            logger.info("Running in JupyterHub environment")
        else:
            logger.info("Running in standalone Jupyter environment")
            
        setup_handlers(self.serverapp.web_app)



