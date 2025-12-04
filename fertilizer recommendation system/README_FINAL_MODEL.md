# Final Fertilizer Recommendation System

## Overview

The `Final_Model.py` integrates three AI models to provide comprehensive fertilizer recommendations:

1. **Primary ML Model** (`fertilizer_ml_model.py`) - Predicts N_Status, P_Status, K_Status, Primary_Fertilizer, pH_Amendment
2. **Secondary Fertilizer Model** (`secondary_fertilizer_model.py`) - Predicts Secondary_Fertilizer (micronutrients)
3. **LLM Model** (`LLM_model.py`) - Generates enhanced recommendations using Google Gemini API

## Input Parameters

The system requires the following inputs:

| Parameter               | Type   | Unit       | Example      |
| ----------------------- | ------ | ---------- | ------------ |
| Size                    | float  | hectares   | 2.5          |
| Crop                    | string | -          | "Wheat"      |
| Soil                    | string | -          | "Loamy"      |
| Sowing Date             | string | YYYY-MM-DD | "2025-11-15" |
| Nitrogen                | float  | mg/kg      | 180.0        |
| Phosphorus              | float  | mg/kg      | 25.0         |
| Potassium               | float  | mg/kg      | 150.0        |
| Soil pH                 | float  | -          | 6.8          |
| Soil Moisture           | float  | %          | 55.0         |
| Electrical Conductivity | float  | µS/cm      | 450.0        |
| Soil Temperature        | float  | °C         | 28.5         |

## Output

The system provides:

- **N_Status, P_Status, K_Status** - Nutrient status (Low/Optimal/High)
- **Primary_Fertilizer** - Recommended primary fertilizer (e.g., Urea, DAP)
- **Secondary_Fertilizer** - Recommended micronutrient fertilizer (e.g., Zinc Sulphate)
- **pH_Amendment** - Soil pH correction recommendations
- **Enhanced Report** - Detailed recommendations including:
  - Application timing
  - Quantities and costs
  - Organic alternatives
  - Soil condition analysis

## Usage

### Method 1: Run the Script Directly

```bash
python Final_Model.py
```

This will:

1. Run an example with predefined parameters
2. Optionally allow you to enter your own data interactively

### Method 2: Import and Use Programmatically

```python
from Final_Model import FinalFertilizerRecommendationSystem

# Initialize the system
system = FinalFertilizerRecommendationSystem()

# Make a prediction
recommendation = system.predict(
    size=2.5,                      # hectares
    crop='Wheat',
    soil='Loamy',
    sowing_date='2025-11-15',
    nitrogen=180.0,                # mg/kg
    phosphorus=25.0,               # mg/kg
    potassium=150.0,               # mg/kg
    soil_ph=6.8,
    soil_moisture=55.0,            # %
    electrical_conductivity=450.0,
    soil_temperature=28.5,         # °C
    use_llm=True                   # Use AI-enhanced recommendations
)

# Access results
print(recommendation['ml_predictions'])
print(recommendation['cost_estimate'])
```

### Method 3: Interactive Mode

When running the script, you'll be prompted to enter your own data:

```
Would you like to enter your own data? (yes/no): yes

--- Field & Crop Information ---
Field Size (hectares): 2.5
Crop Type (e.g., Wheat, Rice, Maize): Wheat
Soil Type (e.g., Loamy, Clay, Sandy, Alluvial): Loamy
Sowing Date (YYYY-MM-DD): 2025-11-15

--- Soil Test Parameters ---
Nitrogen (mg/kg): 180
Phosphorus (mg/kg): 25
Potassium (mg/kg): 150
...
```

## Requirements

### Python Packages

```bash
pip install pandas numpy scikit-learn xgboost catboost lightgbm google-generativeai python-dotenv
```

### Files Required

- `Primary and pH Dataset.csv` - Dataset for training primary ML model
- `fertilizer_ml_model.py` - Primary fertilizer prediction model
- `secondary_fertilizer_model.py` - Secondary fertilizer prediction model
- `LLM_model.py` - LLM-based recommendation generator
- `.env` file with `GEMINI_API_KEY` (optional, for enhanced recommendations)

## Output Files

The system generates JSON files with complete recommendations:

- `final_recommendation_output.json` - Example recommendation
- `user_recommendation_YYYYMMDD_HHMMSS.json` - User-specific recommendations

## Example Output

```json
{
  "ml_predictions": {
    "N_Status": "Optimal",
    "P_Status": "Low",
    "K_Status": "Optimal",
    "Primary_Fertilizer": "Urea",
    "Secondary_Fertilizer": "Zinc Sulphate",
    "pH_Amendment": "None"
  },
  "cost_estimate": {
    "primary_fertilizer": "₹4,200",
    "secondary_fertilizer": "₹1,050",
    "organic_options": "₹2,250",
    "total_estimate": "₹7,500",
    "field_size": "For 2.50 hectares"
  },
  "application_timing": {
    "primary_fertilizer": "Apply in 3 split doses...",
    "secondary_fertilizer": "Apply during active growth...",
    "organic_options": "Apply 3-4 weeks before sowing"
  }
}
```

## Features

✅ **Multi-Model Integration** - Combines ML predictions with rule-based systems  
✅ **Comprehensive Recommendations** - Primary, secondary, and organic fertilizers  
✅ **Cost Estimation** - Calculates costs based on field size  
✅ **Application Timing** - Provides specific dates based on sowing date  
✅ **AI-Enhanced** - Optional LLM-based detailed recommendations  
✅ **Fallback Mode** - Works even without LLM/API access

## Troubleshooting

### Model Not Training

- Ensure `Primary and pH Dataset.csv` is in the same directory
- Check that all required columns are present

### LLM Errors

- Set `use_llm=False` to use fallback mode without API
- Check `.env` file has valid `GEMINI_API_KEY`
- Install: `pip install google-generativeai python-dotenv`

### Import Errors

- Ensure all model files are in the same directory
- Install all required packages

## Support

For issues or questions, please check:

1. All required files are present
2. All Python packages are installed
3. Dataset CSV file is accessible
4. API key is configured (for LLM mode)

---

**Author:** AgriCure AI Team  
**Last Updated:** December 2025
