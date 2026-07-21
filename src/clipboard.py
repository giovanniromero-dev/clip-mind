"""Clipboard operations for ClipMind."""

import pyperclip
import time


def get_selected_text():
    """Read text from clipboard (simulates getting selected text)."""
    try:
        # Save current clipboard content
        old_content = pyperclip.paste()
        
        # Small delay to ensure clipboard is updated
        time.sleep(0.1)
        
        # Try to get new content (user should have copied with Ctrl+C)
        new_content = pyperclip.paste()
        
        return new_content, old_content
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
