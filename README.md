# Edge Light

A lightweight Windows utility that uses your laptop screen as a front-facing light source for better webcam visibility in dark environments.

## Features

- **Solid Ring Light Overlay** - Clean, solid-colored light rendered around screen edges
- **Adjustable Brightness** - Fine control over light intensity from 0 to 100 percent
- **Adjustable Color Temperature** - Warm (2700K) to cool (6500K) tones
- **Adjustable Width** - Control how thick the ring light appears (50-400 pixels)
- **Edge Selection** - Choose which edges glow: All, Top Only, Top + Sides, or Sides Only
- **Click-Through Overlay** - Never blocks mouse or keyboard input
- **Always-On-Top** - Stays visible over all windows
- **System Tray Operation** - No taskbar presence, lives in the system tray
- **Global Hotkeys** - Toggle light and open settings panel with keyboard shortcuts
- **Remappable Hotkeys** - Click the hotkey buttons to set your own key combinations
- **Auto-Start Option** - Launch with Windows automatically
- **Persistent Settings** - All preferences are saved between sessions

## Quick Start

### Option 1: Run the Executable

1. Download `EdgeLight.exe` from the `dist` folder
2. Run it - the app starts minimized to the system tray
3. Click the tray icon to open settings
4. Press your hotkey to toggle the light

### Option 2: Run from Source

1. Install Python 3.8 or later
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python src/main.py
   ```

## Default Hotkeys

| Action | Hotkey |
|--------|--------|
| Toggle Light | Alt+Shift+L |
| Open/Close Panel | Alt+Shift+P |

You can remap these by clicking the hotkey buttons in the settings panel.

## Building the Executable

To create a standalone executable:

```
python build.py
```

The executable will be created in the `dist` folder.

## Privacy and Trust

Edge Light is designed with privacy in mind:

- No camera access
- No screen capture
- No network requests
- No data collection
- 100% local operation
- Open source

## System Requirements

- Windows 10 or Windows 11
- Python 3.8 or later (for running from source)
- Approximately 50MB RAM usage
- No administrator privileges required

## Project Structure

```
Edge-Light/
├── src/
│   ├── main.py              # Application entry point
│   ├── overlay.py           # Ring light overlay rendering
│   ├── tray.py              # System tray interface
│   ├── settings_manager.py  # Settings persistence
│   ├── hotkey.py            # Global hotkey handling
│   ├── autostart.py         # Windows startup management
│   └── constants.py         # Configuration constants
├── dist/
│   └── EdgeLight.exe        # Standalone executable
├── icon.ico                 # Application icon
├── requirements.txt         # Python dependencies
├── build.py                 # Executable build script
└── README.md
```

## License

MIT License - See LICENSE for details.
