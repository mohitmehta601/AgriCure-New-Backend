"""
QUICK START GUIDE - Final Fertilizer Recommendation System
===========================================================

This guide shows you how to quickly get started with the Final_Model.py
"""

# ============================================================================
# OPTION 1: QUICKEST START (Run the main script)
# ============================================================================

# Just run this command in your terminal:
# python Final_Model.py

# This will:
# 1. Initialize all models
# 2. Run an example prediction
# 3. Ask if you want to enter your own data
# 4. Save results to JSON files


# ============================================================================
# OPTION 2: SIMPLE PYTHON SCRIPT
# ============================================================================

from Final_Model import FinalFertilizerRecommendationSystem

# Initialize once
system = FinalFertilizerRecommendationSystem()

# Get recommendation
result = system.predict(
    size=2.5,                       # Field size in hectares
    crop='Wheat',                   # Your crop
    soil='Loamy',                   # Your soil type
    sowing_date='2025-11-15',       # When you'll sow (YYYY-MM-DD)
    nitrogen=180.0,                 # Soil test: N in mg/kg
    phosphorus=25.0,                # Soil test: P in mg/kg
    potassium=150.0,                # Soil test: K in mg/kg
    soil_ph=6.8,                    # Soil pH
    soil_moisture=55.0,             # Soil moisture %
    electrical_conductivity=450.0,  # EC
    soil_temperature=28.5,          # Soil temp in °C
    use_llm=False                   # Set True for AI-enhanced (needs API key)
)

# Get your recommendations
print("Primary Fertilizer:", result['ml_predictions']['Primary_Fertilizer'])
print("Secondary Fertilizer:", result['ml_predictions']['Secondary_Fertilizer'])
print("N Status:", result['ml_predictions']['N_Status'])
print("P Status:", result['ml_predictions']['P_Status'])
print("K Status:", result['ml_predictions']['K_Status'])


# ============================================================================
# OPTION 3: INTERACTIVE MODE
# ============================================================================

# Run the script and follow the prompts:
# python Final_Model.py

# When asked: "Would you like to enter your own data? (yes/no):"
# Type: yes

# Then enter your values:
# Field Size (hectares): 2.5
# Crop Type: Wheat
# Soil Type: Loamy
# Sowing Date: 2025-11-15
# Nitrogen (mg/kg): 180
# Phosphorus (mg/kg): 25
# Potassium (mg/kg): 150
# Soil pH: 6.8
# Soil Moisture (%): 55
# Electrical Conductivity: 450
# Soil Temperature (°C): 28.5
# Use AI-Enhanced Recommendations? (yes/no): no


# ============================================================================
# OPTION 4: SAVE AND ANALYZE RESULTS
# ============================================================================

import json
from Final_Model import FinalFertilizerRecommendationSystem

system = FinalFertilizerRecommendationSystem()

recommendation = system.predict(
    size=2.5, crop='Wheat', soil='Loamy', sowing_date='2025-11-15',
    nitrogen=180.0, phosphorus=25.0, potassium=150.0, soil_ph=6.8,
    soil_moisture=55.0, electrical_conductivity=450.0, 
    soil_temperature=28.5, use_llm=False
)

# Save to file
with open('my_recommendation.json', 'w') as f:
    json.dump(recommendation, f, indent=2)

print("Saved to: my_recommendation.json")

# Access specific parts
ml_predictions = recommendation['ml_predictions']
cost_estimate = recommendation['cost_estimate']

print(f"\nYou need: {ml_predictions['Primary_Fertilizer']}")
print(f"Estimated cost: {cost_estimate['total_estimate']}")


# ============================================================================
# OPTION 5: BATCH PROCESSING
# ============================================================================

from Final_Model import FinalFertilizerRecommendationSystem
import pandas as pd

system = FinalFertilizerRecommendationSystem()

# Your multiple fields
fields = [
    {'name': 'Field 1', 'size': 2.5, 'crop': 'Wheat', 'nitrogen': 180, 'phosphorus': 25, 'potassium': 150},
    {'name': 'Field 2', 'size': 1.8, 'crop': 'Rice', 'nitrogen': 140, 'phosphorus': 18, 'potassium': 190},
    {'name': 'Field 3', 'size': 3.0, 'crop': 'Maize', 'nitrogen': 160, 'phosphorus': 22, 'potassium': 170}
]

results = []

for field in fields:
    rec = system.predict(
        size=field['size'],
        crop=field['crop'],
        soil='Loamy',
        sowing_date='2025-11-15',
        nitrogen=field['nitrogen'],
        phosphorus=field['phosphorus'],
        potassium=field['potassium'],
        soil_ph=6.8,
        soil_moisture=55.0,
        electrical_conductivity=450.0,
        soil_temperature=28.5,
        use_llm=False
    )
    
    results.append({
        'Field': field['name'],
        'Crop': field['crop'],
        'Primary_Fertilizer': rec['ml_predictions']['Primary_Fertilizer'],
        'Secondary_Fertilizer': rec['ml_predictions']['Secondary_Fertilizer'],
        'N_Status': rec['ml_predictions']['N_Status'],
        'P_Status': rec['ml_predictions']['P_Status'],
        'K_Status': rec['ml_predictions']['K_Status']
    })

# Create a summary table
df = pd.DataFrame(results)
print(df)
df.to_csv('batch_results.csv', index=False)


# ============================================================================
# WHAT YOU GET
# ============================================================================

"""
The system returns a dictionary with:

{
  "ml_predictions": {
    "N_Status": "Optimal" / "Low" / "High",
    "P_Status": "Optimal" / "Low" / "High",
    "K_Status": "Optimal" / "Low" / "High",
    "Primary_Fertilizer": "Urea" / "DAP" / "MOP" / etc,
    "Secondary_Fertilizer": "Zinc Sulphate" / "Ferrous Sulphate" / etc,
    "pH_Amendment": "Lime" / "Gypsum" / "None" / etc
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
  },
  
  "soil_condition_analysis": {
    "current_status": {...},
    "soil_test_values": {...},
    "recommendations": [...]
  },
  
  "primary_fertilizer": {...},
  "secondary_fertilizer": {...},
  "organic_alternatives": [...]
}
"""


# ============================================================================
# TROUBLESHOOTING
# ============================================================================

"""
Problem: "Model is not trained"
Solution: Make sure 'Primary and pH Dataset.csv' is in the same folder

Problem: "Module not found"
Solution: Install packages:
  pip install pandas numpy scikit-learn xgboost catboost lightgbm

Problem: "LLM API error"
Solution: Set use_llm=False to skip AI-enhanced mode
  OR create .env file with: GEMINI_API_KEY=your-key-here

Problem: Import errors
Solution: Make sure these files are in the same folder:
  - Final_Model.py
  - fertilizer_ml_model.py
  - secondary_fertilizer_model.py
  - LLM_model.py
  - Primary and pH Dataset.csv
"""


# ============================================================================
# WORKFLOW DIAGRAM
# ============================================================================

"""
INPUT (Your Data)
    ↓
    ├─→ Primary ML Model
    │   └─→ N_Status, P_Status, K_Status, Primary_Fertilizer, pH_Amendment
    │
    ├─→ Secondary Fertilizer Model
    │   └─→ Secondary_Fertilizer (micronutrients)
    │
    └─→ LLM Model (optional)
        └─→ Enhanced recommendations with timing, costs, organic alternatives
    
OUTPUT
    └─→ Complete recommendation report (JSON)
"""


# ============================================================================
# READY TO USE!
# ============================================================================

# Just copy one of the options above and run it!
# The simplest way:

if __name__ == "__main__":
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
        use_llm=False
    )
    
    print("\n✅ YOUR RECOMMENDATIONS:")
    print(f"Primary Fertilizer: {result['ml_predictions']['Primary_Fertilizer']}")
    print(f"Secondary Fertilizer: {result['ml_predictions']['Secondary_Fertilizer']}")
    print(f"N Status: {result['ml_predictions']['N_Status']}")
    print(f"P Status: {result['ml_predictions']['P_Status']}")
    print(f"K Status: {result['ml_predictions']['K_Status']}")
