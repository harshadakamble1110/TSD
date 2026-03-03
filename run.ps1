# TECH Skills Development - Run script for PowerShell
Set-Location $PSScriptRoot

Write-Host "Installing dependencies if needed..." -ForegroundColor Cyan
pip install -q -r requirements.txt 2>$null
if (-not (Test-Path "instance")) { New-Item -ItemType Directory -Path "instance" | Out-Null }

Write-Host ""
Write-Host "Starting TECH Skills Development..." -ForegroundColor Green
Write-Host "Open in browser: http://127.0.0.1:5000" -ForegroundColor Yellow
Write-Host "Press CTRL+C to stop." -ForegroundColor Gray
Write-Host ""

python app.py
