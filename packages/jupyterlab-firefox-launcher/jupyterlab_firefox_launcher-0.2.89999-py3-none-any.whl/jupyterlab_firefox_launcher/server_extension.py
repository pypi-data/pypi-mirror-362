from pathlib import Path
import subprocess
import os
import time
import psutil
import socket
from tornado import web
from tornado.web import HTTPError
from tornado.httpclient import AsyncHTTPClient

from jupyter_server.base.handlers import AuthenticatedFileHandler, JupyterHandler
from jupyter_server.utils import url_path_join

from .handlers import FirefoxHandler

HERE = Path(__file__).parent


def is_port_open(host, port):
    """Check if a port is open"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            return result == 0
    except:
        return False


class SimpleProxyHandler(JupyterHandler):
    """Simple proxy handler for Xpra"""
    
    async def get(self, path):
        """Proxy GET requests to Xpra"""
        # Ensure Xpra is running before proxying
        if not is_port_open("127.0.0.1", 15555):
            print("Xpra not running, attempting to start...")
            if not start_xpra():
                self.set_status(503)
                self.write("Firefox service is not available. Please try again in a moment.")
                return
        
        client = AsyncHTTPClient()
        url = f"http://127.0.0.1:15555/{path}"
        
        try:
            response = await client.fetch(url, method="GET", request_timeout=10)
            for header_name, header_value in response.headers.get_all():
                if header_name.lower() not in ['content-length', 'transfer-encoding']:
                    self.set_header(header_name, header_value)
            self.write(response.body)
        except Exception as e:
            self.set_status(502)
            self.write(f"Firefox service temporarily unavailable: {e}")
        finally:
            client.close()

    async def post(self, path):
        """Proxy POST requests to Xpra"""
        # Ensure Xpra is running before proxying
        if not is_port_open("127.0.0.1", 15555):
            print("Xpra not running, attempting to start...")
            if not start_xpra():
                self.set_status(503)
                self.write("Firefox service is not available. Please try again in a moment.")
                return
                
        client = AsyncHTTPClient()
        url = f"http://127.0.0.1:15555/{path}"
        
        try:
            response = await client.fetch(
                url, 
                method="POST",
                body=self.request.body,
                headers=self.request.headers,
                request_timeout=10
            )
            for header_name, header_value in response.headers.get_all():
                if header_name.lower() not in ['content-length', 'transfer-encoding']:
                    self.set_header(header_name, header_value)
            self.write(response.body)
        except Exception as e:
            self.set_status(502)
            self.write(f"Firefox service temporarily unavailable: {e}")
        finally:
            client.close()


class AddSlashHandler(JupyterHandler):
    """Add trailing slash handler"""
    
    def get(self):
        """Redirect to URL with trailing slash"""
        self.redirect(self.request.uri + "/")


def start_xpra():
    """Start Xpra server if not already running."""
    # Check if Xpra is already running on the port
    if is_port_open("127.0.0.1", 15555):
        print("Xpra already running on port 15555")
        return True
    
    # Check if Xpra process is running
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'xpra' and '--html=on' in proc.info['cmdline']:
                print("Xpra process found but port not open, waiting...")
                for i in range(10):  # Wait up to 10 seconds
                    time.sleep(1)
                    if is_port_open("127.0.0.1", 15555):
                        return True
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Start new Xpra server
    port = 15555
    print(f"Starting Xpra server on port {port}...")
    cmd = [
        'xpra', 'start', 
        f'--bind-tcp=0.0.0.0:{port}',
        '--html=on',
        '--start=firefox',
        '--exit-with-children=yes',
        '--daemon=yes',
        # Disable Xpra controls overlay
        '--html-hide-controls=yes',
        '--html-hide-fullscreen=yes',
        '--html-hide-keyboard=yes',
        '--html-hide-menu=yes',
        '--html-hide-clipboard=yes',
        '--html-hide-sound=yes',
        '--html-hide-video=yes',
        '--html-hide-printing=yes',
        # Additional clean interface options
        '--html-no-virtual-keyboard=yes',
        '--html-no-context-menu=yes',
    ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"Xpra start command output: {result.stdout}")
        
        # Wait for Xpra to be ready
        for i in range(15):  # Wait up to 15 seconds
            time.sleep(1)
            if is_port_open("127.0.0.1", 15555):
                print(f"Xpra ready on port {port}")
                return True
            print(f"Waiting for Xpra to start... ({i+1}/15)")
        
        print("Xpra failed to start within timeout")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Xpra: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error starting Xpra: {e}")
        return False


def load_jupyter_server_extension(server_app):
    """
    Called during notebook start
    """
    base_url = server_app.web_app.settings["base_url"]
    
    server_app.log.info("Loading jupyterlab_firefox_launcher server extension...")
    
    # Start Xpra when the server extension loads
    success = start_xpra()
    if success:
        server_app.log.info("Xpra started successfully")
    else:
        server_app.log.warning("Failed to start Xpra - it will be started on first request")

    server_app.web_app.add_handlers(
        ".*",
        [
            # Serve our own static files if we have any
            (
                url_path_join(base_url, "/firefox/static/(.*)"),
                AuthenticatedFileHandler,
                {"path": (str(HERE / "static"))},
            ),
            # Proxy to Xpra
            (
                url_path_join(base_url, "/proxy/firefox/(.*)"),
                SimpleProxyHandler,
            ),
            # To simplify URL mapping, we make sure that /firefox/ always
            # has a trailing slash
            (url_path_join(base_url, "/firefox"), AddSlashHandler),
            (url_path_join(base_url, "/firefox/"), FirefoxHandler),
        ],
    )
    
    server_app.log.info("Firefox launcher extension loaded successfully")
