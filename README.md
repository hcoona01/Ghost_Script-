# Stealth Vision

A stealthy screen analysis tool that captures your screen, sends it to an AI model for interpretation, and displays the results in an invisible overlay that can be toggled with hotkeys.

## Features

- **Stealth Overlay**: Borderless, transparent window that doesn't steal focus
- **Hotkey Activated**: 
  - `Alt+4`: Capture screen and analyze with AI
  - `Alt+3`: Toggle result visibility
- **AI Powered**: Uses OpenRouter API to interpret screen content
- **Minimal Footprint**: Lightweight Tkinter UI with efficient background processing
- **Error Handling**: Graceful handling of API failures and connection issues

## How It Works

1. Press `Alt+4` to capture your entire screen
2. The screenshot is encoded and sent to an AI model via OpenRouter API
3. The AI analyzes the image and returns a concise response (max 10 words)
4. Results appear in a stealth overlay in the bottom-right corner
5. Press `Alt+3` to show/hide the results

## Requirements

- Python 3.x
- Required packages:
  ```bash
  pip install keyboard pillow requests
  ```
- An OpenRouter API key (get one at [openrouter.ai](https://openrouter.ai))

## Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(or manually install the packages listed above)*
3. Edit `stealth_vision.pyw` and replace `"Your Api Key"` with your actual OpenRouter API key
4. Run the script:
   ```bash
   python stealth_vision.pyw
   ```
   *(or double-click the .pyw file on Windows to run without console)*

## Usage

- Ensure the script is running in the background
- Press `Alt+4` when you want to analyze your current screen
- Wait a moment for the AI to process and return results
- Press `Alt+3` to toggle the visibility of the results overlay
- Results will automatically disappear when a new analysis begins

## Notes

- The overlay appears in the bottom-right corner of your primary monitor
- Initially invisible (text matches background) - becomes visible when results arrive
- Designed to be discreet: no taskbar icon, doesn't activate on click
- Analysis runs in background threads to prevent UI freezing
- Timeout set to 45 seconds for API requests

## Disclaimer

This tool is intended for educational and accessibility purposes. Users should:
- Respect privacy and only analyze their own screen or screens they have permission to view
- Be aware of API usage costs associated with OpenRouter
- Ensure compliance with relevant laws and regulations regarding screen capture and AI usage

## License

MIT License - feel free to modify and distribute as needed.