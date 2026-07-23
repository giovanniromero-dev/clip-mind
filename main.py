#!/usr/bin/env python3
"""ClipMind - AI Clipboard Assistant.

System tray app that captures selected text and sends it to an LLM.
Supports Windows and Linux.
"""

import sys
import os
import threading
import time

# Add src to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.config import load_config, save_config
from src.clipboard import copy_selection, get_selected_text
from src.llm_client import LLMClient, SYSTEM_PROMPTS
from src.popup import ClipMindPopup
from src.tray import TrayManager
from src.hotkey import HotkeyManager
from src.platform import add_to_startup, show_notification


class ClipMindApp:
    """Main application controller."""

    def __init__(self):
        self.config = load_config()
        self.popup = ClipMindPopup(
            on_action=self._handle_action, on_close=self._on_popup_close
        )
        self.tray = TrayManager(on_exit=self._exit, on_open_config=self._open_config)
        self.hotkey = HotkeyManager(on_activate=self._on_hotkey)
        self.llm_client = LLMClient(self.config)
        self.selected_text = ""
        self.last_action = ""
        self.running = False


    def start(self):
        """Start the application (tray, hotkey listener)."""
        self.running = True
        # Start tray icon
        self.tray.start()
        # Start hotkey listener in a daemon thread
        hotkey_thread = threading.Thread(target=self.hotkey.start, daemon=True)
        hotkey_thread.start()
        show_notification('ClipMind', 'ClipMind iniciado. Presiona Alt+C+M para usar.')

        # Keep main thread alive
        try:
            while self.running:
                time.sleep(0.5)
        except KeyboardInterrupt:
            self._exit()


    def _on_hotkey(self):
        """Called when the global hotkey is pressed."""
        try:
            # Get selected text
            copy_selection()

            # Get selected text from clipboard
            text = get_selected_text()

            if not text or text.strip() == "":
                self.popup.show_error(
                    "No hay texto seleccionado.\nSelecciona texto y presiona Alt+C+M."
                )
                return

            self.selected_text = text

            # Show action popup
            self.popup.show_actions(text)

        except Exception as e:
            self.popup.show_error(f"Error al capturar texto:\n{e}")

    def _handle_action(self, action):
        """Handle an action button click."""
        self.last_action = action

        if not self.selected_text:
            self.popup.show_error("No hay texto para procesar.")
            return

        # Show loading
        self.popup.show_loading()

        # Process in background thread
        thread = threading.Thread(
            target=self._process_action, args=(action,), daemon=True
        )
        thread.start()

    def _process_action(self, action):
        """Process the action in a background thread."""
        try:
            system_prompt = SYSTEM_PROMPTS.get(action, SYSTEM_PROMPTS["responder"])
            result = self.llm_client.ask(system_prompt, self.selected_text)

            # Show result in popup (must be in main thread)
            self.popup.window.after(0, lambda: self.popup.show_result(result))

        except Exception as e:
            self.popup.window.after(0, lambda e=e: self.popup.show_error(str(e)))

    def _on_popup_close(self):
        """Called when the popup is closed."""
        pass

    def _open_config(self):
        """Open configuration window."""

        def on_save(new_config):
            self.config = new_config
            save_config(new_config)
            self.llm_client = LLMClient(new_config)
            show_notification("ClipMind", "✅ Configuración guardada")

        self.popup.show_config_wizard(self.config, on_save)

    def _exit(self):
        """Exit the application."""
        self.running = False
        self.hotkey.stop()
        self.tray.stop()
        sys.exit(0)


def main():
    """Entry point."""
    app = ClipMindApp()
    app.start()


if __name__ == "__main__":
    main()

