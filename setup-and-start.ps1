# AgriCure API Complete Setup Script
# This script sets up everything needed and starts the API server

$line = "=" * 70
Write-Host $line -ForegroundColor Cyan
Write-Host "AgriCure API - Complete Setup & Start" -ForegroundColor Green
Write-Host $line -ForegroundColor Cyan
Write-Host ""

# Step 1: Create virtual environment
if (-Not (Test-Path "venv")) {
  Write-Host "Step 1/4: Creating virtual environment..." -ForegroundColor Yellow
  python -m venv venv
  Write-Host "Virtual environment created" -ForegroundColor Green
}
else {
  Write-Host "Step 1/4: Virtual environment already exists" -ForegroundColor Green
}

# Step 2: Activate and install dependencies
Write-Host "Step 2/4: Installing dependencies..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1
pip install -r requirements.txt --quiet
Write-Host "Dependencies installed" -ForegroundColor Green

# Step 3: Train model if needed
$modelPath = "Soil Type Prediction\soil_model_xgb.pkl"
$encoderPath = "Soil Type Prediction\soil_label_encoder.pkl"

if ((-Not (Test-Path $modelPath)) -or (-Not (Test-Path $encoderPath))) {
  Write-Host "Step 3/4: Training soil prediction model..." -ForegroundColor Yellow
  Write-Host "This may take a few minutes..." -ForegroundColor Cyan
    
  Push-Location "Soil Type Prediction"
    
  # Check if dataset exists
  if (-Not (Test-Path "india_soil_dataset.csv")) {
    Write-Host "Generating sample dataset..." -ForegroundColor Cyan
    python generate_sample_dataset.py
  }
    
  # Train model
  python train_soil_model.py
    
  Pop-Location
    
  if ((Test-Path $modelPath) -and (Test-Path $encoderPath)) {
    Write-Host "Model trained successfully" -ForegroundColor Green
  }
  else {
    Write-Host "Model training failed!" -ForegroundColor Red
    exit 1
  }
}
else {
  Write-Host "Step 3/4: Model files already exist" -ForegroundColor Green
}

# Step 4: Start the server
Write-Host "Step 4/4: Starting FastAPI server..." -ForegroundColor Yellow
Write-Host ""
Write-Host $line -ForegroundColor Cyan
Write-Host "Setup Complete! Server Starting..." -ForegroundColor Green
Write-Host $line -ForegroundColor Cyan
Write-Host ""
Write-Host "Server URL: http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "ReDoc: http://localhost:8000/redoc" -ForegroundColor Cyan
Write-Host ""
Write-Host "Frontend Config: Add to .env file:" -ForegroundColor Yellow
Write-Host "VITE_API_URL=http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host $line -ForegroundColor Cyan
Write-Host ""

# Start the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

