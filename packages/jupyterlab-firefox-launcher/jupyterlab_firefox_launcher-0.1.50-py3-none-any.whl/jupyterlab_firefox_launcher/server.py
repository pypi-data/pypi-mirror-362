import os
import subprocess
import time
import logging
from tornado import web
from jupyter_server.base.handlers import APIHandler
from jupyter_server.utils import url_path_join
from jupyter_server.extension.application import ExtensionApp
import requests
import json

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
        """Launch Firefox with direct remote debugging"""
        try:
            logger.info("=== POST request received for Firefox launcher ===")
            logger.info(f"Request headers: {dict(self.request.headers)}")
            logger.info(f"Request body: {self.request.body}")
            
            if IS_JUPYTERHUB:
                logger.info("Detected JupyterHub environment")
                user = os.getenv('JUPYTERHUB_USER', 'default')
                logger.info(f"JupyterHub user: {user}")
            
            # Check if Firefox direct debugging is already running
            if not self._is_firefox_direct_running():
                try:
                    success = self._setup_firefox_direct()
                    if not success:
                        error_response = {"status": "error", "error": "Failed to start Firefox"}
                        self.set_status(500)
                        self.finish(error_response)
                        return
                except Exception as e:
                    logger.error(f"Failed to setup Firefox direct: {str(e)}")
                    error_response = {"status": "error", "error": str(e)}
                    self.set_status(500)
                    self.finish(error_response)
                    return
            else:
                logger.info("Firefox direct debugging is already running")
                
            # Generate the direct Firefox URL
            if IS_JUPYTERHUB:
                user = os.getenv('JUPYTERHUB_USER', 'default')
                service_prefix = os.getenv('JUPYTERHUB_SERVICE_PREFIX', '').rstrip('/')
                if service_prefix:
                    # Use external domain for JupyterHub proxy URLs
                    external_host = "rats12345-0d317c8b-1cfe-423e-a518-57f97fd50c6e.vantagecompute.ai"
                    protocol = 'https'
                    firefox_url = f"{protocol}://{external_host}{service_prefix}/proxy/8888/"
                else:
                    firefox_url = "http://localhost:8888/"
            else:
                firefox_url = "http://localhost:8888/"
                
            logger.info(f"Firefox direct URL: {firefox_url}")
            
            response_data = {"status": "success", "url": firefox_url}
            logger.debug(f"Response: {response_data}")
            self.finish(response_data)
            
        except Exception as e:
            logger.error(f"Unhandled exception in POST: {str(e)}", exc_info=True)
            error_response = {"status": "error", "error": f"Unhandled exception: {str(e)}"}
            self.set_status(500)
            self.finish(error_response)

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
<html>
<head>
    <title>Firefox in JupyterLab - Working!</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; text-align: center; background: #f0f8ff; }
        h1 { color: #2e8b57; }
        .status { background: #e6ffe6; border: 2px solid #4caf50; padding: 20px; border-radius: 10px; margin: 20px; }
        .test-link { background: #2196F3; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; display: inline-block; margin: 10px; }
    </style>
</head>
<body>
    <div class="status">
        <h1>🎉 Firefox Launcher - SUCCESS!</h1>
        <p><strong>Firefox is running and displaying content properly!</strong></p>
        <p>The VNC interface and window manager are working correctly.</p>
    </div>
    
    <div>
        <h2>Network Test</h2>
        <p>Try these external links to test internet connectivity:</p>
        <a href="https://httpbin.org/json" class="test-link" target="_blank">Test API (httpbin.org)</a>
        <a href="https://www.google.com" class="test-link" target="_blank">Google</a>
        <a href="https://www.github.com" class="test-link" target="_blank">GitHub</a>
    </div>
    
    <div style="margin-top: 30px;">
        <p><strong>Instructions:</strong></p>
        <p>1. Click any link above to test external connectivity</p>
        <p>2. Or type any URL directly in Firefox's address bar</p>
        <p>3. If links show 404 errors, there may be network routing restrictions</p>
    </div>
</body>
</html>'''
        
        landing_page_path = os.path.join(profile_dir, "landing.html")
        with open(landing_page_path, 'w') as f:
            f.write(landing_page_content)
        
        # Create user.js file with minimal network configuration
        user_js_content = f'''// Minimal Firefox configuration - disable all network interception
user_pref("network.proxy.type", 0);  // Direct connection, no proxy
user_pref("browser.startup.homepage", "about:config");
user_pref("browser.startup.page", 1);
user_pref("browser.newtabpage.enabled", false);
user_pref("browser.newtab.url", "about:blank");
user_pref("security.fileuri.strict_origin_policy", false);
user_pref("dom.security.https_only_mode", false);
user_pref("network.http.sendOriginHeader", 0);
user_pref("browser.safebrowsing.enabled", false);
user_pref("browser.safebrowsing.malware.enabled", false);
user_pref("datareporting.healthreport.uploadEnabled", false);
user_pref("toolkit.telemetry.enabled", false);
user_pref("browser.ping-centre.telemetry", false);
user_pref("browser.urlbar.suggest.searches", false);
user_pref("browser.search.suggest.enabled", false);
user_pref("network.prefetch-next", false);
user_pref("network.dns.disablePrefetch", true);
user_pref("network.http.speculative-parallel-limit", 0);
'''
        
        user_js_path = os.path.join(profile_dir, "user.js")
        with open(user_js_path, 'w') as f:
            f.write(user_js_content)
        
        logger.info(f"Created Firefox profile at: {profile_dir}")
        logger.info(f"Landing page created at: {landing_page_path}")
        
        # Verify the file was created
        if os.path.exists(landing_page_path):
            logger.info("✅ Landing page file created successfully")
        else:
            logger.error("❌ Failed to create landing page file")
        
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
        
        # Start Firefox on the virtual display with about:config (internal page that should always work)
        firefox_cmd = [
            "firefox", 
            "--new-instance", 
            "--no-remote",
            "--profile", profile_dir,
            "--safe-mode",
            "about:config"
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
        logger.info("Starting Firefox with about:config (safe mode)")
        
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


class VNCProxyHandler(APIHandler):
    """Handler to proxy VNC connections through JupyterLab's API"""
    
    @web.authenticated
    def get(self):
        """Proxy VNC web interface"""
        logger.info("VNC Proxy request received")
        
        # Check if VNC service is accessible
        try:
            import urllib.request
            urllib.request.urlopen('http://localhost:6080/', timeout=5)
            vnc_status = "VNC service is accessible"
        except:
            vnc_status = "VNC service not accessible"
        
        # Serve a redirect to the VNC service through JupyterHub proxy
        self.set_header('Content-Type', 'text/html')
        
        html = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Firefox VNC Access</title>
            <style>
                body {{ 
                    margin: 0; 
                    padding: 20px; 
                    font-family: Arial, sans-serif;
                    background: #f5f5f5;
                }}
                .container {{
                    max-width: 800px;
                    margin: 0 auto;
                    background: white;
                    padding: 30px;
                    border-radius: 8px;
                    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                }}
                .status {{
                    background: #d4edda;
                    border: 1px solid #c3e6cb;
                    padding: 15px;
                    border-radius: 5px;
                    margin-bottom: 20px;
                }}
                .controls {{
                    display: flex;
                    gap: 10px;
                    margin-bottom: 20px;
                }}
                button {{
                    padding: 12px 20px;
                    background: #007bff;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 14px;
                }}
                button:hover {{ background: #0056b3; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🦊 Firefox VNC Access</h1>
                
                <div class="status">
                    ✅ <strong>Status:</strong> {vnc_status}
                </div>
                
                <div class="controls">
                    <button onclick="openVNCDirect()">🚀 Open Firefox VNC</button>
                    <button onclick="openVNCNewTab()">🔗 Open in New Tab</button>
                </div>
                
                <div style="background: #e9ecef; padding: 15px; border-radius: 5px;">
                    <h3>Access Methods:</h3>
                    <p><strong>Direct VNC URL:</strong> <a href="http://localhost:6080/vnc.html" target="_blank">http://localhost:6080/vnc.html</a></p>
                    <p><strong>VNC with auto-connect:</strong> <a href="http://localhost:6080/vnc.html?autoconnect=true&resize=scale" target="_blank">Auto-connect link</a></p>
                </div>
            </div>

            <script>
                function openVNCDirect() {{
                    window.location.href = 'http://localhost:6080/vnc.html?autoconnect=true&resize=scale';
                }}
                
                function openVNCNewTab() {{
                    window.open('http://localhost:6080/vnc.html?autoconnect=true&resize=scale', '_blank');
                }}
                
                // Auto-redirect to VNC after 2 seconds
                setTimeout(function() {{
                    openVNCDirect();
                }}, 2000);
            </script>
        </body>
        </html>
        '''
        self.write(html)
        self.finish()

    def _setup_firefox_direct(self):
        """Setup Firefox with direct remote debugging (no VNC)"""
        logger.info("Setting up Firefox with direct remote debugging...")
        
        try:
            # Clean up any existing Firefox processes
            subprocess.run(['pkill', '-f', 'firefox'], check=False, timeout=10)
            time.sleep(2)
            
            # Create Firefox profile directory
            profile_dir = "/tmp/firefox_profile_direct"
            os.makedirs(profile_dir, exist_ok=True)
            logger.info(f"Firefox profile directory: {profile_dir}")
            
            # Start Firefox with remote debugging on a different port
            firefox_cmd = [
                'firefox',
                '--new-instance',
                '--profile', profile_dir,
                '--remote-debugging-port=8888',
                '--remote-allow-origins=*',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--no-sandbox',
                '--start-maximized',
                '--no-first-run',
                '--disable-default-apps',
                'https://www.google.com'
            ]
            
            logger.info(f"Starting Firefox with command: {' '.join(firefox_cmd)}")
            
            # Start Firefox process
            firefox_process = subprocess.Popen(
                firefox_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=dict(os.environ, DISPLAY=':0')  # Use default display
            )
            
            # Wait for Firefox to start
            time.sleep(5)
            
            # Check if Firefox is running
            if firefox_process.poll() is None:
                logger.info(f"✅ Firefox started successfully (PID: {firefox_process.pid})")
                
                # Register proxy route with JupyterHub if in JupyterHub environment
                if IS_JUPYTERHUB:
                    target_url = "http://localhost:8888"
                    self._register_jupyterhub_proxy(8888, target_url)
                
                # Test if debug port is accessible
                try:
                    import urllib.request
                    urllib.request.urlopen('http://localhost:8888/json', timeout=5)
                    logger.info("✅ Firefox remote debugging port is accessible")
                    return True
                except Exception as e:
                    logger.warning(f"Firefox debug port not accessible: {e}")
                    return True  # Firefox might still be starting
                    
            else:
                stdout, stderr = firefox_process.communicate(timeout=5)
                logger.error(f"❌ Firefox failed to start")
                logger.error(f"Firefox stdout: {stdout.decode()}")
                logger.error(f"Firefox stderr: {stderr.decode()}")
                return False
                
        except Exception as e:
            logger.error(f"Exception in Firefox direct setup: {str(e)}")
            return False

    def _is_firefox_direct_running(self):
        """Check if Firefox with remote debugging is running"""
        try:
            # Check if debug port is accessible
            import urllib.request
            urllib.request.urlopen('http://localhost:8888/json', timeout=2)
            logger.info("Firefox direct debugging is already running")
            return True
        except:
            logger.info("Firefox direct debugging is not running")
            return False

    def _register_jupyterhub_proxy(self, port, target_url):
        """Register a proxy route with JupyterHub's configurable-http-proxy"""
        logger.info(f"Registering JupyterHub proxy route: port {port} -> {target_url}")
        
        try:
            # Get JupyterHub API token and URL
            api_token = os.getenv('JUPYTERHUB_API_TOKEN')
            hub_url = os.getenv('JUPYTERHUB_URL', 'http://hub:8081')
            user = os.getenv('JUPYTERHUB_USER')
            server_name = os.getenv('JUPYTERHUB_SERVER_NAME', '')
            
            if not api_token:
                logger.warning("No JUPYTERHUB_API_TOKEN found, cannot register proxy route")
                return False
                
            # Construct the proxy route path
            if server_name:
                route_path = f"/user/{user}/{server_name}/proxy/{port}"
            else:
                route_path = f"/user/{user}/proxy/{port}"
                
            # Register with JupyterHub proxy API
            proxy_api_url = f"{hub_url}/hub/api/proxy"
            headers = {
                'Authorization': f'token {api_token}',
                'Content-Type': 'application/json'
            }
            
            proxy_data = {
                'target': target_url,
                'jupyterhub': True
            }
            
            # Make the API call to register the route
            response = requests.post(
                f"{proxy_api_url}{route_path}",
                headers=headers,
                json=proxy_data,
                timeout=10
            )
            
            if response.status_code in [201, 202]:
                logger.info(f"✅ Successfully registered proxy route: {route_path} -> {target_url}")
                return True
            else:
                logger.error(f"❌ Failed to register proxy route: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Exception registering JupyterHub proxy: {e}")
            return False

def setup_handlers(web_app):
    """Set up the Firefox launcher handlers"""
    logger.info("Setting up Firefox launcher handlers...")
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    
    # Main launcher route
    route_pattern = url_path_join(base_url, "jupyterlab-firefox-launcher", "launch")
    logger.info(f"Registering route: {route_pattern}")
    
    # VNC proxy route - simpler pattern without capture group
    vnc_route_pattern = url_path_join(base_url, "jupyterlab-firefox-launcher", "vnc")
    logger.info(f"Registering VNC proxy route: {vnc_route_pattern}")
    
    handlers = [
        (route_pattern, FirefoxLauncherHandler),
        (vnc_route_pattern, VNCProxyHandler)
    ]
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

if __name__ == "__main__":
    import argparse
    import sys
    
    # Set up basic logging
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    parser = argparse.ArgumentParser(description='Firefox Launcher Server')
    parser.add_argument('--port', type=int, default=8877, help='Port to run the server on')
    parser.add_argument('--host', default='localhost', help='Host to bind to')
    args = parser.parse_args()
    
    print(f"Starting Firefox Launcher Server on {args.host}:{args.port}")
    print(f"Direct Firefox debugging will be available on port 8888")
    print("Press Ctrl+C to stop")
    
    try:
        # Create a minimal Tornado application
        import tornado.web
        import tornado.ioloop
        
        app = tornado.web.Application([
            (r"/firefox", FirefoxLauncherHandler),
            (r"/vnc", VNCProxyHandler),
        ])
        
        app.listen(args.port, args.host)
        print(f"✅ Server started successfully at http://{args.host}:{args.port}")
        print("Endpoints:")
        print(f"  - Firefox launcher: http://{args.host}:{args.port}/firefox")
        print(f"  - Status check: http://{args.host}:{args.port}/status")
        
        tornado.ioloop.IOLoop.current().start()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)



