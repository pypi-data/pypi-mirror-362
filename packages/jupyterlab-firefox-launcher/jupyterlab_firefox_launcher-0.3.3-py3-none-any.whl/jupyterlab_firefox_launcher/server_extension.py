from pathlib import Path
import subprocess
import os
import time
import psutil
import socket
import random
from tornado import web
from tornado.web import HTTPError
from tornado.httpclient import AsyncHTTPClient

from jupyter_server.base.handlers import AuthenticatedFileHandler, JupyterHandler
from jupyter_server.utils import url_path_join

from .handlers import FirefoxHandler

HERE = Path(__file__).parent

# Global dictionary to track Xpra sessions
xpra_sessions = {}


def get_free_port():
    """Get a free port for Xpra"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port


def is_port_open(host, port):
    """Check if a port is open"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            return result == 0
    except:
        return False


class FirefoxSessionHandler(JupyterHandler):
    """Handle Firefox session lifecycle"""
    
    @web.authenticated
    async def get(self):
        """Get session status - for testing authentication"""
        self.log.info("Firefox session status requested")
        self.write({
            "status": "authenticated",
            "sessions": list(xpra_sessions.keys())
        })
    
    @web.authenticated
    async def post(self):
        """Start a new Firefox session"""
        try:
            self.log.info("Creating new Firefox session...")
            session_id = f"firefox_{random.randint(1000, 9999)}"
            port = get_free_port()
            
            self.log.info(f"Starting Xpra session {session_id} on port {port}")
            success = start_xpra_session(session_id, port)
            if success:
                self.log.info(f"Successfully started Firefox session {session_id}")
                self.write({
                    "session_id": session_id,
                    "port": port,
                    "status": "started"
                })
            else:
                self.log.error(f"Failed to start Firefox session {session_id}")
                self.set_status(500)
                self.write({"error": "Failed to start Xpra process"})
        except Exception as e:
            self.log.error(f"Exception in Firefox session creation: {str(e)}", exc_info=True)
            self.set_status(500)
            self.write({"error": f"Internal error: {str(e)}"})
    
    @web.authenticated
    async def delete(self, session_id):
        """Stop a Firefox session"""
        self.log.info(f"Stopping Firefox session {session_id}")
        success = stop_xpra_session(session_id)
        if success:
            self.log.info(f"Successfully stopped Firefox session {session_id}")
            self.write({"status": "stopped"})
        else:
            self.log.error(f"Failed to stop Firefox session {session_id} - session not found")
            self.set_status(404)
            self.write({"error": "Session not found"})


class SimpleProxyHandler(JupyterHandler):
    """Simple proxy handler for Xpra"""
    
    async def get(self, session_id, path):
        """Proxy GET requests to Xpra session"""
        if session_id not in xpra_sessions:
            self.set_status(404)
            self.write("Firefox session not found")
            return
            
        port = xpra_sessions[session_id]["port"]
        
        # Check if session is still running
        if not is_port_open("127.0.0.1", port):
            self.set_status(503)
            self.write("Firefox session is not running")
            return
        
        client = AsyncHTTPClient()
        url = f"http://127.0.0.1:{port}/{path}"
        
        try:
            response = await client.fetch(url, method="GET", request_timeout=10)
            for header_name, header_value in response.headers.get_all():
                if header_name.lower() not in ['content-length', 'transfer-encoding']:
                    self.set_header(header_name, header_value)
            self.write(response.body)
        except Exception as e:
            self.set_status(502)
            self.write(f"Firefox session error: {e}")
        finally:
            client.close()

    async def post(self, session_id, path):
        """Proxy POST requests to Xpra session"""
        if session_id not in xpra_sessions:
            self.set_status(404)
            self.write("Firefox session not found")
            return
            
        port = xpra_sessions[session_id]["port"]
        
        if not is_port_open("127.0.0.1", port):
            self.set_status(503)
            self.write("Firefox session is not running")
            return
                
        client = AsyncHTTPClient()
        url = f"http://127.0.0.1:{port}/{path}"
        
        try:
            response = await client.fetch(
                url, 
                method="POST",
                body=self.request.body,
                headers=self.request.headers,
                request_timeout=10
            )
            for header_name, header_value in response.headers.get_all():
                if header_name.lower() not in ['content-length', 'transfer-encoding']:
                    self.set_header(header_name, header_value)
            self.write(response.body)
        except Exception as e:
            self.set_status(502)
            self.write(f"Firefox session error: {e}")
        finally:
            client.close()


class AddSlashHandler(JupyterHandler):
    """Add trailing slash handler"""
    
    def get(self):
        """Redirect to URL with trailing slash"""
        self.redirect(self.request.uri + "/")


def start_xpra_session(session_id, port):
    """Start a new Xpra session"""
    try:
        print(f"[XPRA] Starting Xpra session {session_id} on port {port}...")
        
        # Check if Xpra is already running on the port
        if is_port_open("127.0.0.1", port):
            print(f"[XPRA] Port {port} is already in use, getting new port...")
            port = get_free_port()
            print(f"[XPRA] Using new port {port}")
        
        # Check if Xpra command exists
        try:
            xpra_check = subprocess.run(['which', 'xpra'], check=True, capture_output=True, text=True)
            print(f"[XPRA] Xpra found at: {xpra_check.stdout.strip()}")
        except subprocess.CalledProcessError as e:
            print(f"[XPRA] ERROR: Xpra command not found. Return code: {e.returncode}")
            print(f"[XPRA] Stderr: {e.stderr}")
            return False
        
        # Check if Firefox exists
        try:
            firefox_check = subprocess.run(['which', 'firefox'], capture_output=True, text=True)
            if firefox_check.returncode == 0:
                print(f"[XPRA] Firefox found at: {firefox_check.stdout.strip()}")
            else:
                print(f"[XPRA] WARNING: Firefox not found in PATH, Xpra will try to find it")
        except Exception as e:
            print(f"[XPRA] WARNING: Could not check Firefox availability: {e}")
        
        # Check display environment
        display = os.environ.get('DISPLAY')
        print(f"[XPRA] Current DISPLAY environment: {display}")
        
        # Check if we're in a headless environment
        try:
            xvfb_check = subprocess.run(['which', 'Xvfb'], capture_output=True, text=True)
            if xvfb_check.returncode == 0:
                print(f"[XPRA] Xvfb available at: {xvfb_check.stdout.strip()}")
            else:
                print(f"[XPRA] No Xvfb found - may need virtual display")
        except Exception as e:
            print(f"[XPRA] Could not check Xvfb: {e}")
        
        cmd = [
            'xpra', 'start', 
            f'--bind-tcp=0.0.0.0:{port}',
            '--html=on',
            '--start=firefox',
            '--exit-with-children=yes',
            '--daemon=yes',
            # Disable Xpra controls overlay
            '--html-hide-controls=yes',
            '--html-hide-fullscreen=yes',
            '--html-hide-keyboard=yes',
            '--html-hide-menu=yes',
            '--html-hide-clipboard=yes',
            '--html-hide-sound=yes',
            '--html-hide-video=yes',
            '--html-hide-printing=yes',
            # Additional clean interface options
            '--html-no-virtual-keyboard=yes',
            '--html-no-context-menu=yes',
            # Enhanced debugging and display options
            '--debug=all',
            '--verbose',
            # Try to use Xvfb if no display available
            '--xvfb=auto',
        ]
        
        print(f"[XPRA] Running command: {' '.join(cmd)}")
        print(f"[XPRA] Working directory: {os.getcwd()}")
        print(f"[XPRA] Environment variables:")
        for key in ['DISPLAY', 'XAUTHORITY', 'USER', 'HOME', 'PATH']:
            print(f"[XPRA]   {key}: {os.environ.get(key, 'NOT SET')}")
        
        # Run with enhanced logging
        result = subprocess.run(
            cmd, 
            check=True, 
            capture_output=True, 
            text=True,
            timeout=30  # Add timeout to prevent hanging
        )
        
        print(f"[XPRA] Command completed successfully")
        print(f"[XPRA] Return code: {result.returncode}")
        print(f"[XPRA] Stdout ({len(result.stdout)} chars):")
        if result.stdout:
            for line in result.stdout.split('\n'):
                if line.strip():
                    print(f"[XPRA]   OUT: {line}")
        else:
            print(f"[XPRA]   OUT: (empty)")
        
        print(f"[XPRA] Stderr ({len(result.stderr)} chars):")
        if result.stderr:
            for line in result.stderr.split('\n'):
                if line.strip():
                    print(f"[XPRA]   ERR: {line}")
        else:
            print(f"[XPRA]   ERR: (empty)")
        
        # Wait for Xpra to be ready with enhanced monitoring
        print(f"[XPRA] Waiting for session {session_id} to become ready on port {port}...")
        for i in range(30):  # Wait up to 30 seconds with more granular checking
            time.sleep(1)
            
            # Check if port is open
            port_open = is_port_open("127.0.0.1", port)
            print(f"[XPRA] Attempt {i+1}/30: Port {port} open: {port_open}")
            
            if port_open:
                print(f"[XPRA] SUCCESS: Session {session_id} ready on port {port}")
                xpra_sessions[session_id] = {
                    "port": port,
                    "started": time.time(),
                    "process": None  # We could store process info here
                }
                
                # Try to check if Xpra process is actually running
                try:
                    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                        if (proc.info['name'] == 'xpra' and 
                            f'--bind-tcp=0.0.0.0:{port}' in ' '.join(proc.info['cmdline'] or [])):
                            print(f"[XPRA] Found Xpra process: PID {proc.info['pid']}")
                            break
                    else:
                        print(f"[XPRA] WARNING: Port is open but no Xpra process found")
                except Exception as e:
                    print(f"[XPRA] WARNING: Could not check Xpra process: {e}")
                
                return True
            
            # Every 5 seconds, check if there are any Xpra processes
            if (i + 1) % 5 == 0:
                try:
                    xpra_procs = []
                    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                        if proc.info['name'] == 'xpra':
                            xpra_procs.append(f"PID {proc.info['pid']}: {' '.join(proc.info['cmdline'] or [])}")
                    
                    if xpra_procs:
                        print(f"[XPRA] Active Xpra processes ({len(xpra_procs)}):")
                        for proc_info in xpra_procs:
                            print(f"[XPRA]   {proc_info}")
                    else:
                        print(f"[XPRA] No Xpra processes found - may have failed to start")
                except Exception as e:
                    print(f"[XPRA] Could not check processes: {e}")
        
        print(f"[XPRA] TIMEOUT: Session {session_id} failed to start within 30 seconds")
        
        # Final diagnostic check
        try:
            print(f"[XPRA] Final diagnostic check:")
            print(f"[XPRA]   Port {port} open: {is_port_open('127.0.0.1', port)}")
            
            # Check for any error logs or zombie processes
            zombie_procs = []
            for proc in psutil.process_iter(['pid', 'name', 'status']):
                if proc.info['name'] == 'xpra' and proc.info['status'] == psutil.STATUS_ZOMBIE:
                    zombie_procs.append(proc.info['pid'])
            
            if zombie_procs:
                print(f"[XPRA]   Found zombie Xpra processes: {zombie_procs}")
            else:
                print(f"[XPRA]   No zombie Xpra processes")
                
        except Exception as e:
            print(f"[XPRA] Error in final diagnostic: {e}")
        
        return False
        
    except subprocess.CalledProcessError as e:
        print(f"[XPRA] ERROR: Failed to start Xpra session {session_id}")
        print(f"[XPRA] Command that failed: {' '.join(e.cmd) if e.cmd else 'unknown'}")
        print(f"[XPRA] Return code: {e.returncode}")
        print(f"[XPRA] Stdout: {e.stdout}")
        print(f"[XPRA] Stderr: {e.stderr}")
        
        # Try to get more specific error information
        if e.returncode == 1:
            print(f"[XPRA] Return code 1 usually indicates configuration or permission issues")
        elif e.returncode == 127:
            print(f"[XPRA] Return code 127 indicates command not found")
        elif e.returncode == 2:
            print(f"[XPRA] Return code 2 indicates invalid arguments")
        
        return False
    except subprocess.TimeoutExpired as e:
        print(f"[XPRA] ERROR: Xpra session {session_id} timed out after 30 seconds")
        print(f"[XPRA] Command: {' '.join(e.cmd) if e.cmd else 'unknown'}")
        
        # Try to kill any hanging processes
        try:
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                if (proc.info['name'] == 'xpra' and 
                    f'--bind-tcp=0.0.0.0:{port}' in ' '.join(proc.info['cmdline'] or [])):
                    print(f"[XPRA] Killing hanging Xpra process: PID {proc.info['pid']}")
                    proc.kill()
        except Exception as kill_e:
            print(f"[XPRA] Could not kill hanging processes: {kill_e}")
        
        return False
    except Exception as e:
        print(f"[XPRA] ERROR: Unexpected error starting Xpra session {session_id}: {e}")
        import traceback
        print(f"[XPRA] Full traceback:")
        for line in traceback.format_exc().split('\n'):
            if line.strip():
                print(f"[XPRA]   {line}")
        return False


def stop_xpra_session(session_id):
    """Stop an Xpra session"""
    if session_id not in xpra_sessions:
        print(f"[XPRA] ERROR: Session {session_id} not found in active sessions")
        return False
    
    port = xpra_sessions[session_id]["port"]
    print(f"[XPRA] Stopping Xpra session {session_id} on port {port}...")
    
    # Find and kill the Xpra process
    killed_processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if (proc.info['name'] == 'xpra' and 
                f'--bind-tcp=0.0.0.0:{port}' in ' '.join(proc.info['cmdline'] or [])):
                print(f"[XPRA] Found Xpra process to terminate: PID {proc.info['pid']}")
                proc.terminate()
                killed_processes.append(proc.info['pid'])
                # Wait for graceful shutdown
                try:
                    proc.wait(timeout=5)
                    print(f"[XPRA] Process {proc.info['pid']} terminated gracefully")
                except psutil.TimeoutExpired:
                    print(f"[XPRA] Process {proc.info['pid']} did not terminate, killing...")
                    proc.kill()  # Force kill if it doesn't terminate
                    print(f"[XPRA] Process {proc.info['pid']} killed")
                break
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            print(f"[XPRA] Could not access process: {e}")
            continue
    
    if not killed_processes:
        print(f"[XPRA] WARNING: No Xpra process found for session {session_id} on port {port}")
    
    # Remove from sessions
    del xpra_sessions[session_id]
    print(f"[XPRA] Session {session_id} stopped and removed from active sessions")
    return True


def load_jupyter_server_extension(server_app):
    """
    Called during notebook start
    """
    base_url = server_app.web_app.settings["base_url"]
    
    server_app.log.info("Loading jupyterlab_firefox_launcher server extension...")

    server_app.web_app.add_handlers(
        ".*",
        [
            # Session management endpoints
            (
                url_path_join(base_url, "/firefox/session"),
                FirefoxSessionHandler,
            ),
            (
                url_path_join(base_url, "/firefox/session/(.+)"),
                FirefoxSessionHandler,
            ),
            # Serve our own static files if we have any
            (
                url_path_join(base_url, "/firefox/static/(.*)"),
                AuthenticatedFileHandler,
                {"path": (str(HERE / "static"))},
            ),
            # Proxy to Xpra sessions
            (
                url_path_join(base_url, "/proxy/firefox/(.+)/(.*)"),
                SimpleProxyHandler,
            ),
            # To simplify URL mapping, we make sure that /firefox/ always
            # has a trailing slash
            (url_path_join(base_url, "/firefox"), AddSlashHandler),
            (url_path_join(base_url, "/firefox/"), FirefoxHandler),
        ],
    )
    
    server_app.log.info("Firefox launcher extension loaded successfully")
