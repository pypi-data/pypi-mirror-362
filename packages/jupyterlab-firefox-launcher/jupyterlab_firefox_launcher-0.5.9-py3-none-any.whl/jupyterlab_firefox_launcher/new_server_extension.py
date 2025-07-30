#!/usr/bin/env python3
"""
Firefox Desktop Extension

A JupyterLab extension that provides Firefox desktop sessions using the same
proven architecture as jupyter-remote-desktop-proxy. This ensures proper
process isolation and prevents terminal blocking issues.

This extension uses jupyter-server-proxy to manage VNC sessions running Firefox,
avoiding all the complexity and problems of direct process management.
"""

from pathlib import Path
from .server_proxy import setup_firefox_desktop

HERE = Path(__file__).parent


def load_jupyter_server_extension(server_app):
    """
    Load the Firefox desktop server extension.
    
    This registers our handlers with the Jupyter server for serving
    the desktop interface.
    """
    from jupyter_server.utils import url_path_join
    from jupyter_server.base.handlers import AuthenticatedFileHandler
    from jupyter_server_proxy.handlers import AddSlashHandler
    from .handlers import FirefoxDesktopHandler

    base_url = server_app.web_app.settings["base_url"]

    server_app.web_app.add_handlers(
        ".*",
        [
            # Serve our static files (if any)
            (
                url_path_join(base_url, "/firefox-desktop/static/(.*)"),
                AuthenticatedFileHandler,
                {"path": str(HERE / "static")},
            ),
            # Ensure /firefox-desktop/ has trailing slash
            (url_path_join(base_url, "/firefox-desktop"), AddSlashHandler),
            # Main desktop handler
            (url_path_join(base_url, "/firefox-desktop/"), FirefoxDesktopHandler),
        ],
    )
    
    server_app.log.info("Firefox Desktop extension loaded")


# Extension entry points for Jupyter
def _jupyter_server_extension_points():
    """Entry point for Jupyter server extension"""
    return [{"module": "jupyterlab_firefox_launcher"}]


# For backward compatibility
_load_jupyter_server_extension = load_jupyter_server_extension
_jupyter_server_extension_paths = _jupyter_server_extension_points
