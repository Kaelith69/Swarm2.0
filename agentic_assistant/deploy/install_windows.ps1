# ---------------------------------------------------------------------------
# install_windows.ps1 — Bootstrap the Agentic Assistant on Windows
#
# This script:
#   1. Verifies Python 3.10+ is available.
#   2. Creates a Python virtual environment at .venv\.
#   3. Installs all Python dependencies from requirements.txt.
#   4. Creates the RAG data directory.
#   5. Prints next-step instructions.
#
# Usage (from the agentic_assistant\ directory):
#   powershell -ExecutionPolicy Bypass -File deploy\install_windows.ps1
#
# Optional: build llama.cpp on Windows
#   The script prints instructions for building llama.cpp with CMake.
#   If you only use cloud routes (Groq/Gemini/Kimi) you can skip llama.cpp
#   and leave MODEL_PATH / LLAMA_MAIN_PATH unset or pointing to a dummy value.
# ---------------------------------------------------------------------------

$ErrorActionPreference = "Stop"

$AppDir = $PSScriptRoot | Split-Path -Parent
Set-Location $AppDir

Write-Host ""
Write-Host "==> Agentic Assistant — Windows Installer"
Write-Host "    Working directory: $AppDir"
Write-Host ""

# ---------------------------------------------------------------------------
# Step 1: Verify Python
# ---------------------------------------------------------------------------
Write-Host "==> [1/5] Checking Python version ..."
try {
    $pyVersion = python --version 2>&1
    Write-Host "    Found: $pyVersion"
} catch {
    Write-Error "Python not found. Install Python 3.10+ from https://python.org and add it to PATH."
    exit 1
}

# Extract major.minor
$verMatch = [regex]::Match($pyVersion, "Python (\d+)\.(\d+)")
if (-not $verMatch.Success) {
    Write-Error "Could not parse Python version: $pyVersion"
    exit 1
}
$major = [int]$verMatch.Groups[1].Value
$minor = [int]$verMatch.Groups[2].Value
if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 10)) {
    Write-Error "Python 3.10+ required. Found: $pyVersion"
    exit 1
}

# ---------------------------------------------------------------------------
# Step 2: Create virtual environment
# ---------------------------------------------------------------------------
Write-Host "==> [2/5] Creating virtual environment at .venv\ ..."
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "    Virtual environment created."
} else {
    Write-Host "    Virtual environment already exists — skipping."
}

# ---------------------------------------------------------------------------
# Step 3: Install dependencies
# ---------------------------------------------------------------------------
Write-Host "==> [3/5] Installing Python dependencies ..."
$pip = Join-Path $AppDir ".venv\Scripts\pip.exe"
& $pip install --upgrade pip --quiet
& $pip install -r requirements.txt

Write-Host "    Dependencies installed."

# ---------------------------------------------------------------------------
# Step 4: Create data directories
# ---------------------------------------------------------------------------
Write-Host "==> [4/5] Creating data directories ..."
$DataDirs = @(
    "data\rag",
    "data\knowledge"
)
foreach ($d in $DataDirs) {
    $full = Join-Path $AppDir $d
    if (-not (Test-Path $full)) {
        New-Item -ItemType Directory -Path $full -Force | Out-Null
        Write-Host "    Created: $full"
    }
}

# ---------------------------------------------------------------------------
# Step 5: Copy .env and personality templates if missing
# ---------------------------------------------------------------------------
Write-Host "==> [5/5] Checking configuration files ..."

$envFile = Join-Path $AppDir ".env"
$envExample = Join-Path $AppDir ".env.example"
if (-not (Test-Path $envFile)) {
    Copy-Item $envExample $envFile
    Write-Host "    Created .env from .env.example — edit it before running the server."
} else {
    Write-Host "    .env already exists — skipping."
}

$personalityFile = Join-Path $AppDir "personality.yaml"
$personalityExample = Join-Path $AppDir "personality.yaml.example"
if (-not (Test-Path $personalityFile) -and (Test-Path $personalityExample)) {
    Copy-Item $personalityExample $personalityFile
    Write-Host "    Created personality.yaml from personality.yaml.example."
}

# ---------------------------------------------------------------------------
# Summary and next steps
# ---------------------------------------------------------------------------
Write-Host ""
Write-Host "==> Installation complete!"
Write-Host ""
Write-Host "  Next steps:"
Write-Host ""
Write-Host "  1. Edit .env and set your values:"
Write-Host "       - MODEL_PATH     (path to your .gguf model, e.g. C:\llama.cpp\models\model.gguf)"
Write-Host "       - LLAMA_MAIN_PATH (path to llama-cli.exe)"
Write-Host "       - GROQ_API_KEY / GEMINI_API_KEY / KIMI_API_KEY (optional cloud keys)"
Write-Host "       - TELEGRAM_BOT_TOKEN / DISCORD_BOT_TOKEN"
Write-Host "       - BOT_MODE=polling  (recommended for Windows)"
Write-Host ""
Write-Host "  2. (Optional) Edit personality.yaml to give the assistant a name and character."
Write-Host ""
Write-Host "  3. (Optional) Build llama.cpp on Windows:"
Write-Host "       git clone https://github.com/ggerganov/llama.cpp C:\llama.cpp"
Write-Host "       cd C:\llama.cpp"
Write-Host "       cmake -S . -B build -DCMAKE_BUILD_TYPE=Release"
Write-Host "       cmake --build build --config Release -j4"
Write-Host "       # binary: C:\llama.cpp\build\bin\Release\llama-cli.exe"
Write-Host "     OR skip llama.cpp and use cloud-only routes (Groq/Gemini/Kimi)."
Write-Host ""
Write-Host "  4. Ingest knowledge documents (optional):"
Write-Host "       .\.venv\Scripts\python.exe scripts\ingest_documents.py data\knowledge --source knowledge_base"
Write-Host ""
Write-Host "  5. Start the server:"
Write-Host "       powershell -ExecutionPolicy Bypass -File scripts\start_windows.ps1"
Write-Host "     OR:"
Write-Host "       scripts\start_windows.bat"
Write-Host ""
