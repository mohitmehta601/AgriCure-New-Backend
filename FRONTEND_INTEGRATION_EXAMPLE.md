# Frontend Integration Example

## How to Update EnhancedFertilizerForm.tsx

Replace the current API call in the `handleSubmit` function with the new service:

### Step 1: Import the new service

```typescript
import fertilizerRecommendationService, {
  FertilizerFormData,
} from "@/services/fertilizerRecommendationService";
```

### Step 2: Update the handleSubmit function

Find this section in `EnhancedFertilizerForm.tsx` (around line 340-400):

```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  if (!selectedFarm) {
    toast({
      title: t("common.error"),
      description: "Please select a farm first",
      variant: "destructive",
    });
    return;
  }

  setIsLoading(true);

  try {
    // Prepare data for new API
    const fertilizerFormData: FertilizerFormData = {
      // Farm details from selected farm
      size: selectedFarm.size,
      crop: selectedFarm.cropType,
      soil: selectedFarm.soilType,
      sowingDate:
        selectedFarm.sowingDate || new Date().toISOString().split("T")[0],

      // Soil chemistry from form
      nitrogen: parseFloat(formData.nitrogen),
      phosphorus: parseFloat(formData.phosphorus),
      potassium: parseFloat(formData.potassium),
      soilPH: parseFloat(formData.soilPH),

      // Soil physical properties from form
      soilMoisture: parseFloat(formData.soilMoisture),
      electricalConductivity: parseFloat(formData.electricalConductivity),
      soilTemperature: parseFloat(formData.soilTemperature),

      // Optional: Use LLM for enhanced recommendations
      useLLM: true, // Set to false for faster basic recommendations
    };

    // Call the new API
    const recommendation =
      await fertilizerRecommendationService.getRecommendation(
        fertilizerFormData
      );

    // Update state with results
    const enhancedData = {
      ...formData,
      mlPrediction: recommendation.ml_predictions.Primary_Fertilizer,
      llmEnhancedResult: recommendation,
      farm: selectedFarm,
    };

    onSubmit(enhancedData);

    toast({
      title: "✅ Recommendation Generated!",
      description: `Primary: ${recommendation.ml_predictions.Primary_Fertilizer}, Secondary: ${recommendation.ml_predictions.Secondary_Fertilizer}`,
    });
  } catch (error: any) {
    console.error("Error getting recommendation:", error);

    toast({
      title: t("common.error"),
      description: error.message || "Failed to get fertilizer recommendation",
      variant: "destructive",
    });
  } finally {
    setIsLoading(false);
  }
};
```

### Step 3: Add validation before API call

```typescript
// Validate all required fields
const requiredFields = [
  "nitrogen",
  "phosphorus",
  "potassium",
  "soilPH",
  "soilMoisture",
  "electricalConductivity",
  "soilTemperature",
];

const missingFields = requiredFields.filter((field) => !formData[field]);

if (missingFields.length > 0) {
  toast({
    title: "Validation Error",
    description: `Please fill in: ${missingFields.join(", ")}`,
    variant: "destructive",
  });
  setIsLoading(false);
  return;
}
```

## Complete Updated handleSubmit Function

```typescript
const handleSubmit = async (e: React.FormEvent) => {
  e.preventDefault();

  // Validation
  if (!selectedFarm) {
    toast({
      title: t("common.error"),
      description: "Please select a farm first",
      variant: "destructive",
    });
    return;
  }

  const requiredFields = [
    "nitrogen",
    "phosphorus",
    "potassium",
    "soilPH",
    "soilMoisture",
    "electricalConductivity",
    "soilTemperature",
  ];

  const missingFields = requiredFields.filter((field) => !formData[field]);

  if (missingFields.length > 0) {
    toast({
      title: "Validation Error",
      description: `Please fill in: ${missingFields.join(", ")}`,
      variant: "destructive",
    });
    return;
  }

  setIsLoading(true);

  try {
    // Prepare data for Final_Model API
    const fertilizerFormData: FertilizerFormData = {
      size: selectedFarm.size,
      crop: selectedFarm.cropType,
      soil: selectedFarm.soilType,
      sowingDate:
        selectedFarm.sowingDate || new Date().toISOString().split("T")[0],
      nitrogen: parseFloat(formData.nitrogen),
      phosphorus: parseFloat(formData.phosphorus),
      potassium: parseFloat(formData.potassium),
      soilPH: parseFloat(formData.soilPH),
      soilMoisture: parseFloat(formData.soilMoisture),
      electricalConductivity: parseFloat(formData.electricalConductivity),
      soilTemperature: parseFloat(formData.soilTemperature),
      useLLM: true, // Enable LLM for comprehensive recommendations
    };

    console.log("Requesting fertilizer recommendation...", fertilizerFormData);

    // Call the integrated API
    const recommendation =
      await fertilizerRecommendationService.getRecommendation(
        fertilizerFormData
      );

    console.log("Recommendation received:", recommendation);

    // Format data for display components
    const enhancedData = {
      ...formData,
      mlPrediction: recommendation.ml_predictions.Primary_Fertilizer,
      llmEnhancedResult: {
        ...recommendation,
        // Map to expected format
        primary_fertilizer: {
          name: recommendation.ml_predictions.Primary_Fertilizer,
        },
        secondary_fertilizer: {
          name: recommendation.ml_predictions.Secondary_Fertilizer,
        },
        ml_model_prediction: recommendation.ml_predictions,
        cost_estimate: recommendation.cost_estimate,
        application_timing: recommendation.application_timing,
        organic_alternatives: recommendation.organic_alternatives,
      },
      farm: selectedFarm,
    };

    onSubmit(enhancedData);

    toast({
      title: "🎯 Analysis Complete!",
      description: `Recommendations generated for ${selectedFarm.cropType}`,
    });
  } catch (error: any) {
    console.error("Fertilizer recommendation error:", error);

    toast({
      title: t("common.error"),
      description:
        error.message ||
        "Failed to get recommendation. Please ensure both servers are running.",
      variant: "destructive",
    });
  } finally {
    setIsLoading(false);
  }
};
```

## Testing the Integration

### 1. Start all servers

```powershell
cd "P:\Latest AgriCure\Backend"
.\start-integrated-servers.ps1
```

### 2. Start the frontend

```powershell
cd "P:\Latest AgriCure\Frontend"
npm run dev
```

### 3. Test the form

1. Navigate to the Fertilizer Recommendation page
2. Select a farm
3. Fill in all soil parameters (or use auto-fill if sensors are connected)
4. Click "Get ML Recommendation"
5. Check the recommendations display

### 4. Check browser console

Look for:

- "Requesting fertilizer recommendation..." with the data
- "Recommendation received:" with the response
- Any error messages

### 5. Check network tab

Look for the API call to:

- `http://localhost:3000/api/fertilizer-ml/recommend`
- Should return 200 OK
- Response should contain `ml_predictions`, `cost_estimate`, etc.

## Expected Output Structure

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
    "primary_cost": 2500,
    "secondary_cost": 800,
    "total": 3300,
    "currency": "INR"
  },
  "application_timing": {
    "sowing": "Apply at sowing time",
    "vegetative": "Apply during vegetative growth"
  },
  "timestamp": "2025-01-05T10:30:00"
}
```

## Troubleshooting

### Error: "Backend server is not available"

- Check if Python server is running on port 8000
- Check if Node.js server is running on port 3000
- Run health checks:
  ```powershell
  curl http://localhost:8000/health
  curl http://localhost:3000/api/fertilizer-ml/health
  ```

### Error: "Failed to get recommendation"

- Check Python server logs for errors
- Verify the dataset file exists
- Check if all models loaded successfully
- Look for validation errors in the request data

### Display Issues

- Verify `LLMEnhancedFertilizerRecommendations` component can handle the new format
- Check console for data structure mismatches
- Ensure all required fields are present in the response
