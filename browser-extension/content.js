// Content script for GRE Mentor Clipper

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getSelection') {
    const selectedText = window.getSelection().toString().trim();
    if (selectedText) {
      chrome.runtime.sendMessage({
        action: 'clipText',
        text: selectedText,
        url: window.location.href,
        title: document.title
      });
    }
    sendResponse({ success: true });
  }
  return true;
});

// Create floating button when text is selected
let floatingButton = null;

document.addEventListener('mouseup', () => {
  const selectedText = window.getSelection().toString().trim();
  
  if (selectedText && selectedText.length > 0) {
    showFloatingButton();
  } else {
    hideFloatingButton();
  }
});

function showFloatingButton() {
  if (!floatingButton) {
    floatingButton = document.createElement('div');
    floatingButton.id = 'gre-mentor-clip-button';
    floatingButton.innerHTML = '📚 Clip to GRE Mentor';
    floatingButton.className = 'gre-mentor-floating-button';
    
    floatingButton.addEventListener('click', () => {
      const selectedText = window.getSelection().toString().trim();
      if (selectedText) {
        chrome.runtime.sendMessage({
          action: 'clipText',
          text: selectedText,
          url: window.location.href,
          title: document.title
        });
        hideFloatingButton();
      }
    });
    
    document.body.appendChild(floatingButton);
  }
  
  // Position the button near the selection
  const selection = window.getSelection();
  if (selection.rangeCount > 0) {
    const range = selection.getRangeAt(0);
    const rect = range.getBoundingClientRect();
    floatingButton.style.top = `${rect.bottom + window.scrollY + 5}px`;
    floatingButton.style.left = `${rect.left + window.scrollX}px`;
    floatingButton.style.display = 'block';
  }
}

function hideFloatingButton() {
  if (floatingButton) {
    floatingButton.style.display = 'none';
  }
}

// Hide button when clicking elsewhere
document.addEventListener('click', (e) => {
  if (floatingButton && e.target !== floatingButton) {
    hideFloatingButton();
  }
});
