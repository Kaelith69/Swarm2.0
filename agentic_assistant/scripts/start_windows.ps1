# ---------------------------------------------------------------------------
# start_windows.ps1 — Start the Agentic Assistant on Windows
#
# Prerequisites:
#   - Python 3.10+ installed and on PATH
#   - .env file configured (copy .env.example to .env and edit)
#   - Virtual environment created (run deploy\install_windows.ps1 first)
#
# Usage:
#   From the project root (agentic_assistant\):
#     .\scripts\start_windows.ps1
#
# Optional environment overrides:
#   $env:PORT = "8001"; .\scripts\start_windows.ps1
# ---------------------------------------------------------------------------

param(
    [string]$AppDir   = $PSScriptRoot | Split-Path -Parent,
    [string]$Host     = $env:HOST ?? "127.0.0.1",
    [int]   $Port     = if ($env:PORT) { [int]$env:PORT } else { 8000 }
)

Set-Location $AppDir

# Check .env exists
if (-not (Test-Path ".env")) {
    Write-Error "[ERROR] .env not found at $AppDir\.env — copy .env.example to .env and fill values."
    exit 1
}

# Resolve venv python
$VenvPython = Join-Path $AppDir ".venv\Scripts\python.exe"
if (-not (Test-Path $VenvPython)) {
    Write-Error "[ERROR] Virtual environment not found at $AppDir\.venv — run deploy\install_windows.ps1 first."
    exit 1
}

# Set PYTHONPATH so the src/ package is importable
$env:PYTHONPATH = Join-Path $AppDir "src"

Write-Host "[INFO] Starting Agentic Assistant on ${Host}:${Port} ..."
Write-Host "[INFO] Logs → $env:TEMP\agentic-assistant.log"

# Start server in background
$logFile = Join-Path $env:TEMP "agentic-assistant.log"
$proc = Start-Process -FilePath $VenvPython `
    -ArgumentList "-m", "assistant.agent" `
    -RedirectStandardOutput $logFile `
    -RedirectStandardError  "$logFile.err" `
    -PassThru -NoNewWindow

Write-Host "[INFO] Server PID: $($proc.Id)"

# Wait for /health to respond
$ready = $false
for ($i = 1; $i -le 30; $i++) {
    Start-Sleep -Seconds 1
    try {
        $resp = Invoke-WebRequest -Uri "http://${Host}:${Port}/health" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
        if ($resp.StatusCode -eq 200) { $ready = $true; break }
    } catch { }
}

if (-not $ready) {
    Write-Error "[ERROR] Server did not become healthy. Last log lines:"
    Get-Content $logFile -Tail 40 -ErrorAction SilentlyContinue
    Stop-Process -Id $proc.Id -Force -ErrorAction SilentlyContinue
    exit 1
}

Write-Host "[OK] /health responded"
Invoke-RestMethod "http://${Host}:${Port}/health" | ConvertTo-Json -Depth 3

# Quick smoke test
Write-Host ""
Write-Host "[INFO] Running /query smoke test ..."
try {
    $result = Invoke-RestMethod -Method POST `
        -Uri "http://${Host}:${Port}/query" `
        -ContentType "application/json" `
        -Body '{"message":"Hello, who are you?"}' `
        -TimeoutSec 180
    Write-Host "[OK] /query smoke test passed"
    $result | ConvertTo-Json -Depth 3
} catch {
    Write-Warning "[WARN] /query smoke test failed: $_"
}

Write-Host ""
Write-Host "[DONE] Server is running (PID $($proc.Id))."
Write-Host "       Press Ctrl+C to stop, or run: Stop-Process -Id $($proc.Id)"
