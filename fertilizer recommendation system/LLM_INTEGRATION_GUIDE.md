# 🌾 Enhanced Fertilizer Recommendation System with Gemini AI

## Overview

This system combines **Machine Learning predictions** with **Google Gemini AI** to generate comprehensive fertilizer recommendations including:

- ✅ Primary & Secondary fertilizer recommendations
- ✅ Organic alternatives (from predefined list only)
- ✅ Application timing based on crop sowing date
- ✅ Detailed cost analysis with Indian prices (₹/kg)
- ✅ Soil condition analysis
- ✅ NPK values in mg/kg units

---

## 📁 New Files Created

### 1. `llm_enhanced.py`

Main module for generating AI-enhanced recommendations using Gemini API.

**Key Features:**

- Uses Google Gemini 1.5 Flash model
- Generates organic alternatives ONLY from predefined list
- Calculates fertilizer quantities based on field size and nutrient status
- Provides detailed cost breakdown using Indian prices
- Includes fallback mode if Gemini API is unavailable

### 2. `generate_full_recommendation.py`

Complete integration script that combines ML model with LLM enhancements.

**Key Features:**

- Loads trained ML stacking model
- Gets predictions for all 6 targets (N, P, K status + fertilizers + pH amendment)
- Generates comprehensive recommendation report
- Saves output to JSON files
- Provides formatted console output

---

## 🚀 Setup Instructions

### Step 1: Install Dependencies

```powershell
# Navigate to the project directory
cd "p:\Latest AgriCure\Backend\fertilizer recommendation system"

# Install required packages
pip install google-generativeai python-dotenv
```

### Step 2: Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy the API key

### Step 3: Set Environment Variable

**Windows PowerShell:**

```powershell
$env:GEMINI_API_KEY="your-gemini-api-key-here"
```

**Windows CMD:**

```cmd
set GEMINI_API_KEY=your-gemini-api-key-here
```

**Linux/Mac:**

```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

**Alternative: Create .env file**

```powershell
# Create .env file in the project directory
echo "GEMINI_API_KEY=your-gemini-api-key-here" > .env
```

### Step 4: Train ML Model (if not already trained)

```powershell
python multioutput_stacking_fertilizer.py
```

This will create `stacked_model.pkl` file.

---

## 📊 Usage

### Basic Usage - Generate Recommendations

```powershell
python generate_full_recommendation.py
```

This will:

1. Load the trained ML model
2. Process example inputs (Wheat and Rice crops)
3. Generate AI-enhanced recommendations
4. Save results to JSON files
5. Display formatted summary in console

### Advanced Usage - Custom Inputs

Create your own script:

```python
from llm_enhanced import InputData, MLPrediction, generate_enhanced_recommendation

# Define your input data
input_data = InputData(
    temperature=28.5,
    humidity=65.0,
    moisture=55.0,
    soil_type="Loamy",
    crop="Wheat",
    nitrogen=180.0,      # mg/kg
    phosphorus=25.0,     # mg/kg
    potassium=150.0,     # mg/kg
    ph=6.8,
    ec=0.45,             # mmhos/cm²
    sowing_date="2025-11-20",  # ISO format
    field_size=2.27      # hectares
)

# ML model predictions (get from your ML model)
ml_prediction = MLPrediction(
    n_status="Optimal",
    p_status="Low",
    k_status="Optimal",
    primary_fertilizer="Urea",
    secondary_fertilizer="Potassium sulfate",
    ph_amendment="None"
)

# Confidence scores (optional)
confidence_scores = {
    "N_Status": 0.92,
    "P_Status": 0.88,
    "K_Status": 0.90,
    "Primary_Fertilizer": 0.89,
    "Secondary_Fertilizer": 0.85,
    "pH_Amendment": 0.95
}

# Generate recommendation
recommendation = generate_enhanced_recommendation(
    input_data=input_data,
    ml_prediction=ml_prediction,
    confidence_scores=confidence_scores
)

# Use the recommendation
print(recommendation)
```

---

## 📋 Output Format

The system generates a comprehensive JSON report with the following structure:

```json
{
  "ml_model_prediction": {
    "name": "Urea",
    "confidence_percent": 90,
    "npk": "46-0-0"
  },
  "soil_condition_analysis": {
    "current_status": {
      "pH_status": "Optimal",
      "moisture_status": "Optimal",
      "nutrient_deficiencies": ["Phosphorus"]
    },
    "soil_test_values": {
      "nitrogen_mg_kg": 180.0,
      "phosphorus_mg_kg": 25.0,
      "potassium_mg_kg": 150.0,
      "pH": 6.8,
      "EC_mmhos_cm2": 0.45
    },
    "recommendations": [
      "Maintain current pH levels",
      "Address Phosphorus deficiency",
      "Regular soil testing every 6 months is recommended"
    ]
  },
  "primary_fertilizer": {
    "name": "Urea",
    "amount_kg": 227,
    "npk": "46-0-0",
    "reason": "High nitrogen content fertilizer (46% N)...",
    "application_method": "Apply 2-3 weeks before planting..."
  },
  "secondary_fertilizer": {
    "name": "Potassium sulfate",
    "amount_kg": 91,
    "reason": "Addresses potassium deficiency...",
    "application_method": "Apply during fruit development stage..."
  },
  "organic_alternatives": [
    {
      "name": "Vermicompost",
      "amount_kg": 2266,
      "price_per_kg": 8,
      "cost": 18128,
      "reason": "Rich in nutrients, improves soil structure...",
      "timing": "Apply 3-4 weeks before planting"
    },
    {
      "name": "Neem cake",
      "amount_kg": 453,
      "price_per_kg": 25,
      "cost": 11325,
      "reason": "Natural pest deterrent and slow-release nitrogen...",
      "timing": "Apply at the time of land preparation"
    },
    {
      "name": "Bone meal",
      "amount_kg": 340,
      "price_per_kg": 30,
      "cost": 10200,
      "reason": "Excellent source of phosphorus and calcium",
      "timing": "Apply at basal dose before sowing"
    }
  ],
  "application_timing": {
    "primary_fertilizer": "Apply 1-2 weeks before planting (around 13 November 2025)...",
    "secondary_fertilizer": "Apply during fruit development stage (around 11 December 2025)...",
    "organic_options": "Apply 3-4 weeks before planting (around 30 October 2025)..."
  },
  "cost_estimate": {
    "primary_fertilizer": "₹9,065",
    "secondary_fertilizer": "₹5,666",
    "organic_options": "₹4,532",
    "total_estimate": "₹19,263",
    "field_size": "For 2.27 hectares (5.61 acres)",
    "breakdown": {
      "primary": {
        "fertilizer": "Urea",
        "quantity_kg": 227,
        "price_per_kg": "₹5.40",
        "total": "₹1,225"
      },
      "secondary": {
        "fertilizer": "Potassium sulfate",
        "quantity_kg": 91,
        "price_per_kg": "₹30.00",
        "total": "₹2,730"
      },
      "organics": [...]
    }
  },
  "_metadata": {
    "generated_at": "2025-11-06T10:30:45.123456",
    "crop": "Wheat",
    "soil_type": "Loamy",
    "sowing_date": "2025-11-20",
    "field_size_hectares": 2.27,
    "model_used": "Gemini-1.5-Flash + ML Stacking Model",
    "nutrient_units": "mg/kg"
  }
}
```

---

## 🌿 Organic Alternatives List

The system ONLY uses these predefined organic alternatives:

1. Mulch
2. Vermicompost
3. Mustard cake
4. Bone meal
5. Compost
6. Poultry manure
7. Neem cake
8. Banana wastes
9. Azolla
10. PSB (Phosphate Solubilizing Bacteria)
11. Rhizobium biofertilizer
12. Green manure
13. Farmyard manure (FYM)
14. Seaweed extract
15. Fish emulsion
16. Cow dung slurry
17. Bio-slurry
18. Trichoderma compost
19. Beejamrit
20. Panchagavya
21. Jeevamrut

---

## 💰 Price Reference (₹/kg)

### Primary Fertilizers

- Urea: ₹5.40/kg
- DAP: ₹27/kg
- MOP: ₹34/kg
- Calcium Ammonium Nitrate: ₹26/kg
- Ammonium Sulphate: ₹25/kg

### Organic Fertilizers

- Vermicompost: ₹8/kg
- Neem cake: ₹25/kg
- Bone meal: ₹30/kg
- Compost: ₹6/kg
- Poultry manure: ₹5/kg
- FYM: ₹4/kg

**Note:** Prices are indicative and based on average Indian market rates. Actual prices may vary by region and supplier.

---

## 🔧 Troubleshooting

### Issue: "GEMINI_API_KEY not set"

**Solution:** Set the environment variable or create a .env file with your API key.

### Issue: "Model file not found"

**Solution:** Train the ML model first:

```powershell
python multioutput_stacking_fertilizer.py
```

### Issue: "Import could not be resolved"

**Solution:** Install dependencies:

```powershell
pip install -r requirements.txt
```

### Issue: Gemini API call fails

**Solution:** The system automatically falls back to basic recommendations without AI enhancements.

---

## 🎯 Key Features Matching Your Image

✅ **ML Model Prediction** - Shows primary fertilizer with confidence percentage and NPK values

✅ **Soil Condition Analysis** - Current status (pH, Moisture) and nutrient deficiencies with detailed recommendations

✅ **Primary Fertilizer** - Name, quantity (kg), reason, and detailed application method

✅ **Secondary Fertilizer** - Name, quantity (kg), reason for addressing specific deficiency

✅ **Organic Alternatives** - 3 options with quantities, benefits, and timing (from predefined list only)

✅ **Application Timing** - Specific dates calculated from sowing date for primary, secondary, and organic fertilizers

✅ **Cost Estimate** - Breakdown for primary (₹9,065), secondary (₹5,666), organic (₹4,532), and total (₹19,263) for specified field size

✅ **NPK Values in mg/kg** - All nutrient measurements use mg/kg units as specified

---

## 📞 Support

For issues or questions, refer to:

- `ARCHITECTURE.md` - System architecture
- `PROJECT_SUMMARY.md` - Project overview
- `QUICKSTART.md` - Quick start guide

---

## 📝 Notes

1. **Organic alternatives** are ALWAYS selected from the predefined list
2. **NPK values** are provided in mg/kg (not kg/ha)
3. **Prices** are based on Indian market rates (₹/kg)
4. **Field size** calculations support hectares (default) and acres
5. **Application timing** is automatically calculated from sowing date
6. System works in **fallback mode** if Gemini API is unavailable

---

**Happy Farming! 🌾**
