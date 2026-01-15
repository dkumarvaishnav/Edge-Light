# Edge Light - Global Hotkey Handler
# Uses the 'keyboard' library for reliable Windows hotkey detection

import threading
from typing import Callable, Optional, Dict

try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False
    print("Warning: keyboard library not available, global hotkeys disabled")


def hotkey_to_display_string(hotkey_str: str) -> str:
    """Convert hotkey string to display format like 'Alt+Shift+L'."""
    parts = hotkey_str.lower().replace(' ', '').split('+')
    display_parts = []
    
    for part in parts:
        if part in ('ctrl', 'control'):
            display_parts.append('Ctrl')
        elif part == 'alt':
            display_parts.append('Alt')
        elif part == 'shift':
            display_parts.append('Shift')
        elif part in ('win', 'windows', 'cmd', 'super'):
            display_parts.append('Win')
        elif len(part) == 1:
            display_parts.append(part.upper())
        else:
            display_parts.append(part.capitalize())
    
    return '+'.join(display_parts)


def normalize_hotkey(hotkey_str: str) -> str:
    """Normalize hotkey string for the keyboard library."""
    return hotkey_str.lower().replace(' ', '')


class MultiHotkeyManager:
    """
    Manages multiple global hotkeys.
    Uses the 'keyboard' library for reliable Windows support.
    """
    
    def __init__(self):
        """Initialize the multi-hotkey manager."""
        self._hotkeys: Dict[str, dict] = {}  # name -> {hotkey_str, callback}
        self._running = False
    
    def register_hotkey(self, name: str, hotkey_str: str, callback: Callable[[], None]):
        """
        Register a new hotkey.
        
        Args:
            name: Unique name for this hotkey (e.g., 'toggle', 'open_panel')
            hotkey_str: Hotkey string like 'alt+shift+l'
            callback: Function to call when hotkey is pressed
        """
        normalized = normalize_hotkey(hotkey_str)
        
        # If already running and this hotkey exists, unregister old one first
        if self._running and name in self._hotkeys:
            self._unregister_single(name)
        
        self._hotkeys[name] = {
            'hotkey_str': normalized,
            'callback': callback
        }
        
        # If running, register immediately
        if self._running:
            self._register_single(name)
    
    def update_hotkey(self, name: str, new_hotkey_str: str):
        """Update an existing hotkey's key combination."""
        if name not in self._hotkeys:
            print(f"Hotkey '{name}' not found")
            return
        
        normalized = normalize_hotkey(new_hotkey_str)
        
        if self._running:
            self._unregister_single(name)
        
        self._hotkeys[name]['hotkey_str'] = normalized
        
        if self._running:
            self._register_single(name)
        
        print(f"Hotkey '{name}' changed to: {hotkey_to_display_string(normalized)}")
    
    def get_hotkey(self, name: str) -> str:
        """Get the current hotkey string for a named hotkey."""
        if name in self._hotkeys:
            return self._hotkeys[name]['hotkey_str']
        return ""
    
    def start(self):
        """Start listening for all registered hotkeys."""
        if not KEYBOARD_AVAILABLE:
            print("Hotkey support not available (keyboard library not installed)")
            return
        
        if self._running:
            return
        
        self._running = True
        
        for name in self._hotkeys:
            self._register_single(name)
        
        print("Hotkey manager started")
    
    def stop(self):
        """Stop listening for all hotkeys."""
        for name in self._hotkeys:
            self._unregister_single(name)
        self._running = False
    
    def _register_single(self, name: str):
        """Register a single hotkey."""
        if not KEYBOARD_AVAILABLE or name not in self._hotkeys:
            return
        
        hotkey_info = self._hotkeys[name]
        hotkey_str = hotkey_info['hotkey_str']
        callback = hotkey_info['callback']
        
        try:
            keyboard.add_hotkey(
                hotkey_str,
                callback,
                suppress=False,
                trigger_on_release=False
            )
            print(f"Registered hotkey '{name}': {hotkey_str}")
        except Exception as e:
            print(f"Failed to register hotkey '{name}' ({hotkey_str}): {e}")
    
    def _unregister_single(self, name: str):
        """Unregister a single hotkey."""
        if not KEYBOARD_AVAILABLE or name not in self._hotkeys:
            return
        
        hotkey_str = self._hotkeys[name]['hotkey_str']
        
        try:
            keyboard.remove_hotkey(hotkey_str)
        except (KeyError, ValueError):
            pass
        except Exception as e:
            print(f"Error unregistering hotkey '{name}': {e}")
    
    def is_running(self) -> bool:
        """Check if hotkey manager is running."""
        return self._running


class ThreadSafeMultiHotkeyManager:
    """
    Thread-safe wrapper for multi-hotkey manager that works with Qt.
    Ensures callbacks happen on the main thread via Qt signals.
    """
    
    def __init__(self):
        """Initialize the thread-safe manager."""
        self.manager = MultiHotkeyManager()
        self._signals = {}
    
    def register_hotkey(self, name: str, hotkey_str: str, qt_signal):
        """
        Register a hotkey with a Qt signal.
        
        Args:
            name: Unique name for this hotkey
            hotkey_str: Hotkey string like 'alt+shift+l'
            qt_signal: Qt signal to emit when hotkey is pressed
        """
        self._signals[name] = qt_signal
        self.manager.register_hotkey(name, hotkey_str, lambda: self._emit_signal(name))
    
    def _emit_signal(self, name: str):
        """Emit the Qt signal for the given hotkey name."""
        if name in self._signals:
            try:
                self._signals[name].emit()
            except Exception as e:
                print(f"Error emitting signal for '{name}': {e}")
    
    def update_hotkey(self, name: str, new_hotkey_str: str):
        """Update an existing hotkey."""
        self.manager.update_hotkey(name, new_hotkey_str)
    
    def get_hotkey(self, name: str) -> str:
        """Get the current hotkey string."""
        return self.manager.get_hotkey(name)
    
    def start(self):
        """Start listening for hotkeys."""
        self.manager.start()
    
    def stop(self):
        """Stop listening for hotkeys."""
        self.manager.stop()
