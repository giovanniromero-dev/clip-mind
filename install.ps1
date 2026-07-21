# ClipMind Installer for Windows
# Usage: irm https://raw.githubusercontent.com/tuusuario/clipmind/main/install.ps1 | iex

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

# Install git if needed
$gitInstalled = $false
try {
    git --version 2>&1 | Out-Null
    $gitInstalled = $true
} catch {
    $gitInstalled = $false
}

if (-not $gitInstalled) {
    Write-Host "📥 Descargando Git..." -ForegroundColor Yellow
    $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
    $gitInstaller = "$env:TEMP\git-installer.exe"
    
    try {
        Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller -UseBasicParsing
    } catch {
        Write-Host "⚠️  No se pudo descargar Git. Se usará descarga directa." -ForegroundColor Yellow
        $gitInstalled = $false
    }
    
    if ($gitInstalled -eq $false) {
        Start-Process -Wait -FilePath $gitInstaller -ArgumentList "/SILENT"
        Remove-Item $gitInstaller -Force
        Write-Host "✓ Git instalado" -ForegroundColor Green
    }
}

# Install directory
$installDir = "$env:LOCALAPPDATA\ClipMind"

if (Test-Path $installDir) {
    Write-Host "📂 ClipMind ya está instalado. Actualizando..." -ForegroundColor Yellow
    Set-Location $installDir
    git pull
} else {
    Write-Host "📥 Descargando ClipMind..." -ForegroundColor Blue
    New-Item -ItemType Directory -Force -Path $installDir | Out-Null
    
    # Download ZIP instead of requiring git
    $zipUrl = "https://github.com/tuusuario/clipmind/archive/main.zip"
    $zipFile = "$env:TEMP\clipmind.zip"
    
    try {
        Invoke-WebRequest -Uri $zipUrl -OutFile $zipFile -UseBasicParsing
        Expand-Archive -Path $zipFile -DestinationPath $env:TEMP -Force
        Copy-Item -Path "$env:TEMP\clipmind-main\*" -Destination $installDir -Recurse -Force
        Remove-Item $zipFile -Force
        Remove-Item "$env:TEMP\clipmind-main" -Recurse -Force
    } catch {
        Write-Host "❌ Error al descargar ClipMind. Verifica tu conexión." -ForegroundColor Red
        exit 1
    }
}

Set-Location $installDir

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
