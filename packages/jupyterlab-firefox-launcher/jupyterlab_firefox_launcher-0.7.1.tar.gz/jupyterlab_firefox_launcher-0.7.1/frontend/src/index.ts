import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ILauncher } from '@jupyterlab/launcher';

/**
 * Firefox Launcher Extension - Frontend Component
 * 
 * Adds a Firefox launcher icon to JupyterLab that opens the server-proxy Firefox desktop.
 */
const extension: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-firefox-launcher:plugin',
  autoStart: true,
  requires: [ILauncher],
  activate: (app: JupyterFrontEnd, launcher: ILauncher) => {
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

export default extension;