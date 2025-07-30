"use strict";
(self["webpackChunkjupyterlab_firefox_launcher"] = self["webpackChunkjupyterlab_firefox_launcher"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.buildFirefoxHTML = void 0;
const launcher_1 = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const widgets_1 = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
const services_1 = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
// Firefox SVG icon
const firefoxIconSvg = `
<svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm0 22C6.486 22 2 17.514 2 12S6.486 2 12 2s10 4.486 10 10-4.486 10-10 10z" fill="#FF7139"/>
  <path d="M19.5 9.5c-1.2-1.8-3.2-3-5.5-3-1.2 0-2.3.3-3.3.8.5-.4 1.1-.8 1.8-.8 2.2 0 4 1.8 4 4 0 .7-.2 1.4-.5 2h3.5zm-7.5 6c-2.2 0-4-1.8-4-4s1.8-4 4-4 4 1.8 4 4-1.8 4-4 4z" fill="#FF4F00"/>
  <circle cx="12" cy="11.5" r="2.5" fill="#FFA500"/>
</svg>
`;
// Inject CSS styles
const addFirefoxStyles = () => {
    const styleId = 'firefox-launcher-styles';
    if (document.getElementById(styleId)) {
        return; // Already added
    }
    const style = document.createElement('style');
    style.id = styleId;
    style.textContent = `
    /* Firefox icon styling for JupyterLab */
    .jp-firefox-icon {
      background-image: url('data:image/svg+xml;base64,${btoa(firefoxIconSvg)}');
      background-repeat: no-repeat;
      background-size: 16px;
      background-position: center;
      width: 16px;
      height: 16px;
      display: inline-block;
    }
    
    .jp-firefox-icon::before {
      content: '';
      display: inline-block;
      width: 16px;
      height: 16px;
      background-image: inherit;
      background-repeat: inherit;
      background-size: inherit;
      background-position: inherit;
    }
    
    .jp-LauncherCard[data-command="firefox:open"] .jp-LauncherCard-icon {
      background-image: url('data:image/svg+xml;base64,${btoa(firefoxIconSvg)}');
      background-size: 32px;
      background-repeat: no-repeat;
      background-position: center;
    }
  `;
    document.head.appendChild(style);
};
const buildFirefoxHTML = (iframeId, sessionId, baseUrl) => {
    // Simple URL - rely on server-side WebSocket blocking (no --bind-ws options)
    // Xpra HTML5 client will fallback to HTTP when WebSocket connection fails
    const xpraUrl = `${baseUrl}proxy/firefox/${sessionId}/`;
    return `
    <div style="display:flex; justify-content:space-between; align-items:center; padding:4px; gap:8px; background:#f5f5f5;">
      <span style="font-size:12px; color:#666;">Session: ${sessionId} (HTTP-only)</span>
      <div style="display:flex; gap:8px;">
        <button id="ff-refresh">🔄 Refresh</button>
        <button id="ff-close">❌ Close</button>
      </div>
    </div>
    <div id="ff-status" style="display:none; padding:20px; text-align:center; background:#f0f0f0;">
      Starting Firefox session (HTTP-only mode)...
    </div>
    <script>
      // CRITICAL: Block WebSocket globally before iframe loads to prevent connection attempts
      (function() {
        console.log('Blocking WebSocket in Firefox launcher widget');
        var OriginalWebSocket = window.WebSocket;
        window.WebSocket = function(url, protocols) {
          console.log('WebSocket connection blocked by Firefox launcher:', url);
          throw new Error('WebSocket disabled by Firefox launcher - using HTTP-only mode');
        };
        delete window.WebSocket;
      })();
    </script>
    <iframe 
      id="${iframeId}"
      src="${xpraUrl}" 
      style="width:100%; height:90%; border:none; display:none;"
      allowfullscreen
    ></iframe>`;
};
exports.buildFirefoxHTML = buildFirefoxHTML;
// Helper function to get CSRF token
const getCSRFToken = () => {
    const tokenElement = document.querySelector('meta[name="_xsrf"]');
    return tokenElement ? tokenElement.getAttribute('content') : '';
};
const extension = {
    id: 'jupyterlab-firefox-launcher:plugin',
    description: 'JupyterLab extension to launch Firefox in a tab',
    autoStart: true,
    requires: [launcher_1.ILauncher, apputils_1.ICommandPalette],
    activate: async (app, launcher, palette) => {
        // Add Firefox styles to the document
        addFirefoxStyles();
        const command = 'firefox:open';
        const label = 'Firefox Browser';
        app.commands.addCommand(command, {
            label,
            execute: async () => {
                const baseUrl = app.serviceManager.serverSettings.baseUrl;
                const normalizedBaseUrl = baseUrl.endsWith('/') ? baseUrl : baseUrl + '/';
                console.log('Starting Firefox session...'); // Debug logging
                const content = new widgets_1.Widget();
                content.node.style.height = '100%';
                content.node.style.width = '100%';
                content.node.style.overflow = 'hidden';
                // CRITICAL: Block WebSocket at the widget level
                const blockWebSocket = () => {
                    const originalWebSocket = window.WebSocket;
                    window.WebSocket = function (url, protocols) {
                        console.log('WebSocket connection blocked by Firefox launcher widget:', url);
                        throw new Error('WebSocket disabled by Firefox launcher - using HTTP-only mode');
                    };
                    // Remove WebSocket from window object
                    delete window.WebSocket;
                    console.log('WebSocket blocked in Firefox launcher widget');
                };
                // Block WebSocket immediately
                blockWebSocket();
                const widget = new apputils_1.MainAreaWidget({ content });
                widget.id = 'firefox-browser-' + Date.now(); // Unique ID for each session
                widget.title.label = label;
                widget.title.closable = true;
                // Add Firefox icon to the tab
                widget.title.iconClass = 'jp-firefox-icon';
                widget.node.style.height = '100%';
                // Show the widget first with a loading state
                const iframeId = 'firefox-iframe-' + Date.now();
                content.node.innerHTML = `
          <div style="display:flex; justify-content:center; align-items:center; height:100%; background:#f0f0f0;">
            <div style="text-align:center;">
              <div style="font-size:18px; margin-bottom:10px;">🦊</div>
              <div>Starting Firefox session...</div>
            </div>
          </div>
        `;
                app.shell.add(widget, 'main');
                app.shell.activateById(widget.id);
                try {
                    // Use JupyterLab's ServerConnection for authenticated requests
                    const serverSettings = app.serviceManager.serverSettings;
                    // Create a new Firefox session using JupyterLab's request mechanism
                    const response = await services_1.ServerConnection.makeRequest(`${normalizedBaseUrl}firefox/session`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    }, serverSettings);
                    if (!response.ok) {
                        throw new Error(`Failed to create session: ${response.statusText}`);
                    }
                    const sessionData = await response.json();
                    const sessionId = sessionData.session_id;
                    console.log('Firefox session created:', sessionId);
                    // Update the content with the actual Firefox interface
                    content.node.innerHTML = buildFirefoxHTML(iframeId, sessionId, normalizedBaseUrl);
                    // Show status while Firefox starts up
                    const statusDiv = content.node.querySelector('#ff-status');
                    const iframe = content.node.querySelector(`#${iframeId}`);
                    if (statusDiv && iframe) {
                        statusDiv.style.display = 'block';
                        // Additional WebSocket blocking for iframe content
                        iframe.onload = () => {
                            try {
                                // Try to disable WebSocket in iframe if accessible
                                const iframeWindow = iframe.contentWindow;
                                if (iframeWindow && iframeWindow.WebSocket) {
                                    iframeWindow.WebSocket = function (url, protocols) {
                                        console.log('Iframe WebSocket connection blocked:', url);
                                        throw new Error('WebSocket disabled in iframe - using HTTP-only mode');
                                    };
                                    delete iframeWindow.WebSocket;
                                    console.log('WebSocket disabled in iframe content');
                                }
                            }
                            catch (e) {
                                // Ignore cross-origin errors - this is expected and means security is working
                                console.log('Could not access iframe content (cross-origin security)');
                            }
                        };
                        // Wait a bit for Xpra to fully start, then show iframe
                        setTimeout(() => {
                            statusDiv.style.display = 'none';
                            iframe.style.display = 'block';
                        }, 3000);
                    }
                    // Set up event handlers
                    const refreshBtn = content.node.querySelector('#ff-refresh');
                    const closeBtn = content.node.querySelector('#ff-close');
                    refreshBtn === null || refreshBtn === void 0 ? void 0 : refreshBtn.addEventListener('click', () => {
                        if (iframe) {
                            iframe.src = iframe.src;
                        }
                    });
                    closeBtn === null || closeBtn === void 0 ? void 0 : closeBtn.addEventListener('click', () => {
                        widget.close();
                    });
                    // Clean up session when widget is disposed
                    widget.disposed.connect(async () => {
                        try {
                            await services_1.ServerConnection.makeRequest(`${normalizedBaseUrl}firefox/session/${sessionId}`, {
                                method: 'DELETE',
                            }, serverSettings);
                            console.log('Firefox session cleaned up:', sessionId);
                        }
                        catch (error) {
                            console.error('Error cleaning up session:', error);
                        }
                    });
                }
                catch (error) {
                    console.error('Error starting Firefox session:', error);
                    const errorMessage = error instanceof Error ? error.message : String(error);
                    content.node.innerHTML = `
            <div style="display:flex; justify-content:center; align-items:center; height:100%; background:#ffe6e6; color:#d00;">
              <div style="text-align:center;">
                <div style="font-size:18px; margin-bottom:10px;">❌</div>
                <div>Failed to start Firefox session</div>
                <div style="font-size:12px; margin-top:10px;">${errorMessage}</div>
              </div>
            </div>
          `;
                }
            }
        });
        launcher.add({
            command,
            category: 'Other',
            rank: 1,
            // Add Firefox icon to launcher
            kernelIconUrl: `data:image/svg+xml;base64,${btoa(firefoxIconSvg)}`
        });
        palette.addItem({
            command,
            category: 'Other'
        });
    }
};
exports["default"] = extension;


/***/ })

}]);
//# sourceMappingURL=lib_index_js.57de5fee8838a271740b.js.map