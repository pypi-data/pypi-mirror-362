#!/usr/bin/env python3
"""
Firefox Desktop Extension

A JupyterLab extension that provides Firefox desktop sessions using 
jupyter-server-proxy for proper process management and compatibility
with SlurmSpawner environments.

This extension registers the firefox-desktop server proxy configuration
without requiring custom handlers, since jupyter-server-proxy handles
all the HTTP routing and process management.
"""

from pathlib import Path

HERE = Path(__file__).parent


def load_jupyter_server_extension(server_app):
    """
    Load the Firefox desktop server extension.
    
    Since we're using jupyter-server-proxy, we only need to register
    our extension entry points. The actual Firefox service is managed
    by jupyter-server-proxy through the setup_firefox_desktop() function.
    """
    # jupyter-server-proxy automatically discovers our entry point:
    # firefox-desktop = "jupyterlab_firefox_launcher.server_proxy:setup_firefox_desktop"
    
    server_app.log.info("Firefox Desktop extension loaded (using jupyter-server-proxy)")


def _jupyter_server_extension_points():
    """Entry point for Jupyter server extension"""
    return [{"module": "jupyterlab_firefox_launcher"}]


# For backward compatibility  
_load_jupyter_server_extension = load_jupyter_server_extension
_jupyter_server_extension_paths = _jupyter_server_extension_points
