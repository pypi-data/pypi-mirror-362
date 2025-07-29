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
logger = logging.getLogger("Firefox Launcher")

# Check if running in JupyterHub environment
IS_JUPYTERHUB = bool(os.getenv('JUPYTERHUB_USER') or os.getenv('JUPYTERHUB_SERVICE_PREFIX'))

class FirefoxLauncherHandler(web.RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xvfb_process = None
        self.vnc_process = None
        self.novnc_process = None
        logger.info("FirefoxLauncherHandler initialized")

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
        
        self.set_header("Content-Type", "application/json")
        self.write(json.dumps(debug_info))
        self.finish()

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
                        self.set_header("Content-Type", "application/json")
                        self.write(json.dumps(error_response))
                        self.finish()
                        return
                except Exception as e:
                    logger.error(f"Failed to setup Firefox direct: {str(e)}")
                    error_response = {"status": "error", "error": str(e)}
                    self.set_status(500)
                    self.set_header("Content-Type", "application/json")
                    self.write(json.dumps(error_response))
                    self.finish()
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
            
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(response_data))
            self.finish()
            
        except Exception as e:
            logger.error(f"Unhandled exception in POST: {str(e)}", exc_info=True)
            error_response = {"status": "error", "error": f"Unhandled exception: {str(e)}"}
            self.set_status(500)
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(error_response))
            self.finish()

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
            
            # Start Firefox with remote debugging on port 8888 (headless mode)
            firefox_cmd = [
                'firefox',
                '--headless',  # Run in headless mode for no display environment
                '--new-instance',
                '--profile', profile_dir,
                '--remote-debugging-port=8888',
                '--remote-allow-origins=*',
                '--disable-web-security',
                '--disable-features=VizDisplayCompositor',
                '--no-sandbox',
                '--disable-gpu',  # Disable GPU for headless mode
                '--no-first-run',
                '--disable-default-apps',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                'https://www.google.com'
            ]
            
            logger.info(f"Starting Firefox with command: {' '.join(firefox_cmd)}")
            
            # Start Firefox process (no display environment needed for headless)
            firefox_process = subprocess.Popen(
                firefox_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
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
    
    def _register_jupyterhub_proxy(self, port, target_url):
        """Register a service with JupyterHub's configurable-http-proxy"""
        try:
            user = os.getenv('JUPYTERHUB_USER', 'default')
            service_prefix = os.getenv('JUPYTERHUB_SERVICE_PREFIX', '').rstrip('/')
            api_token = os.getenv('JUPYTERHUB_API_TOKEN', '')
            
            if not api_token:
                logger.warning("No JupyterHub API token available, skipping proxy registration")
                return False
            
            # JupyterHub API endpoint for proxy routes
            hub_api_url = os.getenv('JUPYTERHUB_API_URL', 'http://localhost:8081/hub/api')
            proxy_api_url = f"{hub_api_url}/proxy"
            
            # Route path for the proxy
            route_path = f"{service_prefix}/proxy/{port}/"
            
            # Register the route
            headers = {
                'Authorization': f'token {api_token}',
                'Content-Type': 'application/json'
            }
            
            data = {
                'target': target_url,
                'path': route_path
            }
            
            logger.info(f"Registering proxy route: {route_path} -> {target_url}")
            response = requests.post(f"{proxy_api_url}", headers=headers, json=data, timeout=10)
            
            if response.status_code in [200, 201]:
                logger.info(f"✅ Successfully registered proxy route for port {port}")
                return True
            else:
                logger.error(f"❌ Failed to register proxy route: {response.status_code} {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Exception registering JupyterHub proxy: {str(e)}")
            return False


class VNCProxyHandler(web.RequestHandler):
    """Handler to proxy VNC connections through JupyterLab's API"""
    
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
        </head>
        <body>
            <h1>🦊 Firefox VNC Access</h1>
            <p><strong>Status:</strong> {vnc_status}</p>
            <p><a href="http://localhost:6080/vnc.html" target="_blank">Open VNC</a></p>
        </body>
        </html>
        '''
        self.write(html)
        self.finish()


def setup_handlers(web_app):
    """Setup the extension handlers"""
    logger.info("Setting up Firefox launcher handlers")
    
    # Define handler patterns
    handlers = [
        (r"/firefox-launcher/firefox", FirefoxLauncherHandler),
        (r"/firefox-launcher/vnc", VNCProxyHandler),
    ]
    
    # Add handlers to the web app
    for pattern, handler_class in handlers:
        web_app.add_handlers(".*$", [(pattern, handler_class)])
        logger.info(f"Added handler: {pattern}")


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
        import secrets
        
        # Application settings for Jupyter compatibility
        settings = {
            'cookie_secret': secrets.token_bytes(32),
            'identity_provider': None,  # Disable identity provider for standalone mode
        }
        
        app = tornado.web.Application([
            (r"/firefox", FirefoxLauncherHandler),
            (r"/vnc", VNCProxyHandler),
        ], **settings)
        
        app.listen(args.port, args.host)
        print(f"✅ Server started successfully at http://{args.host}:{args.port}")
        print("Endpoints:")
        print(f"  - Firefox launcher: http://{args.host}:{args.port}/firefox")
        print(f"  - VNC proxy: http://{args.host}:{args.port}/vnc")
        
        tornado.ioloop.IOLoop.current().start()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)
