# ClipMind Installer for Windows
# Usage: irm https://raw.githubusercontent.com/giovanniromero-dev/clip-mind/main/install.ps1 | iex

Write-Host "╔══════════════════════════════════════╗" -ForegroundColor Blue
Write-Host "║     🧠 ClipMind - Instalador Windows ║" -ForegroundColor Blue
Write-Host "╚══════════════════════════════════════╝" -ForegroundColor Blue
Write-Host ""

# Check if Python is installed
$pythonInstalled = $false
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.(\d+)") {
        $pythonInstalled = $true
        Write-Host "✓ Python detectado: $pythonVersion" -ForegroundColor Green
    }
} catch {
    $pythonInstalled = $false
}

if (-not $pythonInstalled) {
    Write-Host "📥 Descargando Python 3.13..." -ForegroundColor Yellow
    $pythonUrl = "https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe"
    $pythonInstaller = "$env:TEMP\python-installer.exe"

    try {
        Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller -UseBasicParsing
    } catch {
        Write-Host "❌ No se pudo descargar Python. Descárgalo manualmente de python.org" -ForegroundColor Red
        exit 1
    }

    Write-Host "🔧 Instalando Python..." -ForegroundColor Blue
    Start-Process -Wait -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=0", "PrependPath=1", "Include_test=0"
    Remove-Item $pythonInstaller -Force

    # Refresh PATH
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

    Write-Host "✓ Python instalado" -ForegroundColor Green
}

# Repository settings
$repoOwner = "giovanniromero-dev"
$repoName = "clip-mind"
$zipUrl = "https://github.com/$repoOwner/$repoName/archive/main.zip"

# Install directory
$installDir = "$env:LOCALAPPDATA\ClipMind"

if (Test-Path $installDir) {
    Write-Host "📂 ClipMind ya está instalado. Actualizando..." -ForegroundColor Yellow
    # Remove old files but keep virtual environment
    Get-ChildItem -Path $installDir -Exclude "venv" | Remove-Item -Recurse -Force
} else {
    Write-Host "📥 Instalando ClipMind..." -ForegroundColor Blue
    New-Item -ItemType Directory -Force -Path $installDir | Out-Null
}

# Download and extract ZIP (works with or without Git)
Write-Host "📥 Descargando ClipMind..." -ForegroundColor Blue
$zipFile = "$env:TEMP\clipmind.zip"
$extractDir = "$env:TEMP\${repoName}-main"

try {
    Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing
    if (Test-Path $extractDir) {
        Remove-Item $extractDir -Recurse -Force
    }
    Expand-Archive -Path $zipFile -DestinationPath $env:TEMP -Force
    Copy-Item -Path "$extractDir\*" -Destination $installDir -Recurse -Force
    Remove-Item $zipFile -Force
    Remove-Item $extractDir -Recurse -Force
} catch {
    Write-Host "❌ Error al descargar ClipMind. Verifica tu conexión." -ForegroundColor Red
    exit 1
}

Set-Location $installDir

# Verify essential files exist
if (-not (Test-Path "$installDir\requirements.txt")) {
    Write-Host "❌ Error: No se encontraron los archivos del proyecto." -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "🔧 Creando entorno virtual..." -ForegroundColor Blue
python -m venv venv

# Install dependencies
Write-Host "📦 Instalando dependencias..." -ForegroundColor Blue
& "$installDir\venv\Scripts\pip.exe" install --upgrade pip
& "$installDir\venv\Scripts\pip.exe" install -r requirements.txt
& "$installDir\venv\Scripts\pip.exe" install keyboard  # Windows hotkey library

# Create launcher script
$launcherPath = "$installDir\clipmind.bat"
@"
@echo off
cd /d "$installDir"
call venv\Scripts\activate
python main.py %*
"@ | Out-File -FilePath $launcherPath -Encoding ASCII

# Add to PATH
$userPath = [Environment]::GetEnvironmentVariable("Path", "User")
if ($userPath -notlike "*$installDir*") {
    [Environment]::SetEnvironmentVariable("Path", "$userPath;$installDir", "User")
    $env:Path = [Environment]::GetEnvironmentVariable("Path", "User")
}

# Add to startup (Registry)
Write-Host "🔄 Configurando inicio automático..." -ForegroundColor Blue
$startupPath = "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\ClipMind.bat"
@"
@echo off
start /b "" "$installDir\venv\Scripts\pythonw.exe" "$installDir\main.py"
"@ | Out-File -FilePath $startupPath -Encoding ASCII

# Ask for API key
Write-Host ""
Write-Host "🔑 Configuración inicial" -ForegroundColor Yellow
$hasKey = Read-Host "¿Tienes API key de DeepSeek? (s/N)"
if ($hasKey -eq "s" -or $hasKey -eq "S") {
    $apiKey = Read-Host "Pega tu API key"

    $configDir = "$env:USERPROFILE\.clipmind"
    New-Item -ItemType Directory -Force -Path $configDir | Out-Null

    $config = @{
        provider = "deepseek"
        api_key = $apiKey
        model = "deepseek-chat"
        base_url = "https://api.deepseek.com/v1"
        language = "es"
        hotkey = "ctrl+c+m"
        auto_start = $true
        theme = "dark"
        auto_copy = $false
    }

    $config | ConvertTo-Json | Out-File -FilePath "$configDir\config.json" -Encoding UTF8
    Write-Host "✓ API key guardada" -ForegroundColor Green
} else {
    Write-Host "ℹ️  Puedes configurarlo después ejecutando: clipmind" -ForegroundColor Yellow
}

# Verify installation
Write-Host ""
Write-Host "🔍 Verificando instalación..." -ForegroundColor Blue
try {
    & "$installDir\venv\Scripts\python.exe" -c "import pyperclip, requests, pystray, PIL; print('✓ Dependencias OK')" 2>&1 | Out-Null
    Write-Host "✓ Dependencias verificadas" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Algunas dependencias no se pudieron verificar" -ForegroundColor Yellow
}

# Start ClipMind
Write-Host ""
Write-Host "╔══════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║  🧠 ClipMind instalado con éxito     ║" -ForegroundColor Green
Write-Host "║                                      ║" -ForegroundColor Green
Write-Host "║  Presiona Ctrl+C+M en cualquier      ║" -ForegroundColor Green
Write-Host "║  texto para usar ClipMind            ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "🚀 Iniciando ClipMind..." -ForegroundColor Blue
Start-Process -WindowStyle Hidden -FilePath "$installDir\venv\Scripts\pythonw.exe" -ArgumentList "$installDir\main.py"
Write-Host "✓ ClipMind ejecutándose en segundo plano" -ForegroundColor Green