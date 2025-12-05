# 🚀 Quick Start Guide - Fertilizer Recommendation Integration

## Start Everything (One Command)

```powershell
cd "P:\Latest AgriCure\Backend"
.\start-integrated-servers.ps1
```

Then in another terminal:

```powershell
cd "P:\Latest AgriCure\Frontend"
npm run dev
```

## URLs

| Service       | URL                        | Purpose          |
| ------------- | -------------------------- | ---------------- |
| Frontend      | http://localhost:8080      | Your app UI      |
| Node.js API   | http://localhost:3000/api  | Main API         |
| Python ML API | http://localhost:8000      | ML models        |
| API Docs      | http://localhost:8000/docs | Interactive docs |

## Test the Integration

### 1. Quick Health Check

```powershell
curl http://localhost:8000/health
curl http://localhost:3000/api/fertilizer-ml/health
```

### 2. Test Recommendation

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
    "soil_temperature": 26
  }'
```

## Frontend Form → API Mapping

```typescript
// In your form component
import fertilizerRecommendationService from "@/services/fertilizerRecommendationService";

const recommendation = await fertilizerRecommendationService.getRecommendation({
  size: selectedFarm.size, // from farm selection
  crop: selectedFarm.cropType, // from farm selection
  soil: selectedFarm.soilType, // from farm selection
  sowingDate: selectedFarm.sowingDate, // from farm selection
  nitrogen: parseFloat(formData.nitrogen),
  phosphorus: parseFloat(formData.phosphorus),
  potassium: parseFloat(formData.potassium),
  soilPH: parseFloat(formData.soilPH),
  soilMoisture: parseFloat(formData.soilMoisture),
  electricalConductivity: parseFloat(formData.electricalConductivity),
  soilTemperature: parseFloat(formData.soilTemperature),
  useLLM: true, // set false for faster basic recommendations
});

// Use the response
console.log(recommendation.ml_predictions.Primary_Fertilizer);
console.log(recommendation.ml_predictions.Secondary_Fertilizer);
console.log(recommendation.cost_estimate);
```

## What You Get Back

```typescript
{
  success: true,
  ml_predictions: {
    N_Status: "High" | "Optimal" | "Low",
    P_Status: "High" | "Optimal" | "Low",
    K_Status: "High" | "Optimal" | "Low",
    Primary_Fertilizer: "DAP" | "Urea" | "NPK" | ...,
    Secondary_Fertilizer: "Zinc Sulphate" | "Boron" | ...,
    pH_Amendment: "Lime" | "Gypsum" | "None"
  },
  cost_estimate: {
    primary_fertilizer: "₹2,500",
    secondary_fertilizer: "₹800",
    total_estimate: "₹3,300",
    ...
  },
  application_timing: { ... },
  timestamp: "2025-01-05T10:30:00"
}
```

## Files You Need to Update

✅ **Already Done:**

- Backend/main.py - Python API endpoint
- Backend/src/routes/fertilizerML.js - Node.js proxy
- Backend/src/server.js - Route registration
- Backend/package.json - axios dependency
- Frontend service created

📝 **You Need to Update:**

- `Frontend/src/components/EnhancedFertilizerForm.tsx` - Replace API call in handleSubmit

See `FRONTEND_INTEGRATION_EXAMPLE.md` for exact code.

## Troubleshooting

| Problem                          | Solution                                                                   |
| -------------------------------- | -------------------------------------------------------------------------- |
| "Python ML API is not available" | Start Python server: `python run_server.py`                                |
| "Module not found: axios"        | Run `npm install` in Backend folder                                        |
| "Dataset not found"              | Check `fertilizer recommendation system/Primary and pH Dataset.csv` exists |
| Models not loading               | Run `pip install -r requirements.txt`                                      |
| Frontend errors                  | Check both servers are running, verify VITE_API_URL                        |

## Stop Servers

If using integrated script:

```powershell
# Get job IDs from script output, then:
Stop-Job -Id 1,2
Remove-Job -Id 1,2
```

Or press Ctrl+C in each terminal.

## Documentation Files

1. `INTEGRATION_COMPLETE_SUMMARY.md` - Complete overview
2. `FERTILIZER_INTEGRATION_GUIDE.md` - Detailed technical guide
3. `FRONTEND_INTEGRATION_EXAMPLE.md` - Frontend code examples
4. `FERTILIZER_QUICKSTART.md` - This quick reference

## Need Help?

Check in order:

1. Server health endpoints
2. Browser console (F12)
3. Network tab in browser
4. Python server logs
5. Node.js server logs
6. Documentation files above
