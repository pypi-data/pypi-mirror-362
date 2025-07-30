#!/usr/bin/env python3
"""
Firefox Desktop Server Proxy Configuration

This module provides Firefox launcher functionality using jupyter-server-proxy
with Xpra HTML5 for superior performance and seamless application integration.
"""

import os
import shlex
import stat
from shutil import which
from pathlib import Path

HERE = Path(__file__).parent


def setup_firefox_desktop():
    """
    Setup function for jupyter-server-proxy to launch Firefox with Xpra HTML5.
    
    Returns configuration dict for jupyter-server-proxy to manage an Xpra
    session with Firefox, providing excellent performance and direct HTML5 support.
    """
    
    # Check for Xpra
    xpra = which('xpra')
    if not xpra:
        raise RuntimeError(
            "xpra executable not found. Please install Xpra:\n"
            "  apt-get install xpra xpra-html5\n"
            "  or\n"
            "  yum install xpra python3-xpra-html5\n"
            "  or\n"
            "  conda install -c conda-forge xpra"
        )

    # Check for Firefox
    firefox = which('firefox')
    if not firefox:
        raise RuntimeError(
            "firefox executable not found. Please install Firefox:\n"
            "  apt-get install firefox\n"
            "  or\n"
            "  yum install firefox"
        )

    # Create user-space socket directory for security
    socket_dir = Path.home() / '.firefox-launcher' / 'sockets'
    socket_dir.mkdir(parents=True, exist_ok=True)

    # Path to our Firefox wrapper script
    firefox_wrapper = os.getenv("FIREFOX_LAUNCHER_WRAPPER", str(HERE / 'share' / 'firefox-xstartup'))
    
    # Alternative advanced wrapper with more options
    firefox_wrapper_advanced = str(HERE / 'share' / 'firefox-wrapper-advanced')
    
    # Use advanced wrapper if requested via environment variable
    if os.getenv("FIREFOX_LAUNCHER_ADVANCED", "").lower() in ("1", "true", "yes"):
        firefox_wrapper = firefox_wrapper_advanced
    
    # Make sure the wrapper script is executable
    import stat
    if os.path.exists(firefox_wrapper):
        st = os.stat(firefox_wrapper)
        os.chmod(firefox_wrapper, st.st_mode | stat.S_IEXEC)

    # Allow environment variable customization of Xpra options
    xpra_quality = os.getenv("FIREFOX_LAUNCHER_QUALITY", "100")
    xpra_compress = os.getenv("FIREFOX_LAUNCHER_COMPRESS", "0")
    xpra_dpi = os.getenv("FIREFOX_LAUNCHER_DPI", "96")
    
    # Build Xpra command using --start with our wrapper script
    # This gives us full control over Firefox options while using Xpra's process management
    xpra_command = shlex.join([
        'xpra', 'start',
        '--bind-tcp=0.0.0.0:{port}',  # {port} expanded by jupyter-server-proxy
        '--html=on',  # Enable HTML5 client
        '--daemon=no',  # Run in foreground for proper process management
        '--exit-with-children=yes',  # Exit when Firefox closes
        f'--start={firefox_wrapper}',  # Use our custom wrapper script
        f'--socket-dirs={socket_dir}',  # User-space socket directory
        '--system-proxy-socket=no',  # Disable system proxy socket
        '--mdns=no',  # Disable mDNS
        '--pulseaudio=no',  # Disable audio for simplicity
        '--notifications=no',  # Disable notifications
        '--clipboard=yes',  # Enable clipboard sharing
        '--sharing=no',  # Disable screen sharing
        '--speaker=no',  # Disable speaker
        '--microphone=no',  # Disable microphone
        '--webcam=no',  # Disable webcam
        '--desktop-scaling=auto',  # Auto-scale to browser window
        f'--dpi={xpra_dpi}',  # Configurable DPI
        f'--compress={xpra_compress}',  # Configurable compression
        f'--quality={xpra_quality}',  # Configurable quality
        '--window-close=auto',  # Handle window close events properly
    ])

    return {
        'command': ['sh', '-c', f'cd {os.getcwd()} && {xpra_command}'],
        'timeout': 30,
        'new_browser_window': True,
        'launcher_entry': {
            "title": "Firefox Browser", 
            "path_info": "firefox-desktop",
            "icon_path": "/static/firefox-icon.svg"
        },
        "port": 9876,  # Default port, will be dynamically assigned
        "mappath": {"/": "/index.html"},  # Map root to Xpra HTML5 client
    }
