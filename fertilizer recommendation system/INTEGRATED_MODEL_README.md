# Integrated AgriCure Model

## Overview

The **Integrated AgriCure Model** is a unified, rule-based fertilizer recommendation system that provides:

- Primary fertilizer recommendations (NPK)
- Secondary fertilizer recommendations (micronutrients)
- pH amendment recommendations

## Features

### 🌾 Crop Support

Supports 16 major crops with specific NPK requirements:

- **Cereals**: Rice, Wheat, Maize, Barley, Jowar, Bajra, Ragi
- **Pulses**: Chickpea, Moong, Soybean
- **Cash Crops**: Cotton, Sugarcane, Mustard, Groundnut
- **Vegetables**: Onion, Garlic

### 🧪 Smart Recommendations

#### Primary Fertilizers

- **Single Deficiency**: Targeted fertilizer (Urea, TSP, SSP, MOP, CAN)
- **Dual Deficiency**: Combination fertilizers (DAP, Urea+MOP, TSP+MOP)
- **Triple Deficiency**: Optimized mix based on:
  - Deficit severity
  - Soil pH
  - Crop sensitivity to chloride

#### Secondary Fertilizers (Micronutrients)

- **Zinc Sulphate** - For Zn deficiency
- **Ferrous Sulphate** - For Fe deficiency
- **Borax** - For B deficiency
- **Manganese Sulphate** - For Mn deficiency
- **Copper Sulphate** - For Cu deficiency
- **Ammonium Molybdate** - For Mo deficiency
- **Calcium Chloride** - For Ca deficiency

**Intelligent Detection Based On:**

- High pH (>7.5) → Zn, Fe, Mn deficiency
- Low pH (<5.5) → Mo, Ca deficiency
- Low EC (<200) → Zn, Fe deficiency
- Low moisture (<15%) → B deficiency
- Crop-specific requirements

#### pH Amendments

| pH Range  | Amendment             |
| --------- | --------------------- |
| < 5.5     | Agricultural Lime     |
| 5.5 - 6.0 | Dolomite              |
| 6.0 - 7.5 | No amendment required |
| 7.5 - 8.0 | Gypsum                |
| > 8.0     | Elemental Sulphur     |

## Usage

### Basic Usage

```python
from integrated_agricure_model import IntegratedAgriCure

# Create engine instance
engine = IntegratedAgriCure()

# Get recommendation
result = engine.recommend(
    nitrogen=65.0,          # Measured N (mg/kg)
    phosphorus=10.0,        # Measured P (mg/kg)
    potassium=75.0,         # Measured K (mg/kg)
    crop_type="Wheat",      # Crop name
    ph=5.8,                 # Soil pH
    ec=250.0,               # Electrical conductivity (µS/cm)
    moisture=20.0           # Soil moisture (%)
)

# Access recommendations
print(f"Primary: {result['Primary_Fertilizer']}")
print(f"Secondary: {result['Secondary_Fertilizer']}")
print(f"pH Amendment: {result['pH_Amendment']}")
```

### Input Parameters

| Parameter            | Type  | Description                          | Example |
| -------------------- | ----- | ------------------------------------ | ------- |
| `nitrogen`           | float | Measured nitrogen (mg/kg)            | 65.0    |
| `phosphorus`         | float | Measured phosphorus (mg/kg)          | 10.0    |
| `potassium`          | float | Measured potassium (mg/kg)           | 75.0    |
| `crop_type`          | str   | Crop name (title case)               | "Wheat" |
| `ph`                 | float | Soil pH (0-14)                       | 5.8     |
| `ec`                 | float | Electrical conductivity (µS/cm)      | 250.0   |
| `moisture`           | float | Soil moisture (%)                    | 20.0    |
| `chloride_sensitive` | bool  | (Optional) Crop chloride sensitivity | False   |

### Output Format

```python
{
    "Crop": "Wheat",
    "N_Status": "Moderate",      # Optimal, Mild, Moderate, Severe
    "P_Status": "Severe",
    "K_Status": "Mild",
    "Primary_Fertilizer": "SSP (0-16-0) + Urea (46-0-0) + MOP (0-0-60)",
    "Secondary_Fertilizer": "Zinc Sulphate + Ferrous Sulphate",
    "pH_Amendment": "Dolomite",
    "Deficit_%": {
        "N": 35.0,
        "P": 33.33,
        "K": 25.0
    }
}
```

## Testing

### Run Core Model Tests

```bash
cd "Model Backend/fertilizer recommendation system"
python test_integrated_model.py
```

### Run Integration Tests

```bash
cd "Model Backend"
python test_integrated_system.py
```

### Test the Final Model

```bash
cd "Model Backend/fertilizer recommendation system"
python Final_Model.py
```

## Examples

### Example 1: Severe Deficiency

```python
result = engine.recommend(
    nitrogen=55,
    phosphorus=8,
    potassium=70,
    crop_type="Wheat",
    ph=5.3,
    ec=180,
    moisture=14
)
# Output:
# Primary: SSP (0-16-0) + Urea (46-0-0) + MOP (0-0-60)
# Secondary: Borax + Ferrous Sulphate + Ammonium Molybdate + Zinc Sulphate
# pH Amendment: Agricultural Lime
```

### Example 2: Optimal Conditions

```python
result = engine.recommend(
    nitrogen=100,
    phosphorus=20,
    potassium=120,
    crop_type="Rice",
    ph=6.5,
    ec=500,
    moisture=25
)
# Output:
# Primary: Urea (46-0-0) + DAP (18-46-0) + MOP (0-0-60)
# Secondary: No Secondary Fertilizer Required
# pH Amendment: No amendment required
```

### Example 3: Alkaline Soil

```python
result = engine.recommend(
    nitrogen=80,
    phosphorus=12,
    potassium=90,
    crop_type="Maize",
    ph=8.2,
    ec=150,
    moisture=18
)
# Output:
# Primary: Urea (46-0-0) + DAP (18-46-0) + MOP (0-0-60)
# Secondary: Ferrous Sulphate + Manganese Sulphate + Zinc Sulphate
# pH Amendment: Elemental Sulphur
```

## Architecture

```
IntegratedAgriCure
├── CROP_NPK              # Crop-specific NPK requirements
├── MICRO_FERT            # Micronutrient → Fertilizer mapping
├── CROP_MICRO_NEEDS      # Crop-specific micronutrient needs
├── deficit_pct()         # Calculate deficit percentage
├── severity()            # Determine severity level
├── ph_amendment()        # pH amendment logic
├── recommend_primary()   # Primary fertilizer logic
├── recommend_secondary() # Secondary fertilizer logic
└── recommend()           # Main recommendation engine
```

## Integration with Final_Model.py

The integrated model is automatically used by `Final_Model.py`:

```python
from integrated_agricure_model import IntegratedAgriCure
from Final_Model import FinalFertilizerRecommendationSystem

# This automatically uses the integrated model
system = FinalFertilizerRecommendationSystem()

# Make recommendations
result = system.predict(
    size=2.5,
    crop="Wheat",
    sowing_date="2025-11-15",
    nitrogen=65.0,
    phosphorus=10.0,
    potassium=75.0,
    soil_ph=5.8,
    soil_moisture=20.0,
    electrical_conductivity=250.0,
    soil_temperature=25.0
)
```

## Advantages

✅ **Single Source of Truth** - All logic in one place  
✅ **Deterministic** - Consistent, rule-based outcomes  
✅ **Crop-Aware** - Considers crop-specific requirements  
✅ **Condition-Aware** - pH, EC, moisture-sensitive  
✅ **Maintainable** - Easy to update and debug  
✅ **Well-Tested** - Comprehensive test coverage  
✅ **No Redundancy** - Eliminates duplicate code

## Crop NPK Requirements

| Crop      | N (mg/kg) | P (mg/kg) | K (mg/kg) |
| --------- | --------- | --------- | --------- |
| Rice      | 100       | 20        | 120       |
| Wheat     | 100       | 15        | 100       |
| Maize     | 100       | 15        | 100       |
| Barley    | 80        | 12        | 80        |
| Jowar     | 80        | 12        | 100       |
| Bajra     | 80        | 10        | 80        |
| Ragi      | 80        | 10        | 100       |
| Groundnut | 40        | 12        | 60        |
| Mustard   | 100       | 15        | 100       |
| Soybean   | 60        | 15        | 120       |
| Sugarcane | 150       | 20        | 150       |
| Cotton    | 80        | 15        | 120       |
| Chickpea  | 50        | 18        | 80        |
| Moong     | 60        | 15        | 100       |
| Garlic    | 100       | 20        | 120       |
| Onion     | 150       | 20        | 120       |

## License

Part of the AgriCure Fertilizer Recommendation System

---

**Version**: 1.0.0  
**Date**: December 2025  
**Status**: Production Ready
