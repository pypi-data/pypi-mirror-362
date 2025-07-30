"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const launcher_1 = require("@jupyterlab/launcher");
/**
 * Firefox Launcher Extension - Frontend Component
 *
 * Adds a Firefox launcher icon to JupyterLab that opens the server-proxy Firefox desktop.
 */
const extension = {
    id: 'jupyterlab-firefox-launcher:plugin',
    autoStart: true,
    requires: [launcher_1.ILauncher],
    activate: (app, launcher) => {
        console.log('Firefox launcher frontend component loaded');
        // Add Firefox launcher to the JupyterLab launcher
        launcher.add({
            command: 'firefox-launcher:open',
            category: 'Other',
            rank: 1
        });
        // Register the command to open Firefox
        app.commands.addCommand('firefox-launcher:open', {
            label: 'Firefox Desktop',
            caption: 'Launch Firefox in a desktop environment via Xpra',
            iconClass: 'jp-FirefoxIcon',
            execute: () => {
                // Open Firefox desktop in a new browser tab/window
                const baseUrl = window.location.origin;
                const firefoxUrl = `${baseUrl}/firefox-desktop/`;
                window.open(firefoxUrl, '_blank');
            }
        });
    }
};
exports.default = extension;
//# sourceMappingURL=index.js.map