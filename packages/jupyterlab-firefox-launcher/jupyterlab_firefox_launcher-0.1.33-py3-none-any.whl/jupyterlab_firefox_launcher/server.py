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
                    # Use external domain for JupyterHub proxy URLs
                    external_host = "rats12345-0d317c8b-1cfe-423e-a518-57f97fd50c6e.vantagecompute.ai"
                    protocol = 'https'
                    vnc_url = f"{protocol}://{external_host}{service_prefix}/proxy/{web_port}/vnc.html?autoconnect=true&resize=scale"
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

    def _create_firefox_profile(self):
        """Create a custom Firefox profile with proper network settings"""
        import tempfile
        
        # Create a temporary profile directory
        profile_dir = tempfile.mkdtemp(prefix="firefox_profile_")
        
        # Create a simple HTML landing page
        landing_page_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Firefox Launcher</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; }
        h1 { color: #333; text-align: center; }
        .quick-links { margin: 20px 0; }
        .quick-links a { 
            display: inline-block; margin: 10px; padding: 10px 20px; 
            background: #0078d4; color: white; text-decoration: none; border-radius: 5px; 
        }
        .quick-links a:hover { background: #106ebe; }
        .url-bar { margin: 20px 0; text-align: center; }
        .url-bar input { padding: 10px; width: 300px; border: 1px solid #ccc; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🦊 Firefox in JupyterLab</h1>
        <p>Welcome! Firefox is running successfully. Try these links or enter a URL in the address bar above:</p>
        
        <div class="quick-links">
            <a href="https://www.google.com" target="_blank">Google</a>
            <a href="https://www.github.com" target="_blank">GitHub</a>
            <a href="https://www.stackoverflow.com" target="_blank">Stack Overflow</a>
            <a href="https://www.wikipedia.org" target="_blank">Wikipedia</a>
        </div>
        
        <div class="url-bar">
            <p><strong>Quick test:</strong> Click any link above or type a URL in Firefox's address bar</p>
        </div>
    </div>
</body>
</html>'''
        
        landing_page_path = os.path.join(profile_dir, "landing.html")
        with open(landing_page_path, 'w') as f:
            f.write(landing_page_content)
        
        # Create user.js file with network configuration
        user_js_content = f'''// Network configuration for Firefox in VNC environment
user_pref("network.proxy.type", 0);  // Direct connection, no proxy
user_pref("network.proxy.http", "");
user_pref("network.proxy.http_port", 0);
user_pref("network.proxy.ssl", "");
user_pref("network.proxy.ssl_port", 0);
user_pref("network.proxy.ftp", "");
user_pref("network.proxy.ftp_port", 0);
user_pref("network.proxy.socks", "");
user_pref("network.proxy.socks_port", 0);
user_pref("network.proxy.no_proxies_on", "");
user_pref("network.proxy.autoconfig_url", "");
user_pref("network.proxy.share_proxy_settings", false);
user_pref("network.dns.disableIPv6", false);
user_pref("browser.startup.homepage", "about:blank");
user_pref("browser.startup.page", 0);  // Start with blank page, not homepage
user_pref("security.tls.insecure_fallback_hosts", "localhost");
user_pref("network.stricttransportsecurity.preloadlist", false);
user_pref("security.mixed_content.block_active_content", false);
user_pref("security.mixed_content.block_display_content", false);
user_pref("dom.security.https_only_mode", false);
user_pref("browser.safebrowsing.enabled", false);
user_pref("browser.safebrowsing.malware.enabled", false);
user_pref("network.cookie.cookieBehavior", 0);
user_pref("privacy.trackingprotection.enabled", false);
user_pref("network.http.proxy.respect-be-conservative", false);
user_pref("network.http.proxy.version", "1.1");
user_pref("network.dns.blockDotOnion", false);
user_pref("network.http.sendOriginHeader", 0);
user_pref("security.fileuri.strict_origin_policy", false);
user_pref("network.http.phishy-userpass-length", 255);
user_pref("network.automatic-ntlm-auth.allow-proxies", false);
user_pref("network.http.proxy.pipelining", false);
user_pref("browser.cache.disk.enable", false);
user_pref("browser.cache.memory.enable", false);
user_pref("devtools.console.stdout.chrome", true);
'''
        
        user_js_path = os.path.join(profile_dir, "user.js")
        with open(user_js_path, 'w') as f:
            f.write(user_js_content)
        
        logger.info(f"Created Firefox profile at: {profile_dir}")
        return profile_dir

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
        
        logger.info("Websockify started successfully, starting window manager and Firefox...")
        
        # Start a lightweight window manager first (essential for Firefox to display properly)
        wm_cmd = None
        for wm in ["fluxbox", "openbox", "twm"]:
            try:
                # Check if window manager is available
                subprocess.check_output(["which", wm], stderr=subprocess.DEVNULL)
                wm_cmd = [wm]
                break
            except subprocess.CalledProcessError:
                continue
        
        if wm_cmd:
            logger.info(f"Starting window manager: {' '.join(wm_cmd)}")
            wm_env = {**os.environ, "DISPLAY": display}
            wm_process = subprocess.Popen(
                wm_cmd,
                env=wm_env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            logger.info(f"Window manager started with PID: {wm_process.pid}")
            time.sleep(2)  # Give window manager time to start
        else:
            logger.warning("No suitable window manager found (fluxbox, openbox, twm)")
        
        # Create a custom Firefox profile with proper network settings
        profile_dir = self._create_firefox_profile()
        
        # Start Firefox on the virtual display with a local landing page
        landing_page = os.path.join(profile_dir, "landing.html")
        firefox_cmd = [
            "firefox", 
            "--new-instance", 
            "--no-remote",
            "--profile", profile_dir,
            "--disable-web-security",
            "--disable-features=TranslateUI",
            "--disable-ipc-flooding-protection",
            "data:text/html,<h1 style='color: green; text-align: center; font-family: Arial;'>🎉 Firefox Started Successfully!</h1><div style='text-align: center; margin: 20px;'><p>Network test: <a href='https://httpbin.org/json' target='_blank'>Click here to test external connectivity</a></p><p>Or type any URL in the address bar above!</p></div>"
        ]
        
        # Set up environment with proper network configuration
        firefox_env = {
            **os.environ, 
            "DISPLAY": display,
            "MOZ_HEADLESS": "0",  # Ensure GUI mode
            "MOZ_DISABLE_CONTENT_SANDBOX": "1",  # Disable sandboxing that might block network
            "http_proxy": "",  # Explicitly disable proxy
            "https_proxy": "",
            "HTTP_PROXY": "",
            "HTTPS_PROXY": "",
            "no_proxy": "*",
            "NO_PROXY": "*"
        }
        
        logger.debug(f"Firefox command: {' '.join(firefox_cmd)}")
        logger.debug(f"Firefox environment DISPLAY: {firefox_env.get('DISPLAY')}")
        
        firefox_process = subprocess.Popen(
            firefox_cmd,
            env=firefox_env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        logger.info(f"Firefox process started with PID: {firefox_process.pid}")
        
        # Test network connectivity from Firefox's perspective
        logger.info("Testing network connectivity...")
        try:
            import subprocess
            test_result = subprocess.run(
                ["curl", "-s", "-I", "--connect-timeout", "3", "https://httpbin.org/status/200"],
                capture_output=True, text=True, timeout=5
            )
            if test_result.returncode == 0:
                logger.info("✅ Network connectivity test passed")
            else:
                logger.warning(f"❌ Network connectivity test failed: {test_result.stderr}")
        except Exception as e:
            logger.warning(f"Network test error: {e}")
        
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
                # Use external domain for JupyterHub proxy URLs
                # For now, use the known external domain - in production this should be detected
                external_host = "rats12345-0d317c8b-1cfe-423e-a518-57f97fd50c6e.vantagecompute.ai"
                protocol = 'https'
                
                # Use JupyterHub's proxy system with external URL
                if novnc_path:
                    vnc_url = f"{protocol}://{external_host}{service_prefix}/proxy/{web_port}/vnc.html?autoconnect=true&resize=scale"
                else:
                    vnc_url = f"{protocol}://{external_host}{service_prefix}/proxy/{web_port}/"
                    
                logger.debug(f"Built external JupyterHub URL: {vnc_url}")
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



