
import os
from importlib.metadata import version
from .server_extension import load_jupyter_server_extension

# Get version from package metadata

__version__ = version("jupyterlab-firefox-launcher")


HERE = os.path.dirname(os.path.abspath(__file__))


def _jupyter_server_extension_points():
    """
    Set up the server extension for collecting metrics
    """
    return [{"module": "jupyterlab_firefox_launcher"}]


# For backward compatibility
_load_jupyter_server_extension = load_jupyter_server_extension
_jupyter_server_extension_paths = _jupyter_server_extension_points
