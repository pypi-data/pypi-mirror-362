from pathlib import Path
import subprocess
import os
import time
import psutil
import socket
import random
from tornado import web
from tornado.web import HTTPError
from tornado.httpclient import AsyncHTTPClient

from jupyter_server.base.handlers import AuthenticatedFileHandler, JupyterHandler
from jupyter_server.utils import url_path_join

from .handlers import FirefoxHandler

HERE = Path(__file__).parent

# Global dictionary to track Xpra sessions
xpra_sessions = {}


def get_free_port():
    """Get a free port for Xpra"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def is_port_open(host, port):
    """Check if a port is open"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            return result == 0
    except:
        return False


class FirefoxSessionHandler(JupyterHandler):
    """Handle Firefox session lifecycle"""
    
    @web.authenticated
    async def get(self):
        """Get session status - for testing authentication"""
        self.log.info("Firefox session status requested")
        self.write({
            "status": "authenticated",
            "sessions": list(xpra_sessions.keys())
        })
    
    @web.authenticated
    async def post(self):
        """Start a new Firefox session"""
        self.log.info("Creating new Firefox session...")
        session_id = f"firefox_{random.randint(1000, 9999)}"
        port = get_free_port()
        
        self.log.info(f"Starting Xpra session {session_id} on port {port}")
        success = start_xpra_session(session_id, port)
        if success:
            self.log.info(f"Successfully started Firefox session {session_id}")
            self.write({
                "session_id": session_id,
                "port": port,
                "status": "started"
            })
        else:
            self.log.error(f"Failed to start Firefox session {session_id}")
            self.set_status(500)
            self.write({"error": "Failed to start Firefox session"})
    
    @web.authenticated
    async def delete(self, session_id):
        """Stop a Firefox session"""
        self.log.info(f"Stopping Firefox session {session_id}")
        success = stop_xpra_session(session_id)
        if success:
            self.log.info(f"Successfully stopped Firefox session {session_id}")
            self.write({"status": "stopped"})
        else:
            self.log.error(f"Failed to stop Firefox session {session_id} - session not found")
            self.set_status(404)
            self.write({"error": "Session not found"})


class SimpleProxyHandler(JupyterHandler):
    """Simple proxy handler for Xpra"""
    
    async def get(self, session_id, path):
        """Proxy GET requests to Xpra session"""
        if session_id not in xpra_sessions:
            self.set_status(404)
            self.write("Firefox session not found")
            return
            
        port = xpra_sessions[session_id]["port"]
        
        # Check if session is still running
        if not is_port_open("127.0.0.1", port):
            self.set_status(503)
            self.write("Firefox session is not running")
            return
        
        client = AsyncHTTPClient()
        url = f"http://127.0.0.1:{port}/{path}"
        
        try:
            response = await client.fetch(url, method="GET", request_timeout=10)
            for header_name, header_value in response.headers.get_all():
                if header_name.lower() not in ['content-length', 'transfer-encoding']:
                    self.set_header(header_name, header_value)
            self.write(response.body)
        except Exception as e:
            self.set_status(502)
            self.write(f"Firefox session error: {e}")
        finally:
            client.close()

    async def post(self, session_id, path):
        """Proxy POST requests to Xpra session"""
        if session_id not in xpra_sessions:
            self.set_status(404)
            self.write("Firefox session not found")
            return
            
        port = xpra_sessions[session_id]["port"]
        
        if not is_port_open("127.0.0.1", port):
            self.set_status(503)
            self.write("Firefox session is not running")
            return
                
        client = AsyncHTTPClient()
        url = f"http://127.0.0.1:{port}/{path}"
        
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
            self.write(f"Firefox session error: {e}")
        finally:
            client.close()


class AddSlashHandler(JupyterHandler):
    """Add trailing slash handler"""
    
    def get(self):
        """Redirect to URL with trailing slash"""
        self.redirect(self.request.uri + "/")


def start_xpra_session(session_id, port):
    """Start a new Xpra session"""
    print(f"Starting Xpra session {session_id} on port {port}...")
    
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
        print(f"Xpra session {session_id} start output: {result.stdout}")
        
        # Wait for Xpra to be ready
        for i in range(15):  # Wait up to 15 seconds
            time.sleep(1)
            if is_port_open("127.0.0.1", port):
                print(f"Xpra session {session_id} ready on port {port}")
                xpra_sessions[session_id] = {
                    "port": port,
                    "started": time.time(),
                    "process": None  # We could store process info here
                }
                return True
            print(f"Waiting for Xpra session {session_id} to start... ({i+1}/15)")
        
        print(f"Xpra session {session_id} failed to start within timeout")
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Xpra session {session_id}: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Unexpected error starting Xpra session {session_id}: {e}")
        return False


def stop_xpra_session(session_id):
    """Stop an Xpra session"""
    if session_id not in xpra_sessions:
        return False
    
    port = xpra_sessions[session_id]["port"]
    print(f"Stopping Xpra session {session_id} on port {port}...")
    
    # Find and kill the Xpra process
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if (proc.info['name'] == 'xpra' and 
                f'--bind-tcp=0.0.0.0:{port}' in proc.info['cmdline']):
                proc.terminate()
                # Wait for graceful shutdown
                try:
                    proc.wait(timeout=5)
                except psutil.TimeoutExpired:
                    proc.kill()  # Force kill if it doesn't terminate
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Remove from sessions
    del xpra_sessions[session_id]
    print(f"Xpra session {session_id} stopped")
    return True


def load_jupyter_server_extension(server_app):
    """
    Called during notebook start
    """
    base_url = server_app.web_app.settings["base_url"]
    
    server_app.log.info("Loading jupyterlab_firefox_launcher server extension...")

    server_app.web_app.add_handlers(
        ".*",
        [
            # Session management endpoints
            (
                url_path_join(base_url, "/firefox/session"),
                FirefoxSessionHandler,
            ),
            (
                url_path_join(base_url, "/firefox/session/(.+)"),
                FirefoxSessionHandler,
            ),
            # Serve our own static files if we have any
            (
                url_path_join(base_url, "/firefox/static/(.*)"),
                AuthenticatedFileHandler,
                {"path": (str(HERE / "static"))},
            ),
            # Proxy to Xpra sessions
            (
                url_path_join(base_url, "/proxy/firefox/(.+)/(.*)"),
                SimpleProxyHandler,
            ),
            # To simplify URL mapping, we make sure that /firefox/ always
            # has a trailing slash
            (url_path_join(base_url, "/firefox"), AddSlashHandler),
            (url_path_join(base_url, "/firefox/"), FirefoxHandler),
        ],
    )
    
    server_app.log.info("Firefox launcher extension loaded successfully")
