@echo off
:: ---------------------------------------------------------------------------
:: start_windows.bat — Start the Agentic Assistant on Windows
::
:: For users who prefer a plain .bat file over PowerShell.
:: Prerequisites:
::   - .env configured (copy .env.example to .env)
::   - Virtual environment at .venv\ (run deploy\install_windows.ps1 first)
::
:: Usage (from the agentic_assistant\ directory):
::   scripts\start_windows.bat
:: ---------------------------------------------------------------------------
setlocal

set "APP_DIR=%~dp0.."
set "VENV_PYTHON=%APP_DIR%\.venv\Scripts\python.exe"
set "LOG_FILE=%TEMP%\agentic-assistant.log"

cd /d "%APP_DIR%"

if not exist ".env" (
    echo [ERROR] .env not found. Copy .env.example to .env and fill your values.
    exit /b 1
)

if not exist "%VENV_PYTHON%" (
    echo [ERROR] Virtual environment not found at %APP_DIR%\.venv
    echo         Run:  powershell -ExecutionPolicy Bypass -File deploy\install_windows.ps1
    exit /b 1
)

set "PYTHONPATH=%APP_DIR%\src"

echo [INFO] Starting Agentic Assistant ...
echo [INFO] Logs: %LOG_FILE%

start "AgenticAssistant" /B "%VENV_PYTHON%" -m assistant.agent > "%LOG_FILE%" 2>&1

echo [INFO] Waiting for server startup (up to 30s) ...
set READY=0
for /L %%i in (1,1,30) do (
    timeout /t 1 /nobreak > nul
    curl -sf http://127.0.0.1:8000/health > nul 2>&1
    if not errorlevel 1 (
        set READY=1
        goto :ready
    )
)

:ready
if "%READY%"=="0" (
    echo [ERROR] Server did not start. Check log: %LOG_FILE%
    exit /b 1
)

echo [OK] Server is healthy.
curl http://127.0.0.1:8000/health
echo.
echo [INFO] Smoke test /query ...
curl -s -X POST http://127.0.0.1:8000/query -H "Content-Type: application/json" -d "{\"message\":\"Hello\"}"
echo.
echo [DONE] Server is running. Press Ctrl+C to stop.
pause
endlocal
