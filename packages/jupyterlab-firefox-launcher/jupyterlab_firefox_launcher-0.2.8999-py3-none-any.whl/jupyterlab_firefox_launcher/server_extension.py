from pathlib import Path
import subprocess
import os
import time
import psutil
from tornado import web
from tornado.web import HTTPError
from tornado.httpclient import AsyncHTTPClient

from jupyter_server.base.handlers import AuthenticatedFileHandler, JupyterHandler
from jupyter_server.utils import url_path_join

from .handlers import FirefoxHandler

HERE = Path(__file__).parent


class SimpleProxyHandler(JupyterHandler):
    """Simple proxy handler for Xpra"""
    
    async def get(self, path):
        """Proxy GET requests to Xpra"""
        client = AsyncHTTPClient()
        url = f"http://127.0.0.1:15555/{path}"
        
        try:
            response = await client.fetch(url, method="GET")
            self.set_header("Content-Type", response.headers.get("Content-Type", "text/html"))
            self.write(response.body)
        except Exception as e:
            self.set_status(502)
            self.write(f"Proxy error: {e}")
        finally:
            client.close()

    async def post(self, path):
        """Proxy POST requests to Xpra"""
        client = AsyncHTTPClient()
        url = f"http://127.0.0.1:15555/{path}"
        
        try:
            response = await client.fetch(
                url, 
                method="POST",
                body=self.request.body,
                headers=self.request.headers
            )
            self.set_header("Content-Type", response.headers.get("Content-Type", "text/html"))
            self.write(response.body)
        except Exception as e:
            self.set_status(502)
            self.write(f"Proxy error: {e}")
        finally:
            client.close()


class AddSlashHandler(JupyterHandler):
    """Add trailing slash handler"""
    
    def get(self):
        """Redirect to URL with trailing slash"""
        self.redirect(self.request.uri + "/")


def start_xpra():
    """Start Xpra server if not already running."""
    # Check if Xpra is already running
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'xpra' and '--html=on' in proc.info['cmdline']:
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    # Start new Xpra server
    port = 15555
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
        subprocess.run(cmd, check=True)
        time.sleep(3)  # Give Xpra time to start
        return True
    except Exception as e:
        print(f"Failed to start Xpra: {e}")
        return False


def load_jupyter_server_extension(server_app):
    """
    Called during notebook start
    """
    base_url = server_app.web_app.settings["base_url"]
    
    # Start Xpra when the server extension loads
    start_xpra()

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
    
    server_app.log.info("Loaded jupyterlab_firefox_launcher server extension")
