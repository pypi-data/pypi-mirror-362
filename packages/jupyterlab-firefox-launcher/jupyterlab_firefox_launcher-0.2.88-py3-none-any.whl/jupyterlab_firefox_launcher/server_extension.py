from pathlib import Path
from jupyter_server.base.handlers import AuthenticatedFileHandler
from jupyter_server.utils import url_path_join
from jupyter_server_proxy.handlers import AddSlashHandler
from .handlers import FirefoxHandler

HERE = Path(__file__).parent


def load_jupyter_server_extension(server_app):
    """
    Called during notebook start
    """
    base_url = server_app.web_app.settings["base_url"]

    server_app.web_app.add_handlers(
        ".*",
        [
            # Serve our own static files if we have any
            (
                url_path_join(base_url, "/firefox/static/(.*)"),
                AuthenticatedFileHandler,
                {"path": (str(HERE / "static"))},
            ),
            # To simplify URL mapping, we make sure that /firefox/ always
            # has a trailing slash
            (url_path_join(base_url, "/firefox"), AddSlashHandler),
            (url_path_join(base_url, "/firefox/"), FirefoxHandler),
        ],
    )
    
    server_app.log.info("Loaded jupyterlab_firefox_launcher server extension")
