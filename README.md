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

## Installation

### Download the Installer (Recommended)

The easiest way to install Edge Light is to download the installer:

[Download EdgeLight_Setup_v1.1.0.exe](https://github.com/dkumarvaishnav/Edge-Light/releases/download/v1.1.0/EdgeLight_Setup_v1.1.0.exe)

1. Download the installer from the link above
2. Run the installer and follow the setup wizard
3. Edge Light will be installed with Start Menu shortcuts
4. Launch Edge Light from the Start Menu or let it start with Windows

---

## Alternative Installation Methods

### Option A: Run the Portable Executable

If you prefer not to install, you can download and run the standalone executable:

1. Download `EdgeLight.exe` from the [Releases page](https://github.com/dkumarvaishnav/Edge-Light/releases)
2. Run it directly - the app starts minimized to the system tray
3. Click the tray icon to open settings

### Option B: Run from Source

For developers who want to run from source code:

1. Install Python 3.8 or later
2. Clone this repository
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the application:
   ```
   python src/main.py
   ```

---

## Usage

### Default Hotkeys

| Action | Hotkey |
|--------|--------|
| Toggle Light | Alt+Shift+L |
| Open/Close Panel | Alt+Shift+P |

You can remap these by clicking the hotkey buttons in the settings panel.

### Settings

Click the system tray icon to access:
- Brightness slider
- Color temperature slider
- Width slider
- Edge selection buttons
- Hotkey configuration
- Auto-start toggle

## Building the Installer

To build the installer yourself:

1. Install Inno Setup
2. Build the executable:
   ```
   python build.py
   ```
3. Compile the installer:
   ```
   iscc installer.iss
   ```

The installer will be created in the `installer` folder.

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
- Python 3.8 or later (only for running from source)
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
│   └── EdgeLight.exe        # Portable executable
├── installer/
│   └── EdgeLight_Setup_v1.1.0.exe  # Windows installer
├── icon.ico                 # Application icon
├── installer.iss            # Inno Setup script
├── requirements.txt         # Python dependencies
├── build.py                 # Executable build script
└── README.md
```

## License

MIT License - See LICENSE for details.
