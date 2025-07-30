import os
from jupyter_server.base.handlers import JupyterHandler
from tornado import web


class FirefoxHandler(JupyterHandler):
    """Handler that serves the Firefox browser interface"""
    
    @web.authenticated
    async def get(self):
        """Serve the Firefox interface"""
        # Get the base URL for constructing the proxy URL
        base_url = self.base_url
        
        # Construct the URL to the Xpra proxy
        proxy_url = f"{base_url}proxy/firefox/"
        
        # Simple HTML page that embeds the Xpra interface
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Firefox Browser</title>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
            background-color: #4d4d4d;
        }}
        
        #top-bar {{
            background-color: #4d4d4d;
            color: white;
            padding: 8px 16px;
            display: flex;
            align-items: center;
            border-bottom: 1px solid white;
        }}
        
        #logo {{
            font-weight: bold;
            margin-right: auto;
        }}
        
        #status {{
            font-size: 12px;
        }}
        
        iframe {{
            width: 100%;
            height: calc(100vh - 50px);
            border: none;
            background: white;
        }}
        
        .loading {{
            display: flex;
            justify-content: center;
            align-items: center;
            height: calc(100vh - 50px);
            color: white;
            font-size: 18px;
        }}
    </style>
</head>
<body>
    <div id="top-bar">
        <div id="logo">Firefox Browser</div>
        <div id="status">Loading...</div>
    </div>
    
    <div id="content">
        <div class="loading" id="loading">
            Starting Firefox browser...
        </div>
        <iframe id="firefox-frame" src="{proxy_url}" style="display: none;" 
                onload="document.getElementById('loading').style.display='none'; 
                        this.style.display='block';
                        document.getElementById('status').textContent='Ready';">
        </iframe>
    </div>
    
    <script>
        // Retry loading if initial load fails
        let retryCount = 0;
        const maxRetries = 10;
        
        function checkFrameLoaded() {{
            const frame = document.getElementById('firefox-frame');
            const loading = document.getElementById('loading');
            const status = document.getElementById('status');
            
            try {{
                // Try to access frame content to see if it loaded
                if (frame.contentDocument || frame.contentWindow) {{
                    loading.style.display = 'none';
                    frame.style.display = 'block';
                    status.textContent = 'Ready';
                    return;
                }}
            }} catch (e) {{
                // Frame loaded but cross-origin, which means it worked
                loading.style.display = 'none';
                frame.style.display = 'block';
                status.textContent = 'Ready';
                return;
            }}
            
            // If we get here, frame didn't load properly
            if (retryCount < maxRetries) {{
                retryCount++;
                status.textContent = `Retrying... (${{retryCount}}/${{maxRetries}})`;
                setTimeout(() => {{
                    frame.src = frame.src; // Reload frame
                }}, 3000);
            }} else {{
                loading.innerHTML = 'Failed to load Firefox. <a href="{proxy_url}" target="_blank">Click here to try directly</a>';
                status.textContent = 'Failed';
            }}
        }}
        
        // Initial check after a delay
        setTimeout(checkFrameLoaded, 5000);
        
        // Also try to detect load events
        document.getElementById('firefox-frame').addEventListener('load', () => {{
            setTimeout(checkFrameLoaded, 1000);
        }});
    </script>
</body>
</html>
        """
        
        self.set_header("Content-Type", "text/html")
        self.write(html_content)
