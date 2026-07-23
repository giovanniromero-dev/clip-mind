"""Clipboard operations for ClipMind."""

import pyperclip
import time


def copy_selection():
    """Simulate Ctrl+C to copy selected text to clipboard."""
    import platform as _platform
    if _platform.system() == "Windows":
        import keyboard
        keyboard.send('ctrl+c')
    else:
        import subprocess
        try:
            subprocess.run(['xdotool', 'key', 'ctrl+c'], capture_output=True, timeout=2)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
    time.sleep(0.15)


def get_selected_text():
    """Read text from clipboard."""
    try:
        time.sleep(0.1)
        text = pyperclip.paste()
        return text
    except Exception as e:
        raise RuntimeError(f"Error reading clipboard: {e}")


def copy_to_clipboard(text):
    """Copy text to clipboard."""
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        raise RuntimeError(f"Error copying to clipboard: {e}")


def restore_clipboard(text):
    """Restore previous clipboard content."""
    try:
        pyperclip.copy(text)
        return True
    except Exception as e:
        raise RuntimeError(f"Error restoring clipboard: {e}")
