#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Start all AgriCure backend servers (Node.js + Python FastAPI)
.DESCRIPTION
    This script starts both:
    1. Node.js Express server (port 3000) - for user auth, farms, etc.
    2. Python FastAPI server (port 8000) - for ML models (soil prediction, fertilizer)
.EXAMPLE
    .\start-all-servers.ps1
#>

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  🌾 AgriCure Backend - Starting All Servers" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$BackendDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check if virtual environment exists
$VenvPath = Join-Path $BackendDir ".venv"
if (-not (Test-Path $VenvPath)) {
    Write-Host "❌ Virtual environment not found at: $VenvPath" -ForegroundColor Red
    Write-Host "Please create it first:" -ForegroundColor Yellow
    Write-Host "  python -m venv .venv" -ForegroundColor Yellow
    Write-Host "  .\.venv\Scripts\Activate.ps1" -ForegroundColor Yellow
    Write-Host "  pip install -r requirements.txt" -ForegroundColor Yellow
    exit 1
}

# Check if node_modules exists
$NodeModulesPath = Join-Path $BackendDir "node_modules"
if (-not (Test-Path $NodeModulesPath)) {
    Write-Host "❌ node_modules not found" -ForegroundColor Red
    Write-Host "Please install dependencies first:" -ForegroundColor Yellow
    Write-Host "  npm install" -ForegroundColor Yellow
    exit 1
}

Write-Host "📋 Pre-flight checks passed" -ForegroundColor Green
Write-Host ""

# Function to check if a port is in use
function Test-Port {
    param([int]$Port)
    $Connection = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
    return $null -ne $Connection
}

# Check ports
Write-Host "🔍 Checking ports..." -ForegroundColor Cyan

$Port3000InUse = Test-Port -Port 3000
$Port8000InUse = Test-Port -Port 8000

if ($Port3000InUse) {
    Write-Host "⚠️  Port 3000 is already in use (Node.js)" -ForegroundColor Yellow
    Write-Host "   The Node.js server might already be running" -ForegroundColor Yellow
}

if ($Port8000InUse) {
    Write-Host "⚠️  Port 8000 is already in use (Python)" -ForegroundColor Yellow
    Write-Host "   The Python server might already be running" -ForegroundColor Yellow
}

if ($Port3000InUse -and $Port8000InUse) {
    Write-Host ""
    Write-Host "✅ Both servers appear to be running already!" -ForegroundColor Green
    Write-Host "   Node.js: http://localhost:3000" -ForegroundColor Cyan
    Write-Host "   Python:  http://localhost:8000" -ForegroundColor Cyan
    Write-Host ""
    $Continue = Read-Host "Do you want to continue anyway? (y/N)"
    if ($Continue -ne 'y' -and $Continue -ne 'Y') {
        Write-Host "Exiting..." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host ""
Write-Host "🚀 Starting servers..." -ForegroundColor Cyan
Write-Host ""

# Start Node.js server in a new window
Write-Host "1️⃣  Starting Node.js Express Server (Port 3000)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$BackendDir'; npm start" -WindowStyle Normal

# Wait a bit for Node.js to start
Start-Sleep -Seconds 2

# Start Python FastAPI server in a new window
Write-Host "2️⃣  Starting Python FastAPI Server (Port 8000)..." -ForegroundColor Green
$ActivateScript = Join-Path $VenvPath "Scripts\Activate.ps1"
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$BackendDir'; & '$ActivateScript'; python run_server.py" -WindowStyle Normal

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "  ✅ Servers Starting!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📡 Server URLs:" -ForegroundColor Yellow
Write-Host "   Node.js API:  http://localhost:3000/api" -ForegroundColor Cyan
Write-Host "   Python API:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "   API Docs:     http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "🔧 Server Windows:" -ForegroundColor Yellow
Write-Host "   Two new PowerShell windows should have opened" -ForegroundColor White
Write-Host "   Keep them open while using the application" -ForegroundColor White
Write-Host "   Close them when you're done to stop the servers" -ForegroundColor White
Write-Host ""
Write-Host "📝 Testing the servers:" -ForegroundColor Yellow
Write-Host "   Node.js: http://localhost:3000/api/health" -ForegroundColor White
Write-Host "   Python:  http://localhost:8000/health" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
