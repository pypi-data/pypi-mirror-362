#!/usr/bin/env python3
"""
Firefox launcher script for Xpra
"""
import os
import subprocess
import sys
import random


def main():
    """Main entry point for the Firefox launcher script"""
    # Dynamically allocate port and display
    port = random.randint(15000, 16000)
    display_num = random.randint(100, 200)
    
    # Store for jupyter-server-proxy to read
    with open('/tmp/xpra-port', 'w') as f:
        f.write(str(port))
    
    # Start Xpra with Firefox
    cmd = [
        'xpra', 'start', f':{display_num}',
        f'--bind-tcp=0.0.0.0:{port}',
        '--html=on',
        '--daemon=no',
        '--start-child=firefox',
        '--exit-with-children',
        '--notifications=no',  # Disable notifications to avoid D-Bus issues
        '--dbus-launch=',  # Disable D-Bus launch
        '--systemd-run=no',  # Disable systemd integration
        '--pulseaudio=no',  # Disable PulseAudio integration
        '--speaker=no',  # Disable speaker
        '--microphone=no',  # Disable microphone
        '--mdns=no',  # Disable mDNS to avoid avahi dependency
        '--opengl=no',  # Disable OpenGL to avoid warnings
        '--socket-dirs=/tmp'  # Use /tmp for socket directory instead of /run/user
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Xpra: {e}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError:
        print("Error: xpra command not found. Please install xpra.", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
