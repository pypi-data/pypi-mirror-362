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
const buildFirefoxHTML = (iframeId, url) => {
    return `
    <div style="display:flex; justify-content:end; padding:4px; gap:8px; background:#f5f5f5;">
      <button id="ff-refresh">🔄 Refresh</button>
      <button id="ff-close">❌ Close</button>
    </div>
    <iframe 
      id="${iframeId}"
      src="${url}" 
      style="width:100%; height:90%; border:none;"
      allowfullscreen
    ></iframe>`;
};
exports.buildFirefoxHTML = buildFirefoxHTML;
const extension = {
    id: 'jupyterlab-firefox-launcher:plugin',
    description: 'JupyterLab extension to launch Firefox in a tab',
    autoStart: true,
    requires: [launcher_1.ILauncher, apputils_1.ICommandPalette],
    activate: async (app, launcher, palette) => {
        const command = 'firefox:open';
        const label = 'Firefox Browser';
        app.commands.addCommand(command, {
            label,
            execute: async () => {
                var _a, _b;
                // Use our custom Firefox endpoint that serves the nice interface
                const baseUrl = app.serviceManager.serverSettings.baseUrl;
                // Ensure baseUrl ends with slash and construct proper URL to our custom endpoint
                const normalizedBaseUrl = baseUrl.endsWith('/') ? baseUrl : baseUrl + '/';
                const firefoxUrl = `${normalizedBaseUrl}firefox/`;
                console.log('Firefox URL:', firefoxUrl); // Debug logging
                const content = new widgets_1.Widget();
                content.node.style.height = '100%';
                content.node.style.width = '100%';
                content.node.style.overflow = 'hidden';
                const iframeId = 'firefox-iframe';
                content.node.innerHTML = buildFirefoxHTML(iframeId, firefoxUrl);
                const widget = new apputils_1.MainAreaWidget({ content });
                widget.id = 'firefox-browser';
                widget.title.label = label;
                widget.title.closable = true;
                widget.node.style.height = '100%';
                app.shell.add(widget, 'main');
                app.shell.activateById(widget.id);
                const iframe = content.node.querySelector(`#${iframeId}`);
                if (!iframe) {
                    console.error('Firefox iframe not found');
                    return;
                }
                (_a = content.node.querySelector('#ff-refresh')) === null || _a === void 0 ? void 0 : _a.addEventListener('click', () => {
                    iframe.src = iframe.src;
                });
                (_b = content.node.querySelector('#ff-close')) === null || _b === void 0 ? void 0 : _b.addEventListener('click', () => {
                    widget.close();
                });
            }
        });
        launcher.add({
            command,
            category: 'Other',
            rank: 1
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
//# sourceMappingURL=lib_index_js.7e6da53b8082dc1dd7cd.js.map