# Edge Light - Windows Auto-Start Manager
# Handles adding/removing Edge Light from Windows startup

import os
import sys
import winreg

APP_NAME = "EdgeLight"
REGISTRY_PATH = r"Software\Microsoft\Windows\CurrentVersion\Run"


def get_executable_path() -> str:
    """Get the path to the current executable or script."""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return sys.executable
    else:
        # Running as script - use pythonw to avoid console
        python_path = sys.executable
        script_path = os.path.abspath(os.path.join(
            os.path.dirname(__file__), 'main.py'
        ))
        return f'"{python_path}" "{script_path}"'


def is_autostart_enabled() -> bool:
    """Check if Edge Light is set to start with Windows."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REGISTRY_PATH,
            0,
            winreg.KEY_READ
        )
        try:
            value, _ = winreg.QueryValueEx(key, APP_NAME)
            winreg.CloseKey(key)
            return True
        except WindowsError:
            winreg.CloseKey(key)
            return False
    except WindowsError:
        return False


def enable_autostart() -> bool:
    """Add Edge Light to Windows startup."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REGISTRY_PATH,
            0,
            winreg.KEY_SET_VALUE
        )
        
        exe_path = get_executable_path()
        winreg.SetValueEx(key, APP_NAME, 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        
        print(f"Auto-start enabled: {exe_path}")
        return True
    except WindowsError as e:
        print(f"Failed to enable auto-start: {e}")
        return False


def disable_autostart() -> bool:
    """Remove Edge Light from Windows startup."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            REGISTRY_PATH,
            0,
            winreg.KEY_SET_VALUE
        )
        
        try:
            winreg.DeleteValue(key, APP_NAME)
        except WindowsError:
            pass  # Key doesn't exist, that's fine
        
        winreg.CloseKey(key)
        print("Auto-start disabled")
        return True
    except WindowsError as e:
        print(f"Failed to disable auto-start: {e}")
        return False


def set_autostart(enabled: bool) -> bool:
    """Enable or disable auto-start."""
    if enabled:
        return enable_autostart()
    else:
        return disable_autostart()
