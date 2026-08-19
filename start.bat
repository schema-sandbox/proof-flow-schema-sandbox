@echo off
chcp 65001 >nul
title ProofFlow Launcher
cd /d "%~dp0"

set "PYTHON_EXE=.venv\Scripts\python.exe"
if not exist "%PYTHON_EXE%" (
    set "PYTHON_EXE=python"
)

"%PYTHON_EXE%" start.py

if %errorlevel% neq 0 (
    pause
)
