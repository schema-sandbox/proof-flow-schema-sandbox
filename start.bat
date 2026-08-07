@echo off
title ProofFlow Startup
cd /d "%~dp0"
echo Starting ProofFlow Schema Sandbox...
python start.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo An error occurred starting ProofFlow.
    pause
)
