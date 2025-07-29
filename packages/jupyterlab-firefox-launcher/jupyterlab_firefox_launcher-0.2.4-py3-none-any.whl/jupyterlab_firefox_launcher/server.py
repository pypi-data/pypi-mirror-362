# This file is kept for compatibility but jupyter-server-proxy handles the proxying
# The firefox() function in __init__.py configures the proxy server
pass


def load_jupyter_server_extension(app):
    """Called when the extension is loaded"""
    setup_handlers(app.web_app)
    app.log.info("Loaded jupyterlab_firefox_launcher extension")


def _jupyter_server_extension_paths():
    return [{
        "module": "jupyterlab_firefox_launcher"
    }]

