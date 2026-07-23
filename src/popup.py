"""Popup window for ClipMind."""

import tkinter as tk
from tkinter import ttk


class ClipMindPopup:
    """Popup window with action buttons and result display."""

    def __init__(self, on_action, on_close=None):
        self.on_action = on_action
        self.on_close = on_close
        self.window = None
        self.result_text = None
        self.loading_label = None

    def show_actions(self, selected_text):
        """Show the action selection popup."""
        self._create_window("🧠 ClipMind", "300x200")

        # Selected text preview
        preview = (
            selected_text[:80] + "..." if len(selected_text) > 80 else selected_text
        )
        tk.Label(
            self.window,
            text=f"Texto: {preview}",
            wraplength=260,
            font=("Segoe UI", 9),
            fg="#888",
        ).pack(pady=(10, 5))

        tk.Label(
            self.window, text="¿Qué quieres hacer?", font=("Segoe UI", 12, "bold")
        ).pack(pady=(5, 10))

        # Action buttons frame
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=5)

        actions = [
            ("📝 Resumir", "resumir"),
            ("🌍 Traducir", "traducir"),
            ("❓ Explicar", "explicar"),
            ("💬 Responder", "responder"),
        ]

        for text, action in actions:
            btn = tk.Button(
                btn_frame,
                text=text,
                width=14,
                height=1,
                font=("Segoe UI", 10),
                cursor="hand2",
                command=lambda a=action: self._handle_action(a),
            )
            btn.pack(pady=3)

        # Close button
        tk.Button(
            self.window,
            text="✕ Cerrar",
            font=("Segoe UI", 8),
            fg="#888",
            bd=0,
            command=self.close,
        ).pack(pady=(5, 5))

        self._center_window()
        self.window.focus_force()

    def show_result(self, result):
        """Show the result from the LLM."""
        self._clear_window()
        self.window.geometry("500x400")
        self.window.title("🧠 ClipMind - Resultado")

        tk.Label(self.window, text="Resultado:", font=("Segoe UI", 12, "bold")).pack(
            pady=(10, 5)
        )

        # Result text area
        text_frame = tk.Frame(self.window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.result_text = tk.Text(
            text_frame,
            wrap=tk.WORD,
            font=("Segoe UI", 10),
            bg="#2b2b2b" if self._is_dark_theme() else "#ffffff",
            fg="#ffffff" if self._is_dark_theme() else "#000000",
            relief=tk.FLAT,
            padx=10,
            pady=10,
        )
        self.result_text.insert(tk.END, result)
        self.result_text.config(state=tk.DISABLED)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = tk.Scrollbar(text_frame, command=self.result_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.config(yscrollcommand=scrollbar.set)

        # Bottom buttons
        btn_frame = tk.Frame(self.window)
        btn_frame.pack(pady=10)

        tk.Button(
            btn_frame,
            text="📋 Copiar",
            width=10,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self._copy_result,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="↻ Repetir",
            width=10,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self._repeat_action,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            btn_frame,
            text="✕ Cerrar",
            width=10,
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.close,
        ).pack(side=tk.LEFT, padx=5)

        self._center_window()
        self.window.focus_force()

    def show_loading(self):
        """Show loading indicator."""
        self._clear_window()
        self.window.geometry("300x150")
        self.window.title("🧠 ClipMind - Procesando...")

        self.loading_label = tk.Label(
            self.window,
            text="⏳ Procesando con IA...",
            font=("Segoe UI", 12),
            fg="#888",
        )
        self.loading_label.pack(expand=True)

        self._center_window()

    def show_error(self, message):
        """Show error message."""
        self._clear_window()
        self.window.geometry("400x150")
        self.window.title("🧠 ClipMind - Error")

        tk.Label(
            self.window, text="⚠️ Error", font=("Segoe UI", 12, "bold"), fg="#ff4444"
        ).pack(pady=(15, 5))

        tk.Label(
            self.window, text=message, wraplength=350, font=("Segoe UI", 10), fg="#888"
        ).pack(pady=5)

        tk.Button(
            self.window,
            text="✕ Cerrar",
            font=("Segoe UI", 10),
            cursor="hand2",
            command=self.close,
        ).pack(pady=10)

        self._center_window()

    def show_config_wizard(self, config, on_save):
        """Show first-time configuration wizard."""
        self._create_window("🧠 ClipMind - Configuración inicial", "450x350")

        tk.Label(
            self.window, text="Bienvenido a ClipMind", font=("Segoe UI", 14, "bold")
        ).pack(pady=(15, 5))

        tk.Label(
            self.window,
            text="Necesitas configurar tu proveedor de IA",
            font=("Segoe UI", 10),
            fg="#888",
        ).pack(pady=(0, 15))

        # Provider selection
        tk.Label(self.window, text="Proveedor:", font=("Segoe UI", 10)).pack(
            anchor=tk.W, padx=20
        )
        provider_var = tk.StringVar(value=config.get("provider", "deepseek"))
        provider_combo = ttk.Combobox(
            self.window,
            textvariable=provider_var,
            values=["deepseek", "openai", "ollama"],
            state="readonly",
            width=30,
        )
        provider_combo.pack(pady=(0, 10), padx=20)

        # API Key
        tk.Label(
            self.window,
            text="API Key (dejar vacío si usas Ollama):",
            font=("Segoe UI", 10),
        ).pack(anchor=tk.W, padx=20)
        api_entry = tk.Entry(self.window, width=40, show="*")
        api_entry.insert(0, config.get("api_key", ""))
        api_entry.pack(pady=(0, 10), padx=20)

        # Model
        tk.Label(self.window, text="Modelo:", font=("Segoe UI", 10)).pack(
            anchor=tk.W, padx=20
        )
        model_entry = tk.Entry(self.window, width=40)
        model_entry.insert(0, config.get("model", "deepseek-chat"))
        model_entry.pack(pady=(0, 15), padx=20)

        def save():
            config["provider"] = provider_var.get()
            config["api_key"] = api_entry.get()
            config["model"] = model_entry.get()
            on_save(config)
            self.close()

        tk.Button(
            self.window,
            text="✓ Guardar y continuar",
            font=("Segoe UI", 11),
            bg="#4CAF50",
            fg="white",
            cursor="hand2",
            command=save,
        ).pack(pady=10)

        self._center_window()
        self.window.focus_force()

    def _handle_action(self, action):
        """Handle action button click and store last action."""
        self._last_action = action
        if self.on_action:
            self.on_action(action)

    def _copy_result(self):
        """Copy result to clipboard."""
        if self.result_text:
            text = self.result_text.get("1.0", tk.END).strip()
            try:
                import pyperclip

                pyperclip.copy(text)
                self._show_tooltip("✓ Copiado al portapapeles")
            except Exception:
                self._show_tooltip("Error al copiar")

    def _repeat_action(self):
        """Repeat the last action."""
        if self.on_action and hasattr(self, "_last_action"):
            self.on_action(self._last_action)

    def _show_tooltip(self, message):
        """Show a temporary tooltip."""
        tooltip = tk.Toplevel(self.window)
        tooltip.overrideredirect(True)
        tooltip.attributes("-topmost", True)

        tk.Label(
            tooltip,
            text=message,
            font=("Segoe UI", 10),
            bg="#333",
            fg="white",
            padx=15,
            pady=5,
        ).pack()

        # Position near the window center
        x = self.window.winfo_x() + self.window.winfo_width() // 2 - 75
        y = self.window.winfo_y() + self.window.winfo_height() // 2 - 20
        tooltip.geometry(f"+{x}+{y}")

        # Auto-close after 1.5 seconds
        tooltip.after(1500, tooltip.destroy)

    def _create_window(self, title, geometry):
        """Create the main window."""
        if self.window:
            self.close()

        self.window = tk.Tk()
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.resizable(False, False)
        self.window.attributes("-topmost", True)

        # Theme
        if self._is_dark_theme():
            self.window.configure(bg="#1e1e1e")
        else:
            self.window.configure(bg="#f0f0f0")

        self.window.protocol("WM_DELETE_WINDOW", self.close)

    def _clear_window(self):
        """Clear all widgets from the window."""
        if self.window:
            for widget in self.window.winfo_children():
                widget.destroy()

    def _center_window(self):
        """Center the window on screen."""
        if not self.window:
            return
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f"+{x}+{y}")

    def _is_dark_theme(self):
        """Check if dark theme is enabled."""
        try:
            from src.config import load_config

            config = load_config()
            return config.get("theme", "dark") == "dark"
        except Exception:
            return True

    def close(self):
        """Close the popup."""
        if self.window:
            try:
                self.window.destroy()
            except tk.TclError:
                pass
            self.window = None
        if self.on_close:
            self.on_close()
