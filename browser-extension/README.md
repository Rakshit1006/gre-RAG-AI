# GRE Mentor Browser Extension

Browser extension for clipping content from web pages and sending it to your local GRE Mentor app.

## Installation

### Chrome/Edge

1. Open Chrome/Edge and navigate to `chrome://extensions/`
2. Enable "Developer mode" (toggle in top right)
3. Click "Load unpacked"
4. Select the `browser-extension` folder

### Firefox

1. Open Firefox and navigate to `about:debugging#/runtime/this-firefox`
2. Click "Load Temporary Add-on"
3. Select the `manifest.json` file in the `browser-extension` folder

## Usage

### Method 1: Context Menu
1. Select text on any webpage
2. Right-click and choose "Explain with GRE Mentor"

### Method 2: Keyboard Shortcut
1. Select text
2. Press `Cmd+Shift+Y` (Mac) or `Ctrl+Shift+Y` (Windows/Linux)

### Method 3: Floating Button
1. Select text
2. Click the floating "Clip to GRE Mentor" button that appears

## Requirements

- GRE Mentor backend must be running at `http://localhost:8000`
- The extension will show a connection status in the popup

## Features

- Automatically detects content type (word, question, or concept)
- Generates mnemonics for vocabulary words
- Extracts and saves questions with explanations
- Shows notification on successful save

## Privacy

- All data stays local
- No external requests (except to your local backend)
- No tracking or analytics
