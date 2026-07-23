<div align="center">

# 🧠 ClipMind

**Your AI assistant in the system tray**

Select text, press `Ctrl+C+M`, and get instant answers.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux-lightgrey)](https://github.com/giovanniromero-dev/clip-mind)
[![DeepSeek](https://img.shields.io/badge/API-DeepSeek%20%7C%20OpenAI%20%7C%20Ollama-orange)](https://deepseek.com)

</div>

---

## 📖 What is ClipMind?

ClipMind lives in your **system tray**. It's always there, in the background, waiting. You select text from **any application** (browser, editor, PDF, terminal...), press `Ctrl+C+M`, and an elegant window appears with 4 smart actions powered by **DeepSeek** (or the provider of your choice).

**No interruptions. No annoying windows. No lost context.**

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🌐 **Cross-platform** | Works on **Windows** and **Linux** without modification |
| ⚡ **Global hotkey** | `Ctrl+C+M` from any application, always available |
| 📝 **4 smart actions** | Summarize, Translate, Explain, Respond |
| 🔌 **Multiple providers** | DeepSeek (default), OpenAI, Ollama (local) |
| 🔄 **Auto-start** | Launches automatically when you turn on your PC |
| 🎨 **Dark interface** | Clean, modern design with dark theme |
| 📋 **Quick copy** | One click to copy the result to your clipboard |
| 🔒 **Privacy** | Your data goes directly to the API you choose. No intermediaries |
| 🪶 **Lightweight** | ~50 MB RAM, 0% CPU at rest |

---

## 🚀 Installation

### 🐧 Linux (one line)

```bash
curl -sSL https://raw.githubusercontent.com/giovanniromero-dev/clip-mind/main/install.sh | bash
```

The installer will:
- ✅ Detect Python 3.10+
- ✅ Install dependencies automatically
- ✅ Ask for your DeepSeek API key
- ✅ Create a systemd service for auto-start
- ✅ Launch ClipMind immediately

### 🪟 Windows (one line)

```powershell
irm https://raw.githubusercontent.com/giovanniromero-dev/clip-mind/main/install.ps1 | iex
```

The installer will:
- ✅ Download Python if you don't have it
- ✅ Install dependencies automatically
- ✅ Ask for your DeepSeek API key
- ✅ Add ClipMind to Windows startup
- ✅ Launch ClipMind immediately

---

## 🎯 Usage

### First launch

The first time you run ClipMind, it will walk you through setting up your API key:

```
🧠 ClipMind — First-time setup

Do you have a DeepSeek API key?
  [🌐 Get free API key]
  [🔑 I already have one]
  [💻 Use local model (Ollama)]
```

### Day-to-day

```
1. 📌 Select text in any app
        ↓
2. ⌨️  Press Ctrl+C+M
        ↓
3. 🪟 The ClipMind window appears
        ↓
4. 🎯 Choose an action:
        ┌─────────────────────────────┐
        │ 📝 Summarize  🌍 Translate  │
        │ ❓ Explain    💬 Respond    │
        └─────────────────────────────┘
        ↓
5. 🤖 The AI processes the text
        ↓
6. 📋 Copy the result with one click
```

### Available actions

| Action | Description | Use case |
|--------|-------------|----------|
| 📝 **Summarize** | Condense text to the essentials | Long articles, documents |
| 🌍 **Translate** | Translate to English | Foreign language texts |
| ❓ **Explain** | Explain the concept clearly | Code, technical terms |
| 💬 **Respond** | Generate a reply to the text | Emails, messages, questions |

---

## ⚙️ Configuration

### Configuration file

ClipMind stores its configuration in `~/.clipmind/config.json`:

```json
{
  "provider": "deepseek",
  "api_key": "sk-your-api-key",
  "model": "deepseek-chat",
  "base_url": "https://api.deepseek.com/v1",
  "language": "en",
  "hotkey": "ctrl+c+m",
  "auto_start": true,
  "theme": "dark",
  "auto_copy": false
}
```

### Switch AI providers

ClipMind is **provider-agnostic**. Change your AI by editing `config.json`:

| Provider | `provider` | `api_key` | `model` | `base_url` |
|----------|-----------|-----------|---------|------------|
| 🔵 **DeepSeek** | `deepseek` | Your API key | `deepseek-chat` | `https://api.deepseek.com/v1` |
| 🟢 **OpenAI** | `openai` | Your API key | `gpt-4o-mini` | `https://api.openai.com/v1` |
| 🟣 **Ollama (local)** | `ollama` | `""` | `deepseek-r1:7b` | `http://localhost:11434` |

> **Want to add another provider?** Just add a method in `src/llm_client.py`. It's that simple.

### Custom hotkey

Don't like `Ctrl+C+M`? Change it:

```json
{
  "hotkey": "ctrl+shift+h"
}
```

---

## 🏗️ Development

### Clone and run

```bash
# Clone
git clone https://github.com/giovanniromero-dev/clip-mind.git
cd clip-mind

# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Run in development mode
python main.py
```

### Platform-specific dependencies

```bash
# Windows (hotkeys with keyboard)
pip install keyboard

# Linux (hotkeys with pynput)
pip install pynput
```

### Project structure

```
clip-mind/
├── main.py                 # 🚀 Entry point
├── setup.py                # 📦 PyPI distribution
├── requirements.txt        # 📋 Dependencies
├── README.md               # 📖 Documentation
├── LICENSE                 # ⚖️ MIT
├── .gitignore
├── install.sh              # 🐧 Linux installer
├── install.ps1             # 🪟 Windows installer
└── src/
    ├── __init__.py
    ├── config.py           # ⚙️ Configuration management
    ├── clipboard.py        # 📋 Clipboard operations
    ├── llm_client.py       # 🤖 Multi-provider LLM client
    ├── popup.py            # 🪟 Action popup window
    ├── tray.py             # 🔲 System tray icon
    ├── hotkey.py           # ⌨️ Global hotkey (Ctrl+C+M)
    └── platform.py         # 🔄 Cross-platform abstraction
```

---

## 🧪 Verification

```bash
# Verify everything works
python -c "from src.config import load_config; from src.llm_client import LLMClient; from src.hotkey import HotkeyManager; from src.tray import TrayManager; from src.popup import ClipMindPopup; from src.clipboard import get_selected_text; print('✅ All modules loaded successfully')"
```

---

## ❓ FAQ

### Does ClipMind use a lot of resources?
No. At rest it uses ~0% CPU and ~50 MB RAM. It's lighter than a browser with one tab open.

### Does it work offline?
Only if you use Ollama with a local model. DeepSeek and OpenAI require an internet connection.

### Is my API key safe?
Your API key is stored in `~/.clipmind/config.json` on your machine. It is never sent to any server other than the provider you chose.

### Can I use ClipMind in my language?
Yes. Change `"language"` in the configuration. The default is English.

---

<div align="center">

**Made with 🧠 by ClipMind**

</div>
