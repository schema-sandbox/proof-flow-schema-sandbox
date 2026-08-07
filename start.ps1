# ProofFlow PowerShell Launcher
$rootDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $rootDir
$env:PYTHONPATH = "$rootDir\apps\api"
python start.py
