#!/bin/bash
# ClipMind Installer for Linux
# Usage: curl -sSL https://raw.githubusercontent.com/giovanniromero-dev/clip-mind/main/install.sh | bash

set -e

GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     🧠 ClipMind - Instalador Linux   ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════╝${NC}"
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo -e "${RED}❌ Python no encontrado. Instálalo con: sudo apt install python3 python3-pip${NC}"
    exit 1
fi

PYTHON_VERSION=$($PYTHON --version 2>&1 | grep -oP '\d+\.\d+')
echo -e "${GREEN}✓ Python $PYTHON_VERSION detectado${NC}"

# Check pip
if ! command -v pip3 &> /dev/null && ! $PYTHON -m pip --version &> /dev/null; then
    echo -e "${YELLOW}📦 Instalando pip...${NC}"
    sudo apt install -y python3-pip || sudo dnf install -y python3-pip || sudo pacman -S --noconfirm python-pip
fi

# Install git if needed
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}📦 Instalando git...${NC}"
    sudo apt install -y git || sudo dnf install -y git || sudo pacman -S --noconfirm git
fi

# Repository settings
REPO_OWNER="giovanniromero-dev"
REPO_NAME="clip-mind"
ZIP_URL="https://github.com/$REPO_OWNER/$REPO_NAME/archive/main.zip"

# Install directory
INSTALL_DIR="$HOME/.local/share/clipmind"

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}📂 ClipMind ya está instalado. Actualizando...${NC}"
    # Remove old files but keep virtual environment
    find "$INSTALL_DIR" -mindepth 1 -not -name "venv" -exec rm -rf {} + 2>/dev/null || true
else
    echo -e "${BLUE}📥 Instalando ClipMind...${NC}"
    mkdir -p "$HOME/.local/share"
fi

# Download and extract ZIP (works with or without Git)
echo -e "${BLUE}📥 Descargando ClipMind...${NC}"
ZIP_FILE="/tmp/clipmind.zip"
EXTRACT_DIR="/tmp/${REPO_NAME}-main"

rm -f "$ZIP_FILE" 2>/dev/null || true
rm -rf "$EXTRACT_DIR" 2>/dev/null || true

curl -sSL "$ZIP_URL" -o "$ZIP_FILE"
unzip -o "$ZIP_FILE" -d "/tmp" > /dev/null 2>&1
cp -r "$EXTRACT_DIR/"* "$INSTALL_DIR/"
rm -f "$ZIP_FILE"
rm -rf "$EXTRACT_DIR"

cd "$INSTALL_DIR"

# Verify essential files exist
if [ ! -f "$INSTALL_DIR/requirements.txt" ]; then
    echo -e "${RED}❌ Error: No se encontraron los archivos del proyecto.${NC}"
    exit 1
fi

# Create virtual environment
echo -e "${BLUE}🔧 Creando entorno virtual...${NC}"
$PYTHON -m venv venv
source venv/bin/activate

# Install dependencies
echo -e "${BLUE}📦 Instalando dependencias...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
pip install pynput  # Linux hotkey library

# Create launcher script
echo -e "${BLUE}🔗 Creando acceso directo...${NC}"
mkdir -p "$HOME/.local/bin"
cat > "$HOME/.local/bin/clipmind" << 'EOF'
#!/bin/bash
cd "$HOME/.local/share/clipmind"
source venv/bin/activate
python main.py "$@"
EOF
chmod +x "$HOME/.local/bin/clipmind"

# Add to PATH if not already
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.zshrc" 2>/dev/null || true
    echo -e "${YELLOW}⚠️  Añadido ~/.local/bin al PATH. Reinicia tu terminal o ejecuta: source ~/.bashrc${NC}"
fi

# Create autostart
echo -e "${BLUE}🔄 Configurando inicio automático...${NC}"
mkdir -p "$HOME/.config/autostart"
cat > "$HOME/.config/autostart/clipmind.desktop" << EOF
[Desktop Entry]
Type=Application
Name=ClipMind
Comment=AI Clipboard Assistant
Exec=$HOME/.local/bin/clipmind
Terminal=false
Categories=Utility;
X-GNOME-Autostart-enabled=true
EOF
chmod +x "$HOME/.config/autostart/clipmind.desktop"

# Ask for API key
echo ""
echo -e "${YELLOW}🔑 Configuración inicial${NC}"
read -p "¿Tienes API key de DeepSeek? (s/N): " HAS_KEY
if [[ "$HAS_KEY" == "s" || "$HAS_KEY" == "S" ]]; then
    read -p "Pega tu API key: " API_KEY
    mkdir -p "$HOME/.clipmind"
    cat > "$HOME/.clipmind/config.json" << EOF
{
  "provider": "deepseek",
  "api_key": "$API_KEY",
  "model": "deepseek-chat",
  "base_url": "https://api.deepseek.com/v1",
  "language": "es",
  "hotkey": "ctrl+c+m",
  "auto_start": true,
  "theme": "dark",
  "auto_copy": false
}
EOF
    echo -e "${GREEN}✓ API key guardada${NC}"
else
    echo -e "${YELLOW}ℹ️  Puedes configurarlo después ejecutando: clipmind${NC}"
fi

# Start ClipMind
echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  🧠 ClipMind instalado con éxito     ║${NC}"
echo -e "${GREEN}║                                      ║${NC}"
echo -e "${GREEN}║  Presiona Ctrl+C+M en cualquier      ║${NC}"
echo -e "${GREEN}║  texto para usar ClipMind            ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""

# Start ClipMind in background
echo -e "${BLUE}🚀 Iniciando ClipMind...${NC}"
nohup "$HOME/.local/bin/clipmind" > /dev/null 2>&1 &
echo -e "${GREEN}✓ ClipMind ejecutándose en segundo plano${NC}"
