# FINAL MODEL - COMPLETE DOCUMENTATION

=======================================

## 📁 File Structure

```
fertilizer recommendation system New/
│
├── Final_Model.py                          ← MAIN FILE - Use this!
├── fertilizer_ml_model.py                  ← Primary ML model (dependency)
├── secondary_fertilizer_model.py           ← Secondary fertilizer model (dependency)
├── LLM_model.py                            ← LLM recommendation generator (dependency)
├── Primary and pH Dataset.csv              ← Training dataset (required)
│
├── README_FINAL_MODEL.md                   ← Full documentation
├── QUICK_START.py                          ← Quick start examples
├── test_final_model.py                     ← Test suite with examples
│
└── Output files (generated):
    ├── final_recommendation_output.json
    ├── user_recommendation_*.json
    ├── example_recommendation.json
    └── batch_recommendations.json
```

## 🎯 What Does Final_Model.py Do?

**INPUT:**

- Size (hectares)
- Crop type
- Soil type
- Sowing date
- Nitrogen (mg/kg)
- Phosphorus (mg/kg)
- Potassium (mg/kg)
- Soil pH
- Soil Moisture (%)
- Electrical Conductivity
- Soil Temperature (°C)

**PROCESSING:**

1. **Primary ML Model** → Predicts N_Status, P_Status, K_Status, Primary_Fertilizer, pH_Amendment
2. **Secondary Fertilizer Model** → Predicts Secondary_Fertilizer (micronutrients)
3. **LLM Model** → Generates comprehensive recommendations

**OUTPUT:**

- N_Status, P_Status, K_Status
- Primary_Fertilizer recommendation
- Secondary_Fertilizer recommendation
- pH_Amendment recommendation
- Cost estimates
- Application timing
- Organic alternatives
- Complete recommendation report (JSON)

## 🚀 Quick Start

### Method 1: Run Directly

```bash
python Final_Model.py
```

### Method 2: Use in Your Code

```python
from Final_Model import FinalFertilizerRecommendationSystem

system = FinalFertilizerRecommendationSystem()

result = system.predict(
    size=2.5,
    crop='Wheat',
    soil='Loamy',
    sowing_date='2025-11-15',
    nitrogen=180.0,
    phosphorus=25.0,
    potassium=150.0,
    soil_ph=6.8,
    soil_moisture=55.0,
    electrical_conductivity=450.0,
    soil_temperature=28.5,
    use_llm=False  # Set True for AI-enhanced (needs API key)
)

# Access results
print(result['ml_predictions']['Primary_Fertilizer'])
print(result['ml_predictions']['Secondary_Fertilizer'])
```

### Method 3: Run Examples

```bash
python test_final_model.py
```

### Method 4: Interactive Quick Start

```bash
python QUICK_START.py
```

## 📋 Input Parameters Detail

| Parameter               | Type   | Unit       | Example      | Description        |
| ----------------------- | ------ | ---------- | ------------ | ------------------ |
| size                    | float  | hectares   | 2.5          | Field size         |
| crop                    | string | -          | "Wheat"      | Crop to be grown   |
| soil                    | string | -          | "Loamy"      | Soil type          |
| sowing_date             | string | YYYY-MM-DD | "2025-11-15" | When you'll plant  |
| nitrogen                | float  | mg/kg      | 180.0        | Soil N content     |
| phosphorus              | float  | mg/kg      | 25.0         | Soil P content     |
| potassium               | float  | mg/kg      | 150.0        | Soil K content     |
| soil_ph                 | float  | -          | 6.8          | Soil pH level      |
| soil_moisture           | float  | %          | 55.0         | Soil moisture %    |
| electrical_conductivity | float  | µS/cm      | 450.0        | Soil EC            |
| soil_temperature        | float  | °C         | 28.5         | Soil temperature   |
| use_llm                 | bool   | -          | False        | Use AI enhancement |

## 📊 Output Structure

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
    "primary_fertilizer": "2025-11-15 (Sowing), 2025-12-15 (30 days), 2026-01-14 (60 days)",
    "secondary_fertilizer": "Apply during active growth phase",
    "organic_options": "Apply 3-4 weeks before sowing"
  },

  "soil_condition_analysis": {
    "current_status": {
      "N_status": "Optimal",
      "P_status": "Low",
      "K_status": "Optimal",
      "pH_status": "Optimal",
      "moisture_status": "Optimal"
    },
    "soil_test_values": {
      "nitrogen_mg_kg": 180.0,
      "phosphorus_mg_kg": 25.0,
      "potassium_mg_kg": 150.0,
      "pH": 6.8,
      "EC_mmhos_cm2": 450.0,
      "soil_temperature": 28.5,
      "soil_moisture": 55.0
    }
  },

  "primary_fertilizer": {
    "name": "Urea",
    "amount_kg": 150,
    "npk": "46-0-0",
    "reason": "For nitrogen requirement",
    "application_method": "Split dose application"
  },

  "secondary_fertilizer": {
    "name": "Zinc Sulphate",
    "amount_kg": 15,
    "reason": "Micronutrient deficiency",
    "application_method": "Soil application"
  },

  "organic_alternatives": [
    {
      "name": "Vermicompost",
      "amount_kg": 500,
      "price_per_kg": 15.0,
      "cost": 7500,
      "reason": "Organic nitrogen source",
      "timing": "3-4 weeks before sowing"
    }
  ]
}
```

## 🔧 Installation Requirements

### Python Packages

```bash
pip install pandas numpy scikit-learn xgboost catboost lightgbm
pip install google-generativeai python-dotenv  # Optional, for LLM mode
```

### Required Files

✅ Final_Model.py  
✅ fertilizer_ml_model.py  
✅ secondary_fertilizer_model.py  
✅ LLM_model.py  
✅ Primary and pH Dataset.csv

### Optional (for AI-enhanced mode)

- .env file with GEMINI_API_KEY=your-key-here

## 🎨 Usage Examples

### Example 1: Single Prediction

```python
from Final_Model import FinalFertilizerRecommendationSystem

system = FinalFertilizerRecommendationSystem()

rec = system.predict(
    size=2.5, crop='Wheat', soil='Loamy', sowing_date='2025-11-15',
    nitrogen=180, phosphorus=25, potassium=150, soil_ph=6.8,
    soil_moisture=55, electrical_conductivity=450,
    soil_temperature=28.5, use_llm=False
)

print(rec['ml_predictions'])
```

### Example 2: Batch Processing

```python
from Final_Model import FinalFertilizerRecommendationSystem

system = FinalFertilizerRecommendationSystem()

fields = [
    {'crop': 'Wheat', 'nitrogen': 180, 'phosphorus': 25},
    {'crop': 'Rice', 'nitrogen': 140, 'phosphorus': 18},
    {'crop': 'Maize', 'nitrogen': 160, 'phosphorus': 22}
]

for field in fields:
    rec = system.predict(
        size=2.5, crop=field['crop'], soil='Loamy',
        sowing_date='2025-11-15', nitrogen=field['nitrogen'],
        phosphorus=field['phosphorus'], potassium=150, soil_ph=6.8,
        soil_moisture=55, electrical_conductivity=450,
        soil_temperature=28.5, use_llm=False
    )
    print(f"{field['crop']}: {rec['ml_predictions']['Primary_Fertilizer']}")
```

### Example 3: Save to File

```python
import json
from Final_Model import FinalFertilizerRecommendationSystem

system = FinalFertilizerRecommendationSystem()

rec = system.predict(
    size=2.5, crop='Wheat', soil='Loamy', sowing_date='2025-11-15',
    nitrogen=180, phosphorus=25, potassium=150, soil_ph=6.8,
    soil_moisture=55, electrical_conductivity=450,
    soil_temperature=28.5, use_llm=False
)

with open('my_recommendation.json', 'w') as f:
    json.dump(rec, f, indent=2)
```

## 📈 Model Architecture

```
┌─────────────────────────────────────────────────────┐
│                   USER INPUT                         │
│  (Size, Crop, Soil, Date, N, P, K, pH, etc.)       │
└──────────────────┬──────────────────────────────────┘
                   │
                   ├──────────────────────────────────┐
                   │                                  │
                   ▼                                  ▼
        ┌──────────────────────┐         ┌──────────────────────┐
        │  PRIMARY ML MODEL    │         │ SECONDARY FERT MODEL │
        │ (Random Forest/XGB)  │         │   (Rule-based)       │
        └──────────┬───────────┘         └──────────┬───────────┘
                   │                                  │
                   │  N/P/K Status                   │  Micronutrients
                   │  Primary Fertilizer             │  Secondary Fert
                   │  pH Amendment                   │
                   │                                  │
                   └──────────┬───────────────────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │    LLM MODEL        │
                   │  (Gemini/Fallback)  │
                   └──────────┬──────────┘
                              │
                              ▼
                   ┌─────────────────────┐
                   │  FINAL REPORT       │
                   │  (JSON Output)      │
                   └─────────────────────┘
```

## ⚠️ Troubleshooting

### Problem: Model not training

**Solution:** Ensure `Primary and pH Dataset.csv` is in the same directory

### Problem: Import errors

**Solution:** Install required packages:

```bash
pip install pandas numpy scikit-learn xgboost catboost lightgbm
```

### Problem: LLM API errors

**Solution:** Set `use_llm=False` or configure API key in `.env` file

### Problem: Unknown soil/crop type

**Solution:** The model uses label encoding and will handle unseen categories

## 📞 Support

For issues:

1. Check all required files are present
2. Verify Python packages are installed
3. Ensure dataset CSV is accessible
4. Try with `use_llm=False` first

## 🎯 Key Features

✅ **Multi-Model Integration** - Combines 3 AI models  
✅ **Comprehensive Outputs** - Primary, secondary, organic fertilizers  
✅ **Cost Estimation** - Based on field size and market prices  
✅ **Application Timing** - Specific dates based on sowing  
✅ **Fallback Mode** - Works without API access  
✅ **Batch Processing** - Handle multiple fields  
✅ **JSON Export** - Easy integration with other systems

## 📝 Citation

```
AgriCure AI Team
Final Fertilizer Recommendation System
December 2025
```

## 🔄 Workflow Summary

1. **Initialize System** → `system = FinalFertilizerRecommendationSystem()`
2. **Provide Inputs** → Soil parameters, crop info, field size
3. **Get Predictions** → `result = system.predict(...)`
4. **Access Results** → `result['ml_predictions']`, `result['cost_estimate']`
5. **Save/Export** → JSON file for further use

---

**Ready to use!** Start with `python Final_Model.py` or see `QUICK_START.py` for examples.
