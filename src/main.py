# Edge Light - Main Entry Point
# Lightweight screen-edge glow utility for webcam lighting

import sys
import os

# Add src directory to path for imports
if getattr(sys, 'frozen', False):
    src_dir = os.path.dirname(sys.executable)
else:
    src_dir = os.path.dirname(os.path.abspath(__file__))
    
sys.path.insert(0, src_dir)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QObject, pyqtSignal

from constants import APP_NAME
from settings_manager import get_settings_manager
from overlay import GlowOverlay
from tray import TrayManager
from hotkey import ThreadSafeMultiHotkeyManager, hotkey_to_display_string


class HotkeySignalBridge(QObject):
    """Bridge to emit Qt signals from hotkey threads."""
    toggle_pressed = pyqtSignal()
    panel_pressed = pyqtSignal()


def main():
    """Main entry point for Edge Light application."""
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setQuitOnLastWindowClosed(False)
    
    # Apply dark theme
    app.setStyleSheet("""
        QToolTip {
            background-color: #2D2D2D;
            color: #E0E0E0;
            border: 1px solid #404040;
            padding: 5px;
            border-radius: 3px;
        }
    """)
    
    # Initialize settings and get saved hotkeys
    settings = get_settings_manager()
    hotkey_toggle = settings.get('hotkey_toggle', 'alt+shift+l')
    hotkey_panel = settings.get('hotkey_panel', 'alt+shift+p')
    
    # Initialize components
    overlay = GlowOverlay()
    
    # Setup hotkey bridge (converts thread callbacks to Qt signals)
    hotkey_bridge = HotkeySignalBridge()
    
    # Create multi-hotkey manager
    hotkey_manager = ThreadSafeMultiHotkeyManager()
    
    # Create tray manager
    tray = TrayManager(overlay, settings, hotkey_manager)
    
    # Register hotkeys with their signals
    hotkey_manager.register_hotkey('toggle', hotkey_toggle, hotkey_bridge.toggle_pressed)
    hotkey_manager.register_hotkey('panel', hotkey_panel, hotkey_bridge.panel_pressed)
    
    # Connect hotkey signals to tray actions
    hotkey_bridge.toggle_pressed.connect(tray.toggle)
    hotkey_bridge.panel_pressed.connect(tray.open_panel)
    
    # Start hotkey listener
    hotkey_manager.start()
    
    # Show startup notification
    toggle_display = hotkey_to_display_string(hotkey_toggle)
    panel_display = hotkey_to_display_string(hotkey_panel)
    tray.show_notification(
        f"{APP_NAME} Started",
        f"Toggle: {toggle_display} | Panel: {panel_display}"
    )
    
    # Run application
    exit_code = app.exec_()
    
    # Cleanup
    hotkey_manager.stop()
    settings.save()
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
