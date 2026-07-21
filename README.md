# 🧠 ClipMind

**Selecciona texto, presiona Ctrl+C+M y obtén respuestas de IA al instante.**

ClipMind vive en la bandeja del sistema. Siempre está ahí, esperando. Seleccionas texto en cualquier aplicación, presionas el atajo global, y aparece una ventana con acciones inteligentes usando DeepSeek (u otros proveedores).

## ✨ Características

- **🌐 Cross-platform** — Funciona en Windows y Linux
- **⚡ Atajo global** — `Ctrl+C+M` desde cualquier aplicación
- **📝 4 acciones** — Resumir, Traducir, Explicar, Responder
- **🔌 Múltiples proveedores** — DeepSeek, OpenAI, Ollama (local)
- **🔄 Inicio automático** — Arranca solo al encender el PC
- **🎨 Tema oscuro** — Interfaz limpia y moderna
- **📋 Copia rápida** — Un clic para copiar el resultado

## 🚀 Instalación

### Linux (una línea)

```bash
curl -sSL https://raw.githubusercontent.com/tuusuario/clipmind/main/install.sh | bash
```

### Windows (una línea)

```powershell
irm https://raw.githubusercontent.com/tuusuario/clipmind/main/install.ps1 | iex
```

### Con pip (próximamente)

```bash
pip install clipmind
clipmind
```

## 🎯 Uso

1. **Selecciona texto** en cualquier aplicación (navegador, editor, PDF, etc.)
2. **Presiona `Ctrl+C+M`** (el atajo global)
3. **Elige una acción** en la ventana emergente:

   | Acción | Descripción |
   |--------|-------------|
   | 📝 Resumir | Reduce el texto a lo esencial |
   | 🌍 Traducir | Traduce al español |
   | ❓ Explicar | Explica el concepto de forma clara |
   | 💬 Responder | Genera una respuesta al texto |

4. **Copia el resultado** con un clic

## ⚙️ Configuración

ClipMind se configura automáticamente la primera vez que lo ejecutas. También puedes hacer clic derecho en el icono de la bandeja → "Configuración".

### Archivo de configuración

`~/.clipmind/config.json`

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

### Cambiar de proveedor

| Proveedor | `provider` | `api_key` | `model` | `base_url` |
|-----------|-----------|-----------|---------|------------|
| DeepSeek | `deepseek` | Tu API key | `deepseek-chat` | `https://api.deepseek.com/v1` |
| OpenAI | `openai` | Tu API key | `gpt-4o-mini` | `https://api.openai.com/v1` |
| Ollama (local) | `ollama` | `""` | `deepseek-r1:7b` | `http://localhost:11434` |

## 🏗️ Desarrollo

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

# Ejecutar
python main.py
```

### Dependencias por plataforma

```bash
# Windows
pip install keyboard

# Linux
pip install pynput
```

## 📁 Estructura del proyecto

```
clipmind/
├── main.py              # Punto de entrada
├── src/
│   ├── __init__.py
│   ├── config.py        # Gestión de configuración
│   ├── clipboard.py     # Operaciones de portapapeles
│   ├── llm_client.py    # Cliente multi-proveedor (DeepSeek, OpenAI, Ollama)
│   ├── popup.py         # Ventana emergente con acciones
│   ├── tray.py          # Icono de bandeja del sistema
│   ├── hotkey.py        # Atajo global (Ctrl+C+M)
│   └── platform.py      # Abstracción cross-platform
├── install.sh           # Instalador Linux
├── install.ps1          # Instalador Windows
├── setup.py             # Para PyPI
├── requirements.txt
├── README.md
└── LICENSE
```

## 📄 Licencia

MIT

## 🙌 Contribuciones

¡Las contribuciones son bienvenidas! Abre un issue o envía un PR.
