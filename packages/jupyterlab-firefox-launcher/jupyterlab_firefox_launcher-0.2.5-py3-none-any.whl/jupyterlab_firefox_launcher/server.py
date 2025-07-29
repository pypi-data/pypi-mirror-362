# jupyterlab_firefox_launcher/server.py
from jupyterlab_firefox_launcher import setup_handlers

def load_jupyter_server_extension(app):
    """Called when the extension is loaded"""
    setup_handlers(app.web_app)
    app.log.info("Loaded jupyterlab_firefox_launcher extension")


def _jupyter_server_extension_paths():
    return [{
        "module": "jupyterlab_firefox_launcher"
    }]

