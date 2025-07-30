import os
import sys
import subprocess
import socket
import time
import psutil
import logging
from tornado import web
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.web import RequestHandler
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
            return result == 0
    except Exception:
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
        
        for path in ['/usr/bin/xpra', '/usr/local/bin/xpra', 'xpra']:
            if os.path.exists(path) or subprocess.run(['which', path], capture_output=True).returncode == 0:
                xpra_path = path
                break
        
        for path in ['/usr/bin/firefox', '/usr/local/bin/firefox', 'firefox']:
            if os.path.exists(path) or subprocess.run(['which', path], capture_output=True).returncode == 0:
                firefox_path = path
                break
        
        logger.info(f"Xpra path: {xpra_path}")
        logger.info(f"Firefox path: {firefox_path}")
        
        if not xpra_path:
            raise Exception("Xpra not found in PATH")
        if not firefox_path:
            raise Exception("Firefox not found in PATH")
        
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
        
        # Step 6: Build Xpra command
        cmd = [
            xpra_path,
            'start',
            f':{display_num}',
            f'--bind-tcp=0.0.0.0:{port}',
            '--html=on',
            '--daemon=no',
            f'--start-child={firefox_path}',
            '--no-first-run',
            '--no-default-browser-check',
            '--disable-extensions',
            '--disable-plugins',
            '--html-hide-controls=yes',
            '--html-hide-fullscreen=yes',
            '--html-hide-keyboard=yes',
            '--html-hide-menu=yes',
        ]
        
        logger.info(f"Xpra command: {' '.join(cmd)}")
        
        # Step 7: Set up environment
        env = os.environ.copy()
        env['DISPLAY'] = f':{display_num}'
        
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
        
        # Step 9: Wait for process to start and port to be ready
        max_wait = 15
        wait_interval = 0.5
        
        for i in range(int(max_wait / wait_interval)):
            # Check if process is still running
            if process.poll() is not None:
                stdout, stderr = process.communicate()
                logger.error(f"Xpra process exited early with code: {process.returncode}")
                logger.error(f"STDOUT: {stdout.decode() if stdout else 'None'}")
                logger.error(f"STDERR: {stderr.decode() if stderr else 'None'}")
                raise Exception(f"Xpra exited with code {process.returncode}")
            
            # Check if port is ready
            if is_port_open('localhost', port):
                logger.info(f"Port {port} is ready after {i * wait_interval:.1f} seconds")
                break
            
            time.sleep(wait_interval)
            
            if i % 10 == 9:  # Log every 5 seconds
                logger.info(f"Still waiting for port {port} (waited {(i+1) * wait_interval:.1f}s)")
        else:
            # Timeout - kill process and get output
            logger.error(f"Timeout waiting for port {port} after {max_wait} seconds")
            process.terminate()
            time.sleep(2)
            if process.poll() is None:
                process.kill()
            stdout, stderr = process.communicate()
            logger.error(f"Process STDOUT: {stdout.decode() if stdout else 'None'}")
            logger.error(f"Process STDERR: {stderr.decode() if stderr else 'None'}")
            raise Exception("Timeout waiting for Xpra to start")
        
        # Step 10: Store session info
        session_info = {
            'session_id': session_id,
            'port': port,
            'display': f':{display_num}',
            'process': process,
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
        
        try:
            # Try graceful termination first
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
    """Simple proxy handler for Xpra connections"""
    
    async def get(self, path=""):
        """Proxy GET requests to Xpra"""
        await self._proxy_request("GET", path)
    
    async def post(self, path=""):
        """Proxy POST requests to Xpra"""
        await self._proxy_request("POST", path)
    
    async def _proxy_request(self, method, path):
        """Proxy requests to the appropriate Xpra session"""
        try:
            # Get session ID from query params or headers
            session_id = self.get_argument('session', None)
            
            if not session_id or session_id not in firefox_sessions:
                self.set_status(404)
                self.write({'error': 'Session not found'})
                return
            
            session_info = firefox_sessions[session_id]
            port = session_info['port']
            
            # Build target URL
            target_url = f"http://localhost:{port}/{path}"
            
            # Forward request
            client = AsyncHTTPClient()
            
            request = HTTPRequest(
                url=target_url,
                method=method,
                headers=self.request.headers,
                body=self.request.body if method == "POST" else None,
                follow_redirects=False
            )
            
            response = await client.fetch(request, raise_error=False)
            
            # Forward response
            self.set_status(response.code)
            for name, value in response.headers.get_all():
                if name.lower() not in ['content-length', 'transfer-encoding', 'content-encoding']:
                    self.set_header(name, value)
            
            if response.body:
                self.write(response.body)
            
        except Exception as e:
            logger.error(f"Proxy error: {e}")
            self.set_status(500)
            self.write({'error': str(e)})

class FirefoxHandler(JupyterHandler):
    """Main Firefox interface handler"""
    
    async def get(self):
        """Serve the Firefox interface"""
        # Simple HTML page that will connect to Xpra
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
            </style>
        </head>
        <body>
            <div class="container">
                <h2>🦊 Firefox Browser</h2>
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
                        const iframe = document.createElement('iframe');
                        iframe.src = `http://localhost:${data.port}/`;
                        document.getElementById('firefox-container').appendChild(iframe);
                        document.getElementById('status').textContent = 'Firefox is ready!';
                        
                    } catch (error) {
                        document.getElementById('status').textContent = `Error: ${error.message}`;
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
    logger.info("=== LOADING FIREFOX SERVER EXTENSION ===")
    
    web_app = server_app.web_app
    host_pattern = ".*$"
    base_url = web_app.settings["base_url"]
    
    # Add handlers
    handlers = [
        (url_path_join(base_url, "firefox/?"), FirefoxHandler),
        (url_path_join(base_url, "firefox/session/?"), FirefoxSessionHandler),
        (url_path_join(base_url, "firefox/session/([^/]+)/?"), FirefoxSessionHandler),
        (url_path_join(base_url, "firefox/proxy/(.*)"), SimpleProxyHandler),
    ]
    
    web_app.add_handlers(host_pattern, handlers)
    logger.info(f"Added Firefox handlers to base_url: {base_url}")
    logger.info("=== FIREFOX SERVER EXTENSION LOADED ===")