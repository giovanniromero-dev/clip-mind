"""System tray icon for ClipMind."""

import threading
from PIL import Image, ImageDraw


def create_icon():
    """Create a simple brain icon for the system tray."""
    size = 64
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Draw a simple brain/mind icon
    # Circle background
    draw.ellipse([4, 4, 60, 60], fill=(100, 100, 255, 200))

    # Inner circle (lighter)
    draw.ellipse([12, 12, 52, 52], fill=(70, 70, 200, 180))

    # Brain lines
    draw.arc([16, 16, 48, 48], 0, 360, fill=(180, 180, 255, 200), width=2)
    draw.arc([20, 20, 44, 44], 0, 360, fill=(180, 180, 255, 200), width=2)

    # Center dot
    draw.ellipse([29, 29, 35, 35], fill=(220, 220, 255, 255))

    return image


class TrayManager:
    """Manages the system tray icon and menu."""

    def __init__(self, on_exit=None, on_open_config=None):
        self.on_exit = on_exit
        self.on_open_config = on_open_config
        self.icon = None
        self.running = False

    def start(self):
        """Start the system tray icon in a background thread."""
        self.running = True
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self):
        """Run the tray icon (blocking)."""
        import pystray
        from pystray import MenuItem as item

        icon_image = create_icon()

        menu = [
            item("ClipMind activo", None, enabled=False),
            item("Configuración", self._open_config),
            item("Probar conexión", self._test_connection),
            item("Salir", self._exit_app)
        ]

        self.icon = pystray.Icon(
            "clipmind", icon_image, "ClipMind - Presiona Alt+C+M", menu
        )

        self.icon.run()

    def _open_config(self):
        if self.on_open_config:
            self.on_open_config()

    def _test_connection(self):
        if self.icon:
            try:
                from src.llm_client import LLMClient
                from src.config import load_config
                config = load_config()
                client = LLMClient(config)
                success, msg = client.test_connection()
                if success:
                    self.icon.notify("Conexión exitosa con " + config["provider"])
                else:
                    self.icon.notify("Error: " + msg)
            except Exception as e:
                self.icon.notify(f"Error: {e}")

    def _exit_app(self):
        self.running = False
        if self.icon:
            self.icon.stop()
        if self.on_exit:
            self.on_exit()

    def stop(self):
        self.running = False
        if self.icon:
            self.icon.stop()

    def notify(self, message):
        if self.icon:
            self.icon.notify(message)
