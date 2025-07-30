
import os
import sys
from importlib.metadata import version, PackageNotFoundError

try:
    __version__ = version("jupyterlab-firefox-launcher")
except PackageNotFoundError:
    __version__ = "unknown"


def firefox():
    """Entry point for jupyter-server-proxy that launches Xpra with Firefox"""
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    
    # Use the installed script from bin directory
    script_name = "launch-firefox-xpra"
    if sys.platform == "win32":
        script_name += ".exe"
    
    logger.info(f"Looking for script: {script_name}")
    
    # Find the script in the virtual environment bin directory
    script_path = None
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        # We're in a virtual environment
        bin_dir = os.path.join(sys.prefix, 'bin')
        if sys.platform == "win32":
            bin_dir = os.path.join(sys.prefix, 'Scripts')
        script_path = os.path.join(bin_dir, script_name)
        logger.info(f"Checking venv path: {script_path}")
    else:
        # System installation, look in PATH
        import shutil
        script_path = shutil.which(script_name)
        logger.info(f"Checking PATH result: {script_path}")
    
    if not script_path or not os.path.exists(script_path):
        # Fallback to python -m execution
        logger.info("Script not found, using python -m fallback")
        script_path = [sys.executable, "-m", "jupyterlab_firefox_launcher.scripts"]
    else:
        logger.info(f"Using script at: {script_path}")
        script_path = [script_path]
    
    def get_port():
        try:
            with open('/tmp/xpra-port', 'r') as f:
                return int(f.read().strip())
        except:
            return 15555  # Default fallback port
    
    return {
        "command": script_path,
        "timeout": 90,
        "port": get_port,
        "mappath": {"/": "/"},
        # Point to our custom page instead of the raw Xpra interface
        "launcher_entry": {
            "enabled": True,
            "title": "Firefox Browser",
            "path_info": "firefox"  # This will create /firefox/ endpoint
        }
    }


def _jupyter_server_extension_points():
    return [{
        "module": "jupyterlab_firefox_launcher.server_extension"
    }]


def _load_jupyter_server_extension(server_app):
    """Called when the extension is loaded"""
    from .server_extension import load_jupyter_server_extension
    load_jupyter_server_extension(server_app)
