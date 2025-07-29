
import os
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("jupyterlab-firefox-launcher")
except PackageNotFoundError:
    __version__ = "unknown"

def _get_firefox_proxy():
    """Entry point for jupyter-server-proxy"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, '..', 'launch-firefox-xpra.sh')
    script_path = os.path.abspath(script_path)
    
    def get_port():
        try:
            with open('/tmp/xpra-port', 'r') as f:
                return int(f.read().strip())
        except:
            return 15000  # Default fallback port
    
    return {
        "command": [script_path],
        "timeout": 30,
        "port": get_port,
        "mappath": {"/": "/"},
        # Remove launcher_entry to prevent duplicate entries
        # Let the JupyterLab extension handle the launcher
    }


# For direct import by jupyter-server-proxy
firefox = _get_firefox_proxy


def _jupyter_server_extension_points():
    return [{
        "module": "jupyterlab_firefox_launcher"
    }]


def _load_jupyter_server_extension(server_app):
    server_app.log.info("Loaded jupyterlab_firefox_launcher extension")

