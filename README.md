<div align="center">

# 🧠 ClipMind

**Tu asistente de IA en la bandeja del sistema**

Selecciona texto, presiona `Ctrl+C+M` y obtén respuestas al instante.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)](https://github.com/tuusuario/clipmind)
[![DeepSeek](https://img.shields.io/badge/API-DeepSeek%20%7C%20OpenAI%20%7C%20Ollama-orange)](https://deepseek.com)

</div>

---

## 📖 ¿Qué es ClipMind?

ClipMind vive en la **bandeja del sistema** de tu PC. Siempre está ahí, en segundo plano, esperando. Seleccionas texto en **cualquier aplicación** (navegador, editor, PDF, terminal...), presionas `Ctrl+C+M`, y aparece una ventana elegante con 4 acciones inteligentes potenciadas por **DeepSeek** (o el proveedor que elijas).

**Sin interrupciones. Sin ventanas molestas. Sin perder el contexto.**

---

## ✨ Características

| Característica | Descripción |
|---------------|-------------|
| 🌐 **Cross-platform** | Funciona en **Windows** y **Linux** sin modificar nada |
| ⚡ **Atajo global** | `Ctrl+C+M` desde cualquier aplicación, siempre disponible |
| 📝 **4 acciones inteligentes** | Resumir, Traducir, Explicar, Responder |
| 🔌 **Múltiples proveedores** | DeepSeek (por defecto), OpenAI, Ollama (local) |
| 🔄 **Inicio automático** | Arranca solo al encender el PC — ni te enteras |
| 🎨 **Interfaz oscura** | Diseño moderno y limpio con tema oscuro |
| 📋 **Copia rápida** | Un clic para copiar el resultado al portapapeles |
| 🔒 **Privacidad** | Tus datos van directo a la API que elijas. Sin intermediarios |
| 🪶 **Ligero** | ~50 MB de RAM, 0% CPU en reposo |

---

## 🚀 Instalación

### 🐧 Linux (una línea)

```bash
curl -sSL https://raw.githubusercontent.com/tuusuario/clipmind/main/install.sh | bash
```

El instalador:
- ✅ Detecta Python 3.10+
- ✅ Instala dependencias automáticamente
- ✅ Te pide la API key de DeepSeek
- ✅ Crea un servicio systemd para inicio automático
- ✅ Inicia ClipMind al instante

### 🪟 Windows (una línea)

```powershell
irm https://raw.githubusercontent.com/tuusuario/clipmind/main/install.ps1 | iex
```

El instalador:
- ✅ Descarga Python si no lo tienes
- ✅ Instala dependencias automáticamente
- ✅ Te pide la API key de DeepSeek
- ✅ Añade ClipMind al inicio de Windows
- ✅ Inicia ClipMind al instante

---

## 🎯 Uso

### Primer inicio

La primera vez que ejecutas ClipMind, te guiará para configurar tu API key:

```
🧠 ClipMind — Primera configuración

¿Tienes una API key de DeepSeek?
  [🌐 Obtener API key gratis]
  [🔑 Ya tengo una]
  [💻 Usar modelo local (Ollama)]
```

### Día a día

```
1. 📌 Seleccionas texto en cualquier app
        ↓
2. ⌨️  Presionas Ctrl+C+M
        ↓
3. 🪟 Aparece la ventana ClipMind
        ↓
4. 🎯 Eliges una acción:
        ┌─────────────────────────────┐
        │ 📝 Resumir  🌍 Traducir    │
        │ ❓ Explicar  💬 Responder   │
        └─────────────────────────────┘
        ↓
5. 🤖 La IA procesa el texto
        ↓
6. 📋 Copias el resultado con un clic
```

### Acciones disponibles

| Acción | Descripción | Ejemplo de uso |
|--------|-------------|----------------|
| 📝 **Resumir** | Reduce el texto a lo esencial | Artículos largos, documentos |
| 🌍 **Traducir** | Traduce al español | Textos en inglés, otros idiomas |
| ❓ **Explicar** | Explica el concepto de forma clara | Código, términos técnicos |
| 💬 **Responder** | Genera una respuesta al texto | Correos, mensajes, preguntas |

---

## ⚙️ Configuración

### Archivo de configuración

ClipMind guarda su configuración en `~/.clipmind/config.json`:

```json
{
  "provider": "deepseek",
  "api_key": "sk-tu-api-key",
  "model": "deepseek-chat",
  "base_url": "https://api.deepseek.com/v1",
  "language": "es",
  "hotkey": "ctrl+c+m",
  "auto_start": true,
  "theme": "dark",
  "auto_copy": false
}
```

### Cambiar de proveedor de IA

ClipMind es **agnóstico al proveedor**. Cambia de IA editando el `config.json`:

| Proveedor | `provider` | `api_key` | `model` | `base_url` |
|-----------|-----------|-----------|---------|------------|
| 🔵 **DeepSeek** | `deepseek` | Tu API key | `deepseek-chat` | `https://api.deepseek.com/v1` |
| 🟢 **OpenAI** | `openai` | Tu API key | `gpt-4o-mini` | `https://api.openai.com/v1` |
| 🟣 **Ollama (local)** | `ollama` | `""` | `deepseek-r1:7b` | `http://localhost:11434` |

> **¿Quieres añadir otro proveedor?** Solo añade un método en `src/llm_client.py`. Así de simple.

### Atajo personalizado

¿No te gusta `Ctrl+C+M`? Cámbialo:

```json
{
  "hotkey": "ctrl+shift+h"
}
```

---

## 🏗️ Desarrollo

### Clonar y ejecutar

```bash
# Clonar
git clone https://github.com/tuusuario/clipmind.git
cd clipmind

# Entorno virtual
python -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar en modo desarrollo
python main.py
```

### Dependencias por plataforma

```bash
# Windows (hotkeys con keyboard)
pip install keyboard

# Linux (hotkeys con pynput)
pip install pynput
```

### Estructura del proyecto

```
clipmind/
├── main.py                 # 🚀 Punto de entrada
├── setup.py                # 📦 Para publicación en PyPI
├── requirements.txt        # 📋 Dependencias
├── README.md               # 📖 Documentación
├── LICENSE                 # ⚖️ MIT
├── .gitignore
├── install.sh              # 🐧 Instalador Linux
├── install.ps1             # 🪟 Instalador Windows
└── src/
    ├── __init__.py
    ├── config.py           # ⚙️ Gestión de configuración
    ├── clipboard.py        # 📋 Operaciones de portapapeles
    ├── llm_client.py       # 🤖 Cliente multi-proveedor
    ├── popup.py            # 🪟 Ventana emergente con acciones
    ├── tray.py             # 🔲 Icono de bandeja del sistema
    ├── hotkey.py           # ⌨️ Atajo global (Ctrl+C+M)
    └── platform.py         # 🔄 Abstracción cross-platform
```

---

## 🧪 Verificación

```bash
# Verificar que todo funciona
python -c "from src.config import load_config; from src.llm_client import LLMClient; from src.hotkey import HotkeyManager; from src.tray import TrayManager; from src.popup import ClipMindPopup; from src.clipboard import get_selected_text; print('✅ Todos los módulos cargados correctamente')"
```

---

## ❓ FAQ

### ¿ClipMind consume muchos recursos?
No. En reposo usa ~0% de CPU y ~50 MB de RAM. Es más ligero que un navegador con una pestaña abierta.

### ¿Funciona sin internet?
Solo si usas Ollama con un modelo local. DeepSeek y OpenAI requieren conexión.

### ¿Es seguro mi API key?
Tu API key se guarda en `~/.clipmind/config.json` en tu máquina. Nunca se envía a ningún servidor que no sea el proveedor que elegiste.

### ¿Puedo usar ClipMind en mi idioma?
Sí. Cambia `"language"` en la configuración. Por defecto viene en español.

### ¿Cómo desinstalo ClipMind?

**Linux:**
```bash
curl -sSL https://raw.githubusercontent.com/tuusuario/clipmind/main/uninstall.sh | bash
```

**Windows:**
```powershell
irm https://raw.githubusercontent.com/tuusuario/clipmind/main/uninstall.ps1 | iex
```

---

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Así puedes ayudar:

1. 🐛 **Reporta bugs** — Abre un [issue](https://github.com/tuusuario/clipmind/issues)
2. 💡 **Sugiere ideas** — Nuevas acciones, proveedores, mejoras
3. 🔧 **Envía PRs** — Código, documentación, instaladores
4. 🌍 **Traducciones** — Ayuda a llevar ClipMind a más idiomas

---

## 📄 Licencia

**MIT** — Haz lo que quieras con este código. Úsalo, modifícalo, compártelo.

---

<div align="center">

**Hecho con ❤️ para la comunidad open-source**

[Reportar bug](https://github.com/tuusuario/clipmind/issues) · [Sugerir mejora](https://github.com/tuusuario/clipmind/issues) · [Contribuir](https://github.com/tuusuario/clipmind/pulls)

</div>
