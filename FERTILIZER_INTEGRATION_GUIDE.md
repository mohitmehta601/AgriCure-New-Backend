# Fertilizer Recommendation System Integration

## Overview

The AgriCure Fertilizer Recommendation System has been successfully integrated with the application. This integration connects the `Final_Model.py` (which combines Primary ML Model + Secondary Fertilizer Model + LLM) with the frontend form.

## Architecture

```
Frontend Form (React)
    ↓
Frontend Service (fertilizerRecommendationService.ts)
    ↓
Node.js Backend (Express - port 3000)
    ↓ (proxies request)
Python FastAPI Server (port 8000)
    ↓
Final_Model.py
    ├── Primary ML Model (N/P/K status, Primary Fertilizer, pH Amendment)
    ├── Secondary Fertilizer Model (Micronutrients)
    └── LLM Model (Enhanced recommendations with cost analysis)
```

## Components

### 1. Python FastAPI Server (`Backend/main.py`)

- **Port**: 8000
- **New Endpoints**:
  - `POST /fertilizer-recommendation` - Get fertilizer recommendations
  - `POST /predict-llm-enhanced` - Get LLM-enhanced recommendations
- **Features**:
  - Integrates `Final_Model.py` system
  - Returns ML predictions, cost estimates, and application timing
  - Supports both basic and LLM-enhanced modes

### 2. Node.js Backend (`Backend/src/routes/fertilizerML.js`)

- **Port**: 3000
- **New Routes**:
  - `POST /api/fertilizer-ml/recommend` - Proxy to Python API
  - `POST /api/fertilizer-ml/recommend-enhanced` - LLM-enhanced proxy
  - `GET /api/fertilizer-ml/health` - Check Python API health
  - `GET /api/fertilizer-ml/model-info` - Get model information

### 3. Frontend Service (`Frontend/src/services/fertilizerRecommendationService.ts`)

- TypeScript service for calling the API
- Type-safe interfaces for request/response
- Error handling and timeout management

## Setup Instructions

### Prerequisites

1. Python 3.8+ with required packages
2. Node.js 16+ with npm
3. MongoDB (for user/farm data)

### Step 1: Install Python Dependencies

```powershell
cd "P:\Latest AgriCure\Backend\fertilizer recommendation system"
pip install -r ../requirements.txt
```

### Step 2: Install Node.js Dependencies

```powershell
cd "P:\Latest AgriCure\Backend"
npm install
```

This will install the new `axios` dependency needed for the proxy.

### Step 3: Start the Servers

#### Option A: Use the integrated startup script (Recommended)

```powershell
cd "P:\Latest AgriCure\Backend"
.\start-integrated-servers.ps1
```

#### Option B: Start servers manually

**Terminal 1 - Python API:**

```powershell
cd "P:\Latest AgriCure\Backend"
python run_server.py
```

**Terminal 2 - Node.js API:**

```powershell
cd "P:\Latest AgriCure\Backend"
node src/server.js
```

**Terminal 3 - Frontend:**

```powershell
cd "P:\Latest AgriCure\Frontend"
npm run dev
```

## API Request/Response Format

### Request Format

```json
{
  "size": 2.5,
  "crop": "Wheat",
  "soil": "Loamy",
  "sowing_date": "2025-01-05",
  "nitrogen": 190,
  "phosphorus": 9.5,
  "potassium": 115,
  "soil_ph": 7.1,
  "soil_moisture": 32,
  "electrical_conductivity": 0.5,
  "soil_temperature": 26,
  "use_llm": false
}
```

### Response Format

```json
{
  "success": true,
  "ml_predictions": {
    "N_Status": "High",
    "P_Status": "Low",
    "K_Status": "Optimal",
    "Primary_Fertilizer": "DAP",
    "Secondary_Fertilizer": "Zinc Sulphate",
    "pH_Amendment": "None"
  },
  "cost_estimate": {
    "primary_fertilizer": "₹2,500",
    "secondary_fertilizer": "₹800",
    "organic_options": "₹1,200",
    "total_estimate": "₹4,500",
    "field_size": "2.5 hectares",
    "currency": "INR"
  },
  "application_timing": {
    "sowing": "Apply DAP at sowing",
    "vegetative": "Apply Urea in vegetative stage",
    "flowering": "Foliar spray of micronutrients",
    "maturity": "No fertilizer required"
  },
  "timestamp": "2025-01-05T10:30:00"
}
```

## Form Field Mapping

The frontend form fields map to the API as follows:

| Form Field                      | API Parameter             | Source            |
| ------------------------------- | ------------------------- | ----------------- |
| Farm Selection → Size           | `size`                    | Farm data         |
| Farm Selection → Crop Type      | `crop`                    | Farm data         |
| Farm Selection → Soil Type      | `soil`                    | Farm data         |
| Farm Selection → Sowing Date    | `sowing_date`             | Farm data         |
| Nitrogen (mg/kg)                | `nitrogen`                | User input/sensor |
| Phosphorus (mg/kg)              | `phosphorus`              | User input/sensor |
| Potassium (mg/kg)               | `potassium`               | User input/sensor |
| Soil pH                         | `soil_ph`                 | User input/sensor |
| Soil Moisture (%)               | `soil_moisture`           | User input/sensor |
| Electrical Conductivity (µS/cm) | `electrical_conductivity` | User input/sensor |
| Soil Temperature (°C)           | `soil_temperature`        | User input/sensor |

## Testing

### Test the Python API directly:

```powershell
cd "P:\Latest AgriCure\Backend"
python -c "import requests; print(requests.get('http://localhost:8000/health').json())"
```

### Test through Node.js proxy:

```powershell
curl http://localhost:3000/api/fertilizer-ml/health
```

### Test full recommendation:

```powershell
curl -X POST http://localhost:3000/api/fertilizer-ml/recommend `
  -H "Content-Type: application/json" `
  -d '{
    "size": 2.5,
    "crop": "Wheat",
    "soil": "Loamy",
    "sowing_date": "2025-01-05",
    "nitrogen": 190,
    "phosphorus": 9.5,
    "potassium": 115,
    "soil_ph": 7.1,
    "soil_moisture": 32,
    "electrical_conductivity": 0.5,
    "soil_temperature": 26,
    "use_llm": false
  }'
```

## Environment Variables

### Backend (.env)

```
PORT=3000
PYTHON_API_URL=http://localhost:8000
```

### Frontend (.env)

```
VITE_API_URL=http://localhost:3000/api
```

## Troubleshooting

### Python API not loading

1. Check if all dependencies are installed: `pip install -r requirements.txt`
2. Verify `Primary and pH Dataset.csv` exists in `fertilizer recommendation system/` folder
3. Check Python logs for model loading errors

### Node.js proxy errors

1. Ensure axios is installed: `npm install`
2. Check PYTHON_API_URL environment variable
3. Verify Python server is running on port 8000

### Frontend errors

1. Check VITE_API_URL points to Node.js server
2. Ensure both backend servers are running
3. Check browser console for detailed errors

## Features

### Basic Mode (use_llm: false)

- Fast ML predictions
- N/P/K status classification
- Primary fertilizer recommendation
- Secondary fertilizer (micronutrients)
- pH amendment suggestions

### Enhanced Mode (use_llm: true)

- All basic features
- Detailed cost analysis
- Application timing recommendations
- Organic alternatives
- Comprehensive AI-generated report
- Field-specific calculations

## File Structure

```
Backend/
├── main.py                           # FastAPI server with fertilizer endpoint
├── src/
│   ├── server.js                     # Node.js Express server
│   └── routes/
│       └── fertilizerML.js          # NEW: Fertilizer ML proxy routes
├── fertilizer recommendation system/
│   ├── Final_Model.py               # Main recommendation system
│   ├── fertilizer_ml_model.py       # Primary ML model
│   ├── secondary_fertilizer_model.py# Secondary model
│   └── LLM_model.py                 # LLM enhancement
└── package.json                      # Updated with axios

Frontend/
└── src/
    └── services/
        └── fertilizerRecommendationService.ts  # NEW: Type-safe API client
```

## Next Steps

1. **Update Frontend Form Component** to use the new service
2. **Add Error Handling** UI for API failures
3. **Implement Loading States** during API calls
4. **Add Cost Display** components for recommendations
5. **Create History** feature to save recommendations

## Support

For issues or questions:

1. Check server logs in both terminals
2. Verify all services are running with health checks
3. Review error messages in browser console
4. Check network tab for failed requests
