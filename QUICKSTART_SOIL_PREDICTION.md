# 🚀 Quick Start: Testing Soil Prediction Integration

## Prerequisites

- Python virtual environment activated
- Required packages installed (`pip install -r requirements.txt`)

## Step 1: Start the Python Server

```powershell
# Activate virtual environment (if not already activated)
.\.venv\Scripts\Activate.ps1

# Start the FastAPI server
python run_server.py
```

You should see:

```
======================================================================
🌾 AgriCure API Server Starting...
======================================================================
Model Status: ✓ Loaded
Soil Types: X types available
CORS: Enabled for all origins
======================================================================
```

Server will be running at: **http://localhost:8000**

## Step 2: Verify Server Health

Open a browser and go to:

- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

Or use PowerShell:

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

## Step 3: Test Soil Prediction

Run the integration test:

```powershell
python test-soil-integration.py
```

This will test:

- ✅ Server health
- ✅ Soil data endpoint (main integration)
- ✅ Multiple locations across India

## Step 4: Test from Frontend

1. **Start all servers:**

   ```powershell
   # From Backend directory
   .\start-all-servers.ps1
   ```

2. **Start Frontend:**

   ```powershell
   # From Frontend directory
   npm run dev
   ```

3. **Test in Browser:**
   - Go to http://localhost:5173
   - Login to your account
   - Navigate to Dashboard
   - Click "Add Farm"
   - Click "Get My Location & Soil Type"
   - Browser will ask for location permission
   - Soil type will be auto-detected!

## Manual API Test

Test the API directly with PowerShell:

```powershell
$body = @{
    latitude = 28.6139
    longitude = 77.2090
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/soil-data" `
  -Method Post `
  -ContentType "application/json" `
  -Body $body
```

Expected response:

```json
{
  "location": {
    "latitude": 28.6139,
    "longitude": 77.209,
    "timestamp": "2025-12-01T..."
  },
  "soil_type": "Clay Loam",
  "confidence": 0.87,
  "success": true,
  "sources": ["ML Model Prediction", "XGBoost Classifier"]
}
```

## Troubleshooting

### Server won't start

```powershell
# Check if port 8000 is in use
Get-NetTCPConnection -LocalPort 8000

# Install dependencies
pip install -r requirements.txt
```

### Model not loading

```powershell
# Verify model files exist
cd "Soil Type Prediction"
dir soil_model_xgb.pkl
dir soil_label_encoder.pkl
```

### Import errors

```powershell
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Next Steps

✅ Integration is complete and working!

Read the full documentation: **SOIL_PREDICTION_INTEGRATION.md**

## Quick Links

- **API Documentation:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health
- **Soil Types List:** http://localhost:8000/soil-types
- **API Info:** http://localhost:8000/api-info
