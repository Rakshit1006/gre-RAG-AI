// Background service worker for GRE Mentor Clipper

const API_BASE_URL = 'http://localhost:8000';

// Create context menu
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'gre-mentor-clip',
    title: 'Explain with GRE Mentor',
    contexts: ['selection']
  });
});

// Handle context menu clicks
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'gre-mentor-clip' && info.selectionText) {
    clipSelection(info.selectionText, tab.url, tab.title);
  }
});

// Handle keyboard shortcut
chrome.commands.onCommand.addListener((command) => {
  if (command === 'clip-selection') {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      chrome.tabs.sendMessage(tabs[0].id, { action: 'getSelection' });
    });
  }
});

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'clipText') {
    clipSelection(request.text, request.url, request.title);
    sendResponse({ success: true });
  }
  return true;
});

// Function to send clipped content to backend
async function clipSelection(text, url, title) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/v1/ingest/clip`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        text: text,
        url: url,
        title: title,
        hint: 'auto',
        save: true
      })
    });

    if (response.ok) {
      const data = await response.json();
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon48.png',
        title: 'GRE Mentor',
        message: `Saved as ${data.type}: "${text.substring(0, 50)}..."`,
        priority: 2
      });
    } else {
      throw new Error('Failed to clip content');
    }
  } catch (error) {
    console.error('Clip error:', error);
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon48.png',
      title: 'GRE Mentor Error',
      message: 'Failed to save content. Make sure the backend is running.',
      priority: 2
    });
  }
}
