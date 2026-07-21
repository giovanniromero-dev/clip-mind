"""Global hotkey registration for ClipMind.

Uses keyboard library on Windows, pynput on Linux.
"""

import platform
import threading
import time

SYSTEM = platform.system()


class HotkeyManager:
    """Manages global hotkey registration."""

    def __init__(self, on_activate):
        self.on_activate = on_activate
        self.listener = None
        self.running = False
        self._hotkey = "ctrl+c+m"

    def start(self, hotkey=None):
        """Start listening for the hotkey."""
        if hotkey:
            self._hotkey = hotkey
        
        self.running = True
        
        if SYSTEM == "Windows":
            self._start_windows()
        else:
            self._start_linux()

    def _start_windows(self):
        """Start hotkey listener on Windows using keyboard library."""
        import keyboard
        
        def callback(e):
            if self.on_activate:
                self.on_activate()
        
        # Register the hotkey
        keyboard.add_hotkey(self._hotkey, callback)
        
        # Keep the thread alive
        while self.running:
            time.sleep(0.1)

    def _start_linux(self):
        """Start hotkey listener on Linux using pynput."""
        from pynput import keyboard
        
        # Parse hotkey like "ctrl+c+m"
        keys = self._hotkey.lower().split("+")
        self._required_keys = set(keys)
        self._pressed_keys = set()
        
        def on_press(key):
            try:
                key_name = key.name.lower() if hasattr(key, 'name') else key.char.lower()
            except (AttributeError, ValueError):
                return
            
            self._pressed_keys.add(key_name)
            
            if self._pressed_keys == self._required_keys:
                if self.on_activate:
                    self.on_activate()
        
        def on_release(key):
            try:
                key_name = key.name.lower() if hasattr(key, 'name') else key.char.lower()
            except (AttributeError, ValueError):
                return
            self._pressed_keys.discard(key_name)
        
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()
        self.listener.join()

    def stop(self):
        """Stop the hotkey listener."""
        self.running = False
        if SYSTEM == "Windows":
            import keyboard
            keyboard.unhook_all()
        elif self.listener:
            self.listener.stop()
