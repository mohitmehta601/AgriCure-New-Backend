# AgriCure Integrated Servers Startup Script
# Starts Python FastAPI (port 8000) and Node.js Express (port 3000) servers

Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🌾 AgriCure - Starting Integrated Servers" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# Check if Python is available
Write-Host "🔍 Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✓ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if Node.js is available
Write-Host "🔍 Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    Write-Host "   ✓ Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "   ✗ Node.js not found. Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

# Check if npm packages are installed
Write-Host "🔍 Checking Node.js dependencies..." -ForegroundColor Yellow
if (-Not (Test-Path "node_modules")) {
    Write-Host "   ⚠️  node_modules not found. Installing..." -ForegroundColor Yellow
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ✗ Failed to install Node.js dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "   ✓ Node.js dependencies installed" -ForegroundColor Green
} else {
    Write-Host "   ✓ Node.js dependencies found" -ForegroundColor Green
}

# Check if Python packages are installed
Write-Host "🔍 Checking Python dependencies..." -ForegroundColor Yellow
$pipList = pip list 2>&1
if ($pipList -match "fastapi" -and $pipList -match "uvicorn") {
    Write-Host "   ✓ Python dependencies found" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Installing Python dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "   ✗ Failed to install Python dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "   ✓ Python dependencies installed" -ForegroundColor Green
}

# Check if dataset exists
Write-Host "🔍 Checking ML model data..." -ForegroundColor Yellow
$datasetPath = "fertilizer recommendation system\Primary and pH Dataset.csv"
if (Test-Path $datasetPath) {
    Write-Host "   ✓ Dataset found" -ForegroundColor Green
} else {
    Write-Host "   ✗ Dataset not found: $datasetPath" -ForegroundColor Red
    Write-Host "   Please ensure the dataset is in the correct location" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "🚀 Starting Servers..." -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Function to start Python server
$pythonJob = Start-Job -ScriptBlock {
    param($dir)
    Set-Location $dir
    python run_server.py
} -ArgumentList $scriptDir

# Wait a moment for Python server to start
Start-Sleep -Seconds 3

# Function to start Node.js server
$nodeJob = Start-Job -ScriptBlock {
    param($dir)
    Set-Location $dir
    node src/server.js
} -ArgumentList $scriptDir

# Wait a moment for Node.js server to start
Start-Sleep -Seconds 2

Write-Host "✓ Python FastAPI Server starting... (Job ID: $($pythonJob.Id))" -ForegroundColor Green
Write-Host "✓ Node.js Express Server starting... (Job ID: $($nodeJob.Id))" -ForegroundColor Green
Write-Host ""

# Check if servers are responding
Write-Host "🔍 Checking server health..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Check Python API
try {
    $pythonHealth = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 5
    Write-Host "   ✓ Python API: " -NoNewline -ForegroundColor Green
    Write-Host "http://localhost:8000" -ForegroundColor Cyan
    Write-Host "      Status: $($pythonHealth.status)" -ForegroundColor White
    Write-Host "      Model: $($pythonHealth.model_loaded)" -ForegroundColor White
} catch {
    Write-Host "   ⚠️  Python API not responding yet..." -ForegroundColor Yellow
    Write-Host "      Endpoint: http://localhost:8000" -ForegroundColor Cyan
}

Write-Host ""

# Check Node.js API
try {
    $nodeHealth = Invoke-RestMethod -Uri "http://localhost:3000/api/health" -Method Get -TimeoutSec 5
    Write-Host "   ✓ Node.js API: " -NoNewline -ForegroundColor Green
    Write-Host "http://localhost:3000/api" -ForegroundColor Cyan
    Write-Host "      Status: $($nodeHealth.status)" -ForegroundColor White
} catch {
    Write-Host "   ⚠️  Node.js API not responding yet..." -ForegroundColor Yellow
    Write-Host "      Endpoint: http://localhost:3000/api" -ForegroundColor Cyan
}

Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "📋 Server Information" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "Python FastAPI Server:" -ForegroundColor White
Write-Host "  URL:    http://localhost:8000" -ForegroundColor Cyan
Write-Host "  Docs:   http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "  Health: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Node.js Express Server:" -ForegroundColor White
Write-Host "  URL:    http://localhost:3000/api" -ForegroundColor Cyan
Write-Host "  Health: http://localhost:3000/api/health" -ForegroundColor Cyan
Write-Host "  ML API: http://localhost:3000/api/fertilizer-ml/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend (if running):" -ForegroundColor White
Write-Host "  URL:    http://localhost:8080" -ForegroundColor Cyan
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host "⌨️  Commands" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""
Write-Host "View Python logs:   " -NoNewline -ForegroundColor White
Write-Host "Receive-Job -Id $($pythonJob.Id) -Keep" -ForegroundColor Yellow
Write-Host "View Node.js logs:  " -NoNewline -ForegroundColor White
Write-Host "Receive-Job -Id $($nodeJob.Id) -Keep" -ForegroundColor Yellow
Write-Host "Stop servers:       " -NoNewline -ForegroundColor White
Write-Host "Stop-Job -Id $($pythonJob.Id),$($nodeJob.Id); Remove-Job -Id $($pythonJob.Id),$($nodeJob.Id)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press Ctrl+C to stop this script (servers will continue running)" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Cyan
Write-Host ""

# Monitor jobs
Write-Host "📊 Monitoring servers (press Ctrl+C to exit monitoring)..." -ForegroundColor Yellow
Write-Host ""

try {
    while ($true) {
        Start-Sleep -Seconds 5
        
        # Check job status
        $pythonStatus = (Get-Job -Id $pythonJob.Id).State
        $nodeStatus = (Get-Job -Id $nodeJob.Id).State
        
        if ($pythonStatus -ne "Running") {
            Write-Host "⚠️  Python server stopped unexpectedly! Check logs with: Receive-Job -Id $($pythonJob.Id)" -ForegroundColor Red
            break
        }
        
        if ($nodeStatus -ne "Running") {
            Write-Host "⚠️  Node.js server stopped unexpectedly! Check logs with: Receive-Job -Id $($nodeJob.Id)" -ForegroundColor Red
            break
        }
        
        # Display a heartbeat
        Write-Host "$(Get-Date -Format 'HH:mm:ss') - Servers running..." -ForegroundColor DarkGray
    }
} finally {
    Write-Host ""
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host "🛑 Monitoring stopped" -ForegroundColor Yellow
    Write-Host "=" * 70 -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Servers are still running in background jobs." -ForegroundColor White
    Write-Host "To stop them, run: " -NoNewline -ForegroundColor White
    Write-Host "Stop-Job -Id $($pythonJob.Id),$($nodeJob.Id); Remove-Job -Id $($pythonJob.Id),$($nodeJob.Id)" -ForegroundColor Yellow
    Write-Host ""
}
