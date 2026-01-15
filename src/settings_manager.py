# Edge Light - Settings Manager
# Handles loading/saving user settings to JSON file

import json
import os
import sys
from typing import Any, Dict

from constants import DEFAULT_SETTINGS, SETTINGS_FILENAME


def get_settings_path() -> str:
    """
    Get the path to the settings file.
    Uses the directory where the executable/script is located.
    """
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_dir = os.path.dirname(sys.executable)
    else:
        # Running as script
        base_dir = os.path.dirname(os.path.abspath(__file__))
        base_dir = os.path.dirname(base_dir)  # Go up one level from src/
    
    return os.path.join(base_dir, SETTINGS_FILENAME)


def load_settings() -> Dict[str, Any]:
    """
    Load settings from JSON file.
    Returns default settings if file doesn't exist or is corrupted.
    """
    settings_path = get_settings_path()
    
    try:
        if os.path.exists(settings_path):
            with open(settings_path, 'r', encoding='utf-8') as f:
                saved_settings = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            # (handles case where new settings are added in updates)
            merged = DEFAULT_SETTINGS.copy()
            merged.update(saved_settings)
            return merged
    except (json.JSONDecodeError, IOError, OSError) as e:
        print(f"Warning: Could not load settings: {e}")
    
    return DEFAULT_SETTINGS.copy()


def save_settings(settings: Dict[str, Any]) -> bool:
    """
    Save settings to JSON file.
    Returns True on success, False on failure.
    """
    settings_path = get_settings_path()
    
    try:
        with open(settings_path, 'w', encoding='utf-8') as f:
            json.dump(settings, f, indent=2)
        return True
    except (IOError, OSError) as e:
        print(f"Error: Could not save settings: {e}")
        return False


class SettingsManager:
    """
    Singleton-like settings manager for the application.
    Provides centralized access to settings with auto-save capability.
    """
    
    def __init__(self):
        self._settings = load_settings()
        self._listeners = []
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value."""
        return self._settings.get(key, default)
    
    def set(self, key: str, value: Any, auto_save: bool = True) -> None:
        """Set a setting value and optionally save to disk."""
        self._settings[key] = value
        if auto_save:
            self.save()
        self._notify_listeners(key, value)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all settings as a dictionary."""
        return self._settings.copy()
    
    def save(self) -> bool:
        """Save current settings to disk."""
        return save_settings(self._settings)
    
    def reload(self) -> None:
        """Reload settings from disk."""
        self._settings = load_settings()
    
    def add_listener(self, callback) -> None:
        """Add a callback that gets called when settings change."""
        self._listeners.append(callback)
    
    def remove_listener(self, callback) -> None:
        """Remove a settings change listener."""
        if callback in self._listeners:
            self._listeners.remove(callback)
    
    def _notify_listeners(self, key: str, value: Any) -> None:
        """Notify all listeners of a setting change."""
        for listener in self._listeners:
            try:
                listener(key, value)
            except Exception as e:
                print(f"Error in settings listener: {e}")


# Global settings manager instance
_settings_manager = None


def get_settings_manager() -> SettingsManager:
    """Get the global settings manager instance."""
    global _settings_manager
    if _settings_manager is None:
        _settings_manager = SettingsManager()
    return _settings_manager
