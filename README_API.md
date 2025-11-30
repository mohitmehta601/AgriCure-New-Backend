# AgriCure FastAPI Server

FastAPI server integrating soil prediction model with the Add Farm form.

## 🚀 Quick Start

### Windows (PowerShell)

```powershell
.\start-api.ps1
```

### Windows (Command Prompt)

```batch
start-api.bat
```

### Manual Start

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat

# Install dependencies
pip install -r requirements.txt

# Start server
python main.py
# OR
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Trained soil model** files:
   - `Soil Type Prediction/soil_model_xgb.pkl`
   - `Soil Type Prediction/soil_label_encoder.pkl`

### Training the Model (if not already done)

```bash
cd "Soil Type Prediction"
python train_soil_model.py
cd ..
```

## 🌐 API Endpoints

Once the server is running, access:

- **Server**: http://localhost:8000
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Main Endpoints

#### 1. Health Check

```http
GET /
GET /health
```

Returns server health status and model loading status.

#### 2. Get Soil Data (for Add Farm Form)

```http
POST /soil-data
Content-Type: application/json

{
  "latitude": 28.6139,
  "longitude": 77.2090
}
```

**Response:**

```json
{
  "location": {
    "latitude": 28.6139,
    "longitude": 77.209,
    "timestamp": "2025-12-01T12:00:00"
  },
  "soil_type": "Alluvial Soil",
  "confidence": 0.87,
  "soil_properties": {
    "clay": null,
    "sand": null,
    "silt": null
  },
  "sources": ["ML Model Prediction", "XGBoost Classifier"],
  "success": true,
  "location_info": {
    "country": "India"
  }
}
```

#### 3. Direct Soil Prediction (Advanced)

```http
POST /predict-soil
Content-Type: application/json

{
  "lat": 28.6139,
  "lon": 77.2090,
  "elevation": 300,
  "rainfall": 800,
  "temperature": 25,
  "aridity_index": 0.65,
  "dist_river_km": 10,
  "dist_coast_km": 500,
  "ndvi": 0.45,
  "landcover": "cropland",
  "geology": "alluvium"
}
```

#### 4. Get Available Soil Types

```http
GET /soil-types
```

#### 5. API Information

```http
GET /api-info
```

## 🔌 Frontend Integration

The API is configured for CORS and works with the frontend Add Farm form.

### Frontend Configuration

Update your frontend `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

### Usage in Add Farm Form

The frontend `locationSoilService.ts` already calls the `/soil-data` endpoint:

```typescript
const response = await fetch(`${API_BASE_URL}/soil-data`, {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    latitude: 28.6139,
    longitude: 77.209,
  }),
});
```

## 📦 Dependencies

- **FastAPI**: Modern, fast web framework
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation
- **Pandas**: Data manipulation
- **Scikit-learn**: ML preprocessing
- **XGBoost**: ML model
- **Joblib**: Model serialization

## 🗂️ Project Structure

```
Backend/
├── main.py                      # Main FastAPI application
├── requirements.txt              # Python dependencies
├── start-api.ps1                # PowerShell startup script
├── start-api.bat                # Batch startup script
├── README_API.md                # This file
└── Soil Type Prediction/
    ├── soil_model_xgb.pkl       # Trained model
    ├── soil_label_encoder.pkl   # Label encoder
    └── train_soil_model.py      # Model training script
```

## 🔧 Configuration

### Port Configuration

Default port: `8000`

To change the port, modify in `main.py`:

```python
uvicorn.run("main:app", host="0.0.0.0", port=YOUR_PORT, reload=True)
```

### CORS Configuration

Currently allows all origins for development. For production, update in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🧪 Testing

### Test Health Endpoint

```bash
curl http://localhost:8000/health
```

### Test Soil Data Endpoint

```bash
curl -X POST http://localhost:8000/soil-data \
  -H "Content-Type: application/json" \
  -d '{"latitude": 28.6139, "longitude": 77.2090}'
```

### Using PowerShell

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get

$body = @{
    latitude = 28.6139
    longitude = 77.2090
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/soil-data" -Method Post -Body $body -ContentType "application/json"
```

## 📝 Features

✅ **Soil Type Prediction**: ML-based soil classification  
✅ **Location Integration**: Accept GPS coordinates  
✅ **CORS Enabled**: Works with frontend  
✅ **Auto Documentation**: Interactive API docs  
✅ **Model Validation**: Health checks  
✅ **Error Handling**: Comprehensive error responses  
✅ **Logging**: Detailed server logs

## 🐛 Troubleshooting

### Model Not Found Error

```
Error: Model not loaded
```

**Solution**: Train the model first:

```bash
cd "Soil Type Prediction"
python train_soil_model.py
```

### Port Already in Use

```
Error: Address already in use
```

**Solution**: Change the port or kill the process:

```bash
# Find process
netstat -ano | findstr :8000
# Kill process
taskkill /PID <PID> /F
```

### Import Errors

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**: Install dependencies:

```bash
pip install -r requirements.txt
```

## 📊 Model Information

- **Algorithm**: XGBoost Classifier
- **Input Features**: 11 features (9 numeric + 2 categorical)
- **Output**: Soil type classification with confidence scores
- **Supported Soil Types**: Based on Indian soil classification

## 🔐 Security Notes

⚠️ **For Production**:

1. Update CORS to specific origins
2. Add authentication/API keys
3. Use HTTPS
4. Add rate limiting
5. Validate all inputs
6. Set up proper logging and monitoring

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Uvicorn Documentation](https://www.uvicorn.org/)
- [XGBoost Documentation](https://xgboost.readthedocs.io/)

## 🤝 Support

For issues or questions, check the server logs or visit the interactive API docs at http://localhost:8000/docs
