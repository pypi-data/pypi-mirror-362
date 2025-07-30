import os
import shlex
from shutil import which

HERE = os.path.dirname(os.path.abspath(__file__))


def setup_firefox():
    """
    Setup Firefox via Xpra for jupyter-server-proxy.
    """
    xpra = which('xpra')
    if not xpra:
        raise RuntimeError(
            "xpra executable not found, please install Xpra"
        )

    # Build the xpra command to start Firefox
    # Use a fixed port that Xpra will bind to
    xpra_port = 15555
    
    xpra_args = [
        xpra, 'start',
        f'--bind-tcp=0.0.0.0:{xpra_port}',
        '--html=on',
        '--start=firefox',
        '--exit-with-children=yes',
        '--daemon=no'  # Run in foreground for jupyter-server-proxy
    ]

    xpra_command = shlex.join(xpra_args)

    return {
        'command': ['/bin/sh', '-c', f'cd {os.getcwd()} && {xpra_command}'],
        'port': xpra_port,
        'timeout': 30,
        'new_browser_window': True,
        # We want the launcher entry to point to /firefox/, not to /firefox-proxy/
        # /firefox/ is the user facing URL, while /firefox-proxy/ serves the actual proxy
        "launcher_entry": {"title": "Firefox Browser", "path_info": "firefox"},
    }
