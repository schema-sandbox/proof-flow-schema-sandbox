@echo off
setlocal
cd /d "%~dp0"

echo ===================================================
echo   ProofFlow Launcher
echo ===================================================
echo.

if exist "%~dp0.venv\Scripts\python.exe" (
    set "PY_BIN=%~dp0.venv\Scripts\python.exe"
    goto RUN
)

if exist ".venv\Scripts\python.exe" (
    set "PY_BIN=.venv\Scripts\python.exe"
    goto RUN
)

where python >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_BIN=python"
    goto RUN
)

where py >nul 2>nul
if %errorlevel% equ 0 (
    set "PY_BIN=py"
    goto RUN
)

echo [ERROR] Python not found. Please install Python or setup .venv.
pause
exit /b 1

:RUN
echo [INFO] Using: %PY_BIN%
echo [INFO] Starting ProofFlow server...
echo.

"%PY_BIN%" "%~dp0start.py"

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Server exited with code %errorlevel%.
    pause
)
