"""Platform abstraction layer for ClipMind.

Handles cross-platform differences between Windows and Linux.
"""

import platform
import os
import sys
import subprocess

SYSTEM = platform.system()  # "Windows" or "Linux"


def get_hotkey_library():
    """Return the appropriate hotkey library for the current platform."""
    if SYSTEM == "Windows":
        import keyboard
        return keyboard
    else:
        # Linux uses pynput
        from pynput import keyboard as pynput_keyboard
        return pynput_keyboard


def get_tray_library():
    """Return the appropriate system tray library."""
    import pystray
    return pystray


def get_icon_path():
    """Return path to the app icon."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base, "assets", "icon.png")
    if os.path.exists(icon_path):
        return icon_path
    return None


def add_to_startup():
    """Add ClipMind to system startup."""
    if SYSTEM == "Windows":
        _add_to_startup_windows()
    elif SYSTEM == "Linux":
        _add_to_startup_linux()


def _add_to_startup_windows():
    """Add to Windows registry Run key."""
    import winreg
    exe_path = sys.executable
    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
    
    # If running as PyInstaller exe
    if getattr(sys, 'frozen', False):
        target = sys.executable
    else:
        target = f'"{exe_path}" "{script_path}"'
    
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "ClipMind", 0, winreg.REG_SZ, target)
        winreg.CloseKey(key)
        return True
    except Exception:
        return False


def _add_to_startup_linux():
    """Add to Linux autostart via .desktop file."""
    autostart_dir = os.path.join(os.path.expanduser("~"), ".config", "autostart")
    os.makedirs(autostart_dir, exist_ok=True)
    
    desktop_file = os.path.join(autostart_dir, "clipmind.desktop")
    
    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "main.py")
    
    content = f"""[Desktop Entry]
Type=Application
Name=ClipMind
Comment=AI Clipboard Assistant
Exec=python3 {script_path}
Terminal=false
Categories=Utility;
X-GNOME-Autostart-enabled=true
"""
    try:
        with open(desktop_file, "w") as f:
            f.write(content)
        os.chmod(desktop_file, 0o755)
        return True
    except Exception:
        return False


def remove_from_startup():
    """Remove ClipMind from system startup."""
    if SYSTEM == "Windows":
        _remove_from_startup_windows()
    elif SYSTEM == "Linux":
        _remove_from_startup_linux()


def _remove_from_startup_windows():
    """Remove from Windows registry."""
    import winreg
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(key, "ClipMind")
        winreg.CloseKey(key)
        return True
    except Exception:
        return False


def _remove_from_startup_linux():
    """Remove Linux autostart."""
    desktop_file = os.path.join(
        os.path.expanduser("~"), ".config", "autostart", "clipmind.desktop"
    )
    if os.path.exists(desktop_file):
        os.remove(desktop_file)
        return True
    return False


def show_notification(title, message):
    """Show a system notification."""
    if SYSTEM == "Windows":
        try:
            from plyer import notification
            notification.notify(title=title, message=message, timeout=3)
        except ImportError:
            pass
    elif SYSTEM == "Linux":
        try:
            subprocess.run(
                ["notify-send", title, message],
                capture_output=True, timeout=5
            )
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
