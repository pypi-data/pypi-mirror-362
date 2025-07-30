import os
import sys
import subprocess
import socket
import time
import psutil
import logging
from tornado import web
# NOTE: websocket import removed - using HTML5-only approach
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.web import RequestHandler
# NOTE: WebSocketHandler import removed - using HTML5-only approach
from jupyter_server.base.handlers import JupyterHandler
from jupyter_server.utils import url_path_join
import secrets
import asyncio

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Global session storage
firefox_sessions = {}

def get_free_port():
    """Get a free port for Xpra"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def is_port_open(host, port, timeout=3):
    """Check if a port is open and accepting connections"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            if result == 0:
                # Port is open, but let's also verify we can actually communicate
                try:
                    # Send a simple HTTP request to verify the service is responding
                    sock.send(b"GET / HTTP/1.0\r\n\r\n")
                    response = sock.recv(1024)
                    # If we get any response, the service is likely working
                    return len(response) > 0
                except:
                    # Port is open but service might not be fully ready
                    return True  # Still consider it "open" for basic connectivity
            return False
    except Exception as e:
        logger.debug(f"Port check failed for {host}:{port}: {e}")
        return False

def find_xpra_processes():
    """Find running Xpra processes"""
    processes = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if proc.info['name'] and 'xpra' in proc.info['name'].lower():
                processes.append(proc.info)
    except Exception as e:
        logger.error(f"Error finding Xpra processes: {e}")
    return processes

def start_xpra_session(session_id):
    """Start a new Xpra session with enhanced error reporting"""
    logger.info(f"=== STARTING XPRA SESSION {session_id} ===")
    
    try:
        # Step 1: Environment diagnostics
        display = os.environ.get('DISPLAY', 'NOT_SET')
        logger.info(f"DISPLAY environment: {display}")
        logger.info(f"USER: {os.environ.get('USER', 'NOT_SET')}")
        logger.info(f"HOME: {os.environ.get('HOME', 'NOT_SET')}")
        logger.info(f"Working directory: {os.getcwd()}")
        
        # Step 2: Check for required binaries
        xpra_path = None
        firefox_path = None
        xvfb_available = False
        
        for path in ['/usr/bin/xpra', '/usr/local/bin/xpra', 'xpra']:
            if os.path.exists(path) or subprocess.run(['which', path], capture_output=True).returncode == 0:
                xpra_path = path
                break
        
        for path in ['/usr/bin/firefox', '/usr/local/bin/firefox', 'firefox']:
            if os.path.exists(path) or subprocess.run(['which', path], capture_output=True).returncode == 0:
                firefox_path = path
                break
        
        # Check for Xvfb (virtual framebuffer)
        for path in ['/usr/bin/Xvfb', '/usr/local/bin/Xvfb', 'Xvfb']:
            if os.path.exists(path) or subprocess.run(['which', path], capture_output=True).returncode == 0:
                xvfb_available = True
                break
        
        logger.info(f"Xpra path: {xpra_path}")
        logger.info(f"Firefox path: {firefox_path}")
        logger.info(f"Xvfb available: {xvfb_available}")
        
        if not xpra_path:
            raise Exception("Xpra not found in PATH")
        if not firefox_path:
            raise Exception("Firefox not found in PATH")
        
        # Warn if no display and no Xvfb
        if not display and not xvfb_available:
            logger.warning("No DISPLAY set and no Xvfb available - Xpra may fail to start")
        
        # Step 3: Get a free port
        port = get_free_port()
        logger.info(f"Allocated port: {port}")
        
        # Step 4: Generate unique display number
        display_num = port % 1000 + 100  # Generate display number from port
        logger.info(f"Using display number: :{display_num}")
        
        # Step 5: Check existing Xpra processes
        existing_processes = find_xpra_processes()
        logger.info(f"Existing Xpra processes: {len(existing_processes)}")
        for proc in existing_processes:
            logger.info(f"  PID {proc['pid']}: {' '.join(proc['cmdline']) if proc['cmdline'] else 'N/A'}")
        
        # Step 6: Set up environment first (needed for socket directory)
        env = os.environ.copy()
        
        # Create XDG_RUNTIME_DIR in user space to avoid permission issues
        user_id = os.getuid() if hasattr(os, 'getuid') else 1000
        home_dir = os.path.expanduser("~")
        xdg_runtime_dir = f"{home_dir}/.xdg_runtime"
        xpra_runtime_dir = f"{xdg_runtime_dir}/xpra"
        
        try:
            os.makedirs(xpra_runtime_dir, mode=0o700, exist_ok=True)
            logger.info(f"Created user XDG_RUNTIME_DIR: {xdg_runtime_dir}")
        except Exception as e:
            logger.warning(f"Could not create user runtime dir: {e}")
            # Use /tmp as fallback
            xdg_runtime_dir = f"/tmp/xdg_runtime_{user_id}"
            xpra_runtime_dir = f"{xdg_runtime_dir}/xpra"
            os.makedirs(xpra_runtime_dir, mode=0o700, exist_ok=True)
            logger.info(f"Using temp XDG_RUNTIME_DIR: {xdg_runtime_dir}")
        
        env['XDG_RUNTIME_DIR'] = xdg_runtime_dir
        
        # Step 6.5: Use fixed ports for HTML5 (based on validated solution)
        # Use working HTML5 ports from our debugging: 39339 or 42271
        fixed_ports = [39339, 42271]
        chosen_port = None
        
        # Try to find an available fixed port
        for fixed_port in fixed_ports:
            if not is_port_open('localhost', fixed_port, timeout=1):
                chosen_port = fixed_port
                break
        
        if chosen_port is None:
            # Fall back to next available port in range
            for test_port in range(39340, 39400):
                if not is_port_open('localhost', test_port, timeout=1):
                    chosen_port = test_port
                    break
        
        if chosen_port is None:
            raise Exception("No available ports found in HTML5 range")
        
        port = chosen_port  # Override the dynamic port with fixed port
        logger.info(f"Using fixed HTML5 port: {port}")
        
        # Step 7: Build Xpra command - HTML5 only, no WebSocket options
        cmd = [
            xpra_path,
            'start',
            f':{display_num}',
            f'--bind-tcp=0.0.0.0:{port}',  # Bind to all interfaces for JupyterHub access from different nodes
            '--html=on',
            '--daemon=no',
            '--exit-with-children=no',  # Don't exit when children exit initially
            # Handle headless environment - use Xvfb instead of auto
            '--xvfb=Xvfb' if xvfb_available else '--xvfb=/usr/bin/Xvfb',
            '--dpi=96',
            # Disable problematic features
            '--notifications=no',  # Disable dbus notifications
            '--mdns=no',          # Disable mdns discovery
            # Explicitly set socket directory to user space
            f'--socket-dir={xpra_runtime_dir}',
            # Prevent systemd integration attempts
            '--no-systemd-run',
            '--start-via-proxy=no',
            # Force HTML5-only mode - disable WebSocket transport completely
            '--html5-websockets=no' if xpra_path else '',  # Disable WebSocket in HTML5 client
            '--websocket=no',                              # Disable WebSocket transport
            '--ssl=no',                                    # Disable SSL to prevent secure WebSocket attempts
            # NOTE: Removed --websockets=no as this option doesn't exist in all Xpra versions
            # HTML5 is enabled by default with --html=on
        ]
        
        # Filter out empty strings from cmd
        cmd = [arg for arg in cmd if arg]
        
        logger.info(f"Xpra command: {' '.join(cmd)}")
        
        # If no DISPLAY is set, Xpra with --xvfb will handle it
        if not env.get('DISPLAY'):
            logger.info("No DISPLAY set, Xpra will use --xvfb to create virtual display")
        else:
            logger.info(f"Existing DISPLAY: {env.get('DISPLAY')}")
        
        # Let Xpra manage the display - don't override it
        # The display will be :display_num when Xpra starts
        
        logger.info("Starting Xpra process...")
        
        # Step 8: Start the process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
            cwd=os.getcwd()
        )
        
        logger.info(f"Xpra process started with PID: {process.pid}")
        
        # Step 9: Wait for Xpra to initialize and display to be ready
        max_wait = 30  # Increased timeout
        wait_interval = 0.5
        
        logger.info("Waiting for Xpra to initialize...")
        
        port_ready = False
        http_ready = False
        
        for i in range(int(max_wait / wait_interval)):
            # Check if process is still running
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                logger.error(f"Xpra process exited early with code: {process.returncode}")
                logger.error(f"STDOUT: {stdout.decode() if stdout else 'None'}")
                logger.error(f"STDERR: {stderr.decode() if stderr else 'None'}")
                raise Exception(f"Xpra exited with code {process.returncode}")
            
            # Check if port is ready
            if not port_ready and is_port_open('localhost', port, timeout=2):
                logger.info(f"Port {port} is ready after {i * wait_interval:.1f} seconds")
                port_ready = True
            
            # Once port is ready, check if HTTP service is responsive
            if port_ready and not http_ready:
                try:
                    import urllib.request
                    import urllib.error
                    
                    # Try to make a simple HTTP request to check if Xpra web interface is ready
                    req = urllib.request.Request(f'http://localhost:{port}/', timeout=2)
                    with urllib.request.urlopen(req) as response:
                        if response.getcode() == 200:
                            logger.info(f"HTTP service ready after {i * wait_interval:.1f} seconds")
                            http_ready = True
                            break
                except (urllib.error.URLError, urllib.error.HTTPError, Exception) as e:
                    # Service not ready yet, continue waiting
                    pass
            
            time.sleep(wait_interval)
            
            if i % 10 == 9:  # Log every 5 seconds
                status = []
                if port_ready:
                    status.append("port ready")
                if http_ready:
                    status.append("HTTP ready")
                if not status:
                    status.append("waiting for port")
                logger.info(f"Xpra startup: {', '.join(status)} (waited {(i+1) * wait_interval:.1f}s)")
        
        if not port_ready:
            # Timeout - kill process and get output
            logger.error(f"Timeout waiting for port {port} after {max_wait} seconds")
            process.terminate()
            time.sleep(2)
            if process.poll() is None:
                process.kill()
            stdout, stderr = process.communicate()
            logger.error(f"Process STDOUT: {stdout.decode() if stdout else 'None'}")
            logger.error(f"Process STDERR: {stderr.decode() if stderr else 'None'}")
            raise Exception("Timeout waiting for Xpra port to open")
        
        if not http_ready:
            logger.warning(f"Port {port} is open but HTTP service not responding after {max_wait} seconds")
            # Don't fail here, sometimes Xpra takes time to initialize HTTP but still works
        
        # Step 10: Start Firefox separately once display is ready
        logger.info("Display is ready, starting Firefox...")
        
        # Give Xpra a moment to fully initialize
        time.sleep(2)
        
        # Start Firefox with proper display environment
        firefox_cmd = [
            firefox_path,
            '--no-first-run',
            '--no-default-browser-check', 
            '--disable-extensions',
            '--disable-plugins',
            '--disable-web-security',
            '--disable-features=VizDisplayCompositor'
        ]
        
        firefox_env = env.copy()
        firefox_env['DISPLAY'] = f':{display_num}'
        
        firefox_process = subprocess.Popen(
            firefox_cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=firefox_env,
            cwd=os.getcwd()
        )
        
        logger.info(f"Firefox process started with PID: {firefox_process.pid}")
        
        # Step 11: Store session info
        session_info = {
            'session_id': session_id,
            'port': port,
            'display': f':{display_num}',
            'process': process,
            'firefox_process': firefox_process,
            'start_time': time.time()
        }
        
        firefox_sessions[session_id] = session_info
        logger.info(f"=== XPRA SESSION {session_id} STARTED SUCCESSFULLY ===")
        logger.info(f"Session info: port={port}, display=:{display_num}, pid={process.pid}")
        
        return session_info
        
    except Exception as e:
        logger.error(f"=== XPRA SESSION {session_id} FAILED ===")
        logger.error(f"Error: {str(e)}")
        logger.error(f"Error type: {type(e).__name__}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise

def stop_xpra_session(session_id):
    """Stop an Xpra session"""
    logger.info(f"Stopping Xpra session: {session_id}")
    
    if session_id in firefox_sessions:
        session_info = firefox_sessions[session_id]
        process = session_info['process']
        firefox_process = session_info.get('firefox_process')
        
        try:
            # Stop Firefox first
            if firefox_process and firefox_process.poll() is None:
                logger.info(f"Terminating Firefox process {firefox_process.pid}")
                firefox_process.terminate()
                time.sleep(2)
                if firefox_process.poll() is None:
                    firefox_process.kill()
            
            # Try graceful termination of Xpra
            process.terminate()
            time.sleep(2)
            
            # Force kill if still running
            if process.poll() is None:
                process.kill()
                
            del firefox_sessions[session_id]
            logger.info(f"Session {session_id} stopped successfully")
            
        except Exception as e:
            logger.error(f"Error stopping session {session_id}: {e}")
    else:
        logger.warning(f"Session {session_id} not found")

class FirefoxSessionHandler(JupyterHandler):
    """Handle Firefox session creation and deletion"""
    
    @web.authenticated
    async def post(self):
        """Create a new Firefox session"""
        logger.info("=== POST /firefox/session called ===")
        
        try:
            # Generate session ID
            session_id = f"firefox_{secrets.randbelow(10000)}"
            logger.info(f"Generated session ID: {session_id}")
            
            # Start Xpra session
            session_info = start_xpra_session(session_id)
            
            response_data = {
                'session_id': session_id,
                'port': session_info['port'],
                'status': 'started'
            }
            
            logger.info(f"Sending success response: {response_data}")
            self.write(response_data)
            
        except Exception as e:
            logger.error(f"Error in POST /firefox/session: {e}")
            import traceback
            logger.error(f"Full traceback: {traceback.format_exc()}")
            
            self.set_status(500)
            self.write({'error': str(e)})
    
    @web.authenticated  
    async def get(self, session_id=None):
        """Get session status or list all sessions"""
        logger.info(f"GET /firefox/session/{session_id} called")
        
        try:
            if session_id:
                # Get specific session status
                if session_id not in firefox_sessions:
                    self.set_status(404)
                    self.write({'error': 'Session not found'})
                    return
                
                session_info = firefox_sessions[session_id]
                process = session_info['process']
                firefox_process = session_info.get('firefox_process')
                port = session_info['port']
                
                # Check process status
                xpra_running = process.poll() is None
                firefox_running = firefox_process and firefox_process.poll() is None
                port_responsive = is_port_open('localhost', port, timeout=1)
                
                status = {
                    'session_id': session_id,
                    'port': port,
                    'xpra_running': xpra_running,
                    'firefox_running': firefox_running,
                    'port_responsive': port_responsive,
                    'healthy': xpra_running and port_responsive,
                    'start_time': session_info.get('start_time', 0)
                }
                
                self.write(status)
            else:
                # List all sessions
                sessions = {}
                for sid, info in firefox_sessions.items():
                    process = info['process']
                    sessions[sid] = {
                        'port': info['port'],
                        'running': process.poll() is None,
                        'start_time': info.get('start_time', 0)
                    }
                self.write({'sessions': sessions})
                
        except Exception as e:
            logger.error(f"Error getting session status: {e}")
            self.set_status(500)
            self.write({'error': str(e)})
    
    @web.authenticated  
    async def delete(self, session_id):
        """Delete a Firefox session"""
        logger.info(f"DELETE /firefox/session/{session_id} called")
        
        try:
            stop_xpra_session(session_id)
            self.write({'status': 'stopped'})
            
        except Exception as e:
            logger.error(f"Error stopping session {session_id}: {e}")
            self.set_status(500)
            self.write({'error': str(e)})

class SimpleProxyHandler(JupyterHandler):
    """
    HTTP proxy handler for Xpra connections in slurmspawner environment.
    
    Routes HTTP requests from JupyterLab frontend through JupyterHub to 
    the compute node where Xpra HTML5 server is running. This eliminates
    the WebSocket authentication issues while maintaining connectivity
    across the distributed compute environment.
    """
    
    def check_xsrf_cookie(self):
        """Disable XSRF protection for proxy requests"""
        pass
    
    async def get(self, session_id, path=""):
        """Proxy GET requests to Xpra"""
        await self._proxy_request("GET", session_id, path)
    
    async def post(self, session_id, path=""):
        """Proxy POST requests to Xpra"""
        await self._proxy_request("POST", session_id, path)
    
    async def put(self, session_id, path=""):
        """Proxy PUT requests to Xpra"""
        await self._proxy_request("PUT", session_id, path)
    
    async def delete(self, session_id, path=""):
        """Proxy DELETE requests to Xpra"""
        await self._proxy_request("DELETE", session_id, path)
    
    async def head(self, session_id, path=""):
        """Proxy HEAD requests to Xpra"""
        await self._proxy_request("HEAD", session_id, path)
    
    async def options(self, session_id, path=""):
        """Proxy OPTIONS requests to Xpra"""
        await self._proxy_request("OPTIONS", session_id, path)
    
    async def _proxy_request(self, method, session_id, path):
        """Proxy requests to the appropriate Xpra session with retry logic"""
        max_retries = 3
        retry_delay = 0.5
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Proxy request: method={method}, session_id={session_id}, path={path} (attempt {attempt + 1})")
                
                if not session_id or session_id not in firefox_sessions:
                    logger.error(f"Session not found: {session_id}. Available sessions: {list(firefox_sessions.keys())}")
                    self.set_status(404)
                    self.write({'error': 'Session not found'})
                    return
                
                session_info = firefox_sessions[session_id]
                port = session_info['port']
                
                # Check if Xpra session is still running
                process = session_info['process']
                if process.poll() is not None:
                    logger.error(f"Xpra process for session {session_id} has exited")
                    self.set_status(503)
                    self.write({'error': 'Xpra session has ended'})
                    return
                
                # Check if port is still available
                if not is_port_open('localhost', port, timeout=2):
                    if attempt < max_retries - 1:
                        logger.warning(f"Port {port} not responding, retrying in {retry_delay}s...")
                        await asyncio.sleep(retry_delay)
                        continue
                    else:
                        logger.warning(f"Port {port} is not responding for session {session_id}")
                        self.set_status(503)
                        self.write({'error': 'Xpra service not available'})
                        return
                
                # Build target URL - make sure path starts with /
                clean_path = path if path.startswith('/') else '/' + path
                target_url = f"http://localhost:{port}{clean_path}"
                
                logger.info(f"Proxying to: {target_url}")
                
                # Forward request
                client = AsyncHTTPClient()
                
                request = HTTPRequest(
                    url=target_url,
                    method=method,
                    headers=self.request.headers,
                    body=self.request.body if method in ["POST", "PUT", "PATCH"] else None,
                    follow_redirects=False,
                    request_timeout=15,  # Increased timeout for Xpra
                    connect_timeout=10
                )
                
                try:
                    response = await client.fetch(request, raise_error=False)
                    logger.info(f"Proxy response: {response.code} for {target_url}")
                    
                    # Forward response
                    self.set_status(response.code)
                    for name, value in response.headers.get_all():
                        if name.lower() not in ['content-length', 'transfer-encoding', 'content-encoding']:
                            self.set_header(name, value)
                    
                    if response.body:
                        self.write(response.body)
                    return  # Success, exit retry loop
                        
                except Exception as fetch_error:
                    error_msg = str(fetch_error)
                    logger.warning(f"Fetch error for {target_url} (attempt {attempt + 1}): {error_msg}")
                    
                    # Check if it's a timeout or connection error that we should retry
                    if attempt < max_retries - 1 and any(err in error_msg.lower() for err in 
                        ['timeout', 'connection closed', 'connection refused', 'streamclosed']):
                        logger.info(f"Retrying request in {retry_delay}s...")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    
                    # Final attempt failed or non-retryable error
                    if "timeout" in error_msg.lower():
                        self.set_status(504)
                        self.write({'error': 'Request timeout - Xpra service may be overloaded'})
                    elif "connection" in error_msg.lower():
                        self.set_status(503)
                        self.write({'error': 'Service temporarily unavailable - please try again'})
                    else:
                        self.set_status(502)
                        self.write({'error': f'Proxy error: {fetch_error}'})
                    return
                
            except Exception as e:
                logger.error(f"Proxy error (attempt {attempt + 1}): {e}")
                if attempt == max_retries - 1:
                    import traceback
                    logger.error(f"Proxy traceback: {traceback.format_exc()}")
                    self.set_status(500)
                    self.write({'error': str(e)})
                    return
                else:
                    await asyncio.sleep(retry_delay)

# NOTE: WebSocketProxyHandler disabled - HTML5-only approach eliminates WebSocket 403 auth errors
# class WebSocketProxyHandler(WebSocketHandler, JupyterHandler):
#     """WebSocket proxy handler for Xpra connections - DISABLED FOR HTML5-ONLY"""
#     
#     def check_xsrf_cookie(self):
#         """Disable XSRF protection for WebSocket proxy requests"""
#         pass
#     
#     def initialize(self):
#         self.backend_ws = None
#         self.session_id = None
#         self.target_port = None
#     
#     def check_origin(self, origin):
#         """Allow WebSocket connections from any origin for now"""
#         return True
#     
#     async def open(self, session_id, path=""):
#         """Open WebSocket connection"""
#         try:
#             logger.info(f"WebSocket open: session_id={session_id}, path={path}")
#             
#             if not session_id or session_id not in firefox_sessions:
#                 logger.error(f"WebSocket session not found: {session_id}")
#                 self.close(code=1008, reason="Session not found")
#                 return
#             
#             session_info = firefox_sessions[session_id]
#             self.target_port = session_info['port']
#             self.session_id = session_id
#             
#             # Check if Xpra session is still running
#             process = session_info['process']
#             if process.poll() is not None:
#                 logger.error(f"Xpra process for session {session_id} has exited")
#                 self.close(code=1011, reason="Xpra session ended")
#                 return
#             
#             # Check if port is still available
#             if not is_port_open('localhost', self.target_port, timeout=1):
#                 logger.warning(f"Port {self.target_port} is not responding for session {session_id}")
#                 self.close(code=1011, reason="Xpra service not available")
#                 return
#             
#             # Build WebSocket URL for Xpra
#             clean_path = path if path.startswith('/') else '/' + path
#             ws_url = f"ws://localhost:{self.target_port}{clean_path}"
#             
#             logger.info(f"Connecting to backend WebSocket: {ws_url}")
#             
#             # Create WebSocket connection to Xpra
#             from tornado.websocket import websocket_connect
#             
#             try:
#                 self.backend_ws = await websocket_connect(
#                     ws_url,
#                     on_message_callback=self.on_backend_message,
#                     connect_timeout=5,
#                     compression_options={}
#                 )
#                 logger.info(f"Backend WebSocket connected successfully")
#                 
#             except Exception as e:
#                 logger.error(f"Failed to connect to backend WebSocket: {e}")
#                 if "Connection refused" in str(e):
#                     self.close(code=1011, reason="Xpra service not ready")
#                 else:
#                     self.close(code=1011, reason="Backend connection failed")
#                 
#         except Exception as e:
#             logger.error(f"WebSocket open error: {e}")
#             import traceback
#             logger.error(f"WebSocket traceback: {traceback.format_exc()}")
#             self.close(code=1011, reason="Internal error")
#     
#     def on_backend_message(self, message):
#         """Forward messages from backend to client"""
#         if message and hasattr(self, 'ws_connection') and self.ws_connection and not self.ws_connection.stream.closed():
#             try:
#                 self.write_message(message)
#             except Exception as e:
#                 logger.error(f"Error forwarding backend message: {e}")
#                 # Close connection if we can't forward messages
#                 try:
#                     self.close(code=1011, reason="Message forwarding failed")
#                 except:
#                     pass
#     
#     def on_message(self, message):
#         """Forward messages from client to backend"""
#         if self.backend_ws and hasattr(self.backend_ws, 'stream') and not self.backend_ws.stream.closed():
#             try:
#                 self.backend_ws.write_message(message)
#             except Exception as e:
#                 logger.error(f"Error forwarding client message: {e}")
#                 # Close connection if we can't forward messages
#                 try:
#                     self.close(code=1011, reason="Backend forwarding failed")
#                 except:
#                     pass
#     
#     def on_close(self):
#         """Close backend connection when client disconnects"""
#         logger.info(f"WebSocket closed for session {getattr(self, 'session_id', 'unknown')}")
#         if hasattr(self, 'backend_ws') and self.backend_ws:
#             try:
#                 self.backend_ws.close()
#             except Exception as e:
#                 logger.error(f"Error closing backend WebSocket: {e}")

class FirefoxHandler(JupyterHandler):
    """Main Firefox interface handler"""
    
    async def get(self):
        """Serve the Firefox interface"""
        # HTML page that connects through JupyterLab proxy (required for slurmspawner)
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Firefox Browser</title>
            <style>
                body { margin: 0; padding: 0; font-family: Arial, sans-serif; }
                .container { padding: 20px; text-align: center; }
                .status { margin: 20px 0; }
                iframe { width: 100%; height: 80vh; border: none; }
                .info { background: #e3f2fd; padding: 10px; margin: 10px 0; border-radius: 4px; }
            </style>
            <script>
                // Force disable WebSocket globally to prevent Xpra HTML5 client from using it
                (function() {
                    // Store original WebSocket for debugging
                    var OriginalWebSocket = window.WebSocket;
                    
                    // Override WebSocket constructor to prevent connections
                    window.WebSocket = function(url, protocols) {
                        console.log('WebSocket connection blocked:', url);
                        // Throw an error to make Xpra fall back to HTTP
                        throw new Error('WebSocket disabled - using HTTP-only mode');
                    };
                    
                    // Also disable on prototype
                    if (OriginalWebSocket && OriginalWebSocket.prototype) {
                        delete OriginalWebSocket.prototype.constructor;
                    }
                    
                    // Remove from global scope
                    delete window.WebSocket;
                    
                    // Override for any iframe content after load
                    function disableWebSocketInIframe(iframe) {
                        try {
                            var iframeWindow = iframe.contentWindow || iframe.contentDocument.defaultView;
                            if (iframeWindow && iframeWindow.WebSocket) {
                                var originalWS = iframeWindow.WebSocket;
                                iframeWindow.WebSocket = function(url, protocols) {
                                    console.log('Iframe WebSocket connection blocked:', url);
                                    throw new Error('WebSocket disabled in iframe - using HTTP-only mode');
                                };
                                delete iframeWindow.WebSocket;
                            }
                        } catch (e) {
                            // Ignore cross-origin errors
                            console.log('Could not disable WebSocket in iframe (cross-origin):', e.message);
                        }
                    }
                    
                    // Monitor for new iframes
                    var observer = new MutationObserver(function(mutations) {
                        mutations.forEach(function(mutation) {
                            mutation.addedNodes.forEach(function(node) {
                                if (node.tagName === 'IFRAME') {
                                    node.addEventListener('load', function() {
                                        disableWebSocketInIframe(node);
                                    });
                                }
                            });
                        });
                    });
                    
                    observer.observe(document.body, { childList: true, subtree: true });
                })();
            </script>
        </head>
        <body>
            <div class="container">
                <h2>🦊 Firefox Browser (HTML5)</h2>
                <div class="info">Using HTML5-only connection via JupyterLab proxy (compatible with all Xpra versions)</div>
                <div class="status" id="status">Starting Firefox session...</div>
                <div id="firefox-container"></div>
            </div>
            
            <script>
                async function startFirefoxSession() {
                    try {
                        const response = await fetch('/firefox/session', {
                            method: 'POST',
                            credentials: 'same-origin'
                        });
                        
                        if (!response.ok) {
                            throw new Error('Failed to start session');
                        }
                        
                        const data = await response.json();
                        
                        // Connect through JupyterLab proxy to reach Xpra on compute node
                        // Add comprehensive parameters to force HTTP-only mode and disable WebSocket attempts
                        const iframe = document.createElement('iframe');
                        iframe.src = `/proxy/firefox/${data.session_id}/?websocket=no&websockets=no&ws=no&ssl=no&tls=no&secure=no&encryption=no&sharing=1&keyboard=1&sound=no&microphone=no&webcam=no&printing=no&file-transfer=no&clipboard=yes&notifications=no`;
                        iframe.title = "Firefox Browser via Xpra HTML5 (HTTP-only)";
                        iframe.style.width = '100%';
                        iframe.style.height = '80vh';
                        iframe.style.border = 'none';
                        
                        // Disable WebSocket in iframe after load
                        iframe.onload = function() {
                            try {
                                if (iframe.contentWindow && iframe.contentWindow.WebSocket) {
                                    iframe.contentWindow.WebSocket = undefined;
                                    delete iframe.contentWindow.WebSocket;
                                }
                            } catch (e) {
                                // Ignore cross-origin errors
                            }
                        };
                        
                        document.getElementById('firefox-container').appendChild(iframe);
                        document.getElementById('status').textContent = 
                            `Firefox is ready! (Session: ${data.session_id}, HTTP-only mode)`;
                        
                    } catch (error) {
                        document.getElementById('status').textContent = `Error: ${error.message}`;
                        console.error('Firefox session error:', error);
                    }
                }
                
                startFirefoxSession();
            </script>
        </body>
        </html>
        """
        
        self.set_header('Content-Type', 'text/html')
        self.write(html)

def load_jupyter_server_extension(server_app):
    """Load the server extension"""
    logger.info("=== LOADING FIREFOX SERVER EXTENSION (HTML5-ONLY VIA HTTP PROXY) ===")
    
    web_app = server_app.web_app
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    
    # Add handlers - Using HTTP proxy for slurmspawner compatibility
    handlers = [
        (url_path_join(base_url, "firefox/?"), FirefoxHandler),
        (url_path_join(base_url, "firefox/session/?"), FirefoxSessionHandler),
        (url_path_join(base_url, "firefox/session/([^/]+)/?"), FirefoxSessionHandler),
        # HTTP proxy for slurmspawner - routes traffic to compute node Xpra instances
        (url_path_join(base_url, "proxy/firefox/([^/]+)/(.*)"), SimpleProxyHandler),
        # NOTE: Using HTML5-only approach for maximum compatibility
        # All communication goes through HTTP proxy using Tornado AsyncHTTPClient
    ]
    
    web_app.add_handlers(host_pattern, handlers)
    logger.info(f"Added Firefox handlers to base_url: {base_url}")
    logger.info("=== FIREFOX SERVER EXTENSION LOADED (HTML5-ONLY VIA HTTP PROXY) ===")