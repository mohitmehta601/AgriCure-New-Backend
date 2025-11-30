# AgriCure FastAPI Server Startup Script
# PowerShell Script to start the API server

Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "🌾 AgriCure API Server Startup" -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan

# Check if virtual environment exists
if (-Not (Test-Path "venv")) {
  Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
  python -m venv venv
  Write-Host "✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if requirements are installed
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

Write-Host "✓ Dependencies installed" -ForegroundColor Green

# Check if model files exist
$modelPath = "Soil Type Prediction\soil_model_xgb.pkl"
$encoderPath = "Soil Type Prediction\soil_label_encoder.pkl"

if (-Not (Test-Path $modelPath)) {
  Write-Host "⚠️  Warning: Soil model not found at $modelPath" -ForegroundColor Red
  Write-Host "   Please train the model first by running:" -ForegroundColor Yellow
  Write-Host "   cd 'Soil Type Prediction'" -ForegroundColor Yellow
  Write-Host "   python train_soil_model.py" -ForegroundColor Yellow
  exit 1
}

if (-Not (Test-Path $encoderPath)) {
  Write-Host "⚠️  Warning: Label encoder not found at $encoderPath" -ForegroundColor Red
  exit 1
}

Write-Host "✓ Model files found" -ForegroundColor Green
Write-Host ""
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host "🚀 Starting FastAPI Server..." -ForegroundColor Green
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""
Write-Host "📍 Server URL: " -NoNewline -ForegroundColor Cyan
Write-Host "http://localhost:8000" -ForegroundColor White
Write-Host "📚 API Docs: " -NoNewline -ForegroundColor Cyan
Write-Host "http://localhost:8000/docs" -ForegroundColor White
Write-Host "📊 ReDoc: " -NoNewline -ForegroundColor Cyan
Write-Host "http://localhost:8000/redoc" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "=" -NoNewline -ForegroundColor Cyan
Write-Host ("=" * 69) -ForegroundColor Cyan
Write-Host ""

# Start the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
