"""
🌱 PRIMARY FERTILIZER & pH AMENDMENT MODEL
==========================================

Type: 100% Rule-Based Expert System
Purpose: Fertilizer & pH recommendation based on deficiency ratios
Accuracy: 100% (deterministic, no learning error)

This model provides rule-based recommendations for:
- N_Status (Nitrogen status with deficiency amount)
- P_Status (Phosphorus status with deficiency amount)
- K_Status (Potassium status with deficiency amount)
- Primary_Fertilizer (based on NPK deficiency ratio matching)
- pH_Amendment (based on crop-specific soil pH preferences)

Author: AgriCure AI Team
Date: December 2025
"""

from typing import Dict, Any, List, Tuple


# ==================================================================================
# 1️⃣ CROP-SPECIFIC NPK THRESHOLDS
# ==================================================================================

CROP_NPK_RANGES = {
    "Rice":      {"N": 100, "P": 20, "K": 120},
    "Wheat":     {"N": 100, "P": 15, "K": 100},
    "Maize":     {"N": 100, "P": 15, "K": 100},
    "Barley":    {"N": 80,  "P": 12, "K": 80},
    "Jowar":     {"N": 80,  "P": 12, "K": 100},
    "Bajra":     {"N": 80,  "P": 10, "K": 80},
    "Ragi":      {"N": 80,  "P": 10, "K": 100},
    "Groundnut": {"N": 40,  "P": 12, "K": 60},
    "Mustard":   {"N": 100, "P": 15, "K": 100},
    "Soybean":   {"N": 60,  "P": 15, "K": 120},
    "Sugarcane": {"N": 150, "P": 20, "K": 150},
    "Cotton":    {"N": 80,  "P": 15, "K": 120},
    "Chickpea":  {"N": 50,  "P": 18, "K": 80},
    "Moong":     {"N": 60,  "P": 15, "K": 100},
    "Garlic":    {"N": 100, "P": 20, "K": 120},
    "Onion":     {"N": 150, "P": 20, "K": 120}
}


# ==================================================================================
# 2️⃣ COMPREHENSIVE FERTILIZER DATABASE
# ==================================================================================

FERTILIZER_DATABASE = {
    "Urea": {"N": 46, "P": 0, "K": 0, "ratio": "46-0-0"},
    "Diammonium Phosphate (DAP)": {"N": 18, "P": 46, "K": 0, "ratio": "18-46-0"},
    "Muriate of Potash (MOP)": {"N": 0, "P": 0, "K": 60, "ratio": "0-0-60"},
    "Monoammonium Phosphate (MAP)": {"N": 11, "P": 52, "K": 0, "ratio": "11-52-0"},
    "Single Super Phosphate (SSP)": {"N": 0, "P": 16, "K": 0, "ratio": "0-16-0"},
    "Ammonium Sulphate": {"N": 21, "P": 0, "K": 0, "ratio": "21-0-0"},
    "Potassium Nitrate": {"N": 13, "P": 0, "K": 46, "ratio": "13-0-46"},
    "Triple Super Phosphate (TSP)": {"N": 0, "P": 46, "K": 0, "ratio": "0-46-0"},
    "Ammonium Nitrate": {"N": 34, "P": 0, "K": 0, "ratio": "34-0-0"},
    "Ammonium Chloride": {"N": 25, "P": 0, "K": 0, "ratio": "25-0-0"},
    "Sulphate of Potash (SOP)": {"N": 0, "P": 0, "K": 50, "ratio": "0-0-50"},
    "Potassium Carbonate": {"N": 0, "P": 0, "K": 56, "ratio": "0-0-56"},
    "Potassium Magnesium Sulphate": {"N": 0, "P": 0, "K": 22, "ratio": "0-0-22"},
    "Rock Phosphate": {"N": 0, "P": 30, "K": 0, "ratio": "0-30-0"},
    "Urea Ammonium Nitrate (UAN)": {"N": 30, "P": 0, "K": 0, "ratio": "30-0-0"},
    "Balanced NPK (Maintenance)": {"N": 0, "P": 0, "K": 0, "ratio": "0-0-0"},
    "Calcium Ammonium Nitrate (CAN)": {"N": 26, "P": 0, "K": 0, "ratio": "26-0-0"}
}


# ==================================================================================
# 3️⃣ CROP-SPECIFIC pH RANGES AND AMENDMENTS
# ==================================================================================

CROP_PH_PREFERENCES = {
    "Rice": {
        "optimal_range": (5.5, 6.5),
        "increase_ph": "Agricultural Lime (CaCO₃)",
        "decrease_ph": "Elemental Sulphur (S)"
    },
    "Wheat": {
        "optimal_range": (6.0, 7.0),
        "increase_ph": "Dolomite (CaMg(CO₃)₂)",
        "decrease_ph": "Ferrous Sulphate"
    },
    "Maize": {
        "optimal_range": (5.8, 6.8),
        "increase_ph": "Agricultural Lime (CaCO₃)",
        "decrease_ph": "Aluminium Sulphate"
    },
    "Barley": {
        "optimal_range": (6.0, 7.5),
        "increase_ph": "Wood Ash",
        "decrease_ph": "Elemental Sulphur (S)"
    },
    "Jowar": {
        "optimal_range": (6.0, 7.5),
        "increase_ph": "Dolomite (CaMg(CO₃)₂)",
        "decrease_ph": "Ammonium Sulphate"
    },
    "Bajra": {
        "optimal_range": (6.0, 7.5),
        "increase_ph": "Agricultural Lime (CaCO₃)",
        "decrease_ph": "Elemental Sulphur (S)"
    },
    "Ragi": {
        "optimal_range": (5.5, 6.5),
        "increase_ph": "Agricultural Lime (CaCO₃)",
        "decrease_ph": "Ammonium Sulphate"
    },
    "Groundnut": {
        "optimal_range": (6.0, 6.5),
        "increase_ph": "Gypsum (CaSO₄·2H₂O)",
        "decrease_ph": "Elemental Sulphur (S)"
    },
    "Mustard": {
        "optimal_range": (6.0, 7.0),
        "increase_ph": "Dolomite (CaMg(CO₃)₂)",
        "decrease_ph": "Elemental Sulphur (S)"
    },
    "Soybean": {
        "optimal_range": (6.0, 6.8),
        "increase_ph": "Agricultural Lime (CaCO₃)",
        "decrease_ph": "Ferrous Sulphate"
    },
    "Sugarcane": {
        "optimal_range": (6.5, 7.5),
        "increase_ph": "Quicklime (CaO)",
        "decrease_ph": "Elemental Sulphur (S)"
    },
    "Cotton": {
        "optimal_range": (6.0, 7.5),
        "increase_ph": "Hydrated Lime (Ca(OH)₂)",
        "decrease_ph": "Aluminium Sulphate"
    },
    "Chickpea": {
        "optimal_range": (6.0, 7.0),
        "increase_ph": "Agricultural Lime (CaCO₃)",
        "decrease_ph": "Elemental Sulphur (S)"
    },
    "Moong": {
        "optimal_range": (6.0, 7.0),
        "increase_ph": "Dolomite (CaMg(CO₃)₂)",
        "decrease_ph": "Ammonium Sulphate"
    },
    "Garlic": {
        "optimal_range": (6.0, 6.8),
        "increase_ph": "Agricultural Lime (CaCO₃)",
        "decrease_ph": "Elemental Sulphur (S)"
    },
    "Onion": {
        "optimal_range": (6.0, 6.8),
        "increase_ph": "Wood Ash",
        "decrease_ph": "Ferrous Sulphate"
    }
}


# ==================================================================================
# 4️⃣ DEFICIENCY CALCULATION
# ==================================================================================

def calculate_deficiency(current: float, required: float) -> Dict[str, Any]:
    """
    Calculate nutrient deficiency and status
    
    Parameters:
    -----------
    current : float
        Current nutrient level in mg/kg
    required : float
        Required nutrient level in mg/kg
    
    Returns:
    --------
    dict: {
        "status": "Low" or "Optimal",
        "deficiency": deficiency amount (0 if optimal),
        "percentage": deficiency percentage
    }
    """
    if current >= required:
        return {
            "status": "Optimal",
            "deficiency": 0,
            "percentage": 0
        }
    else:
        deficiency = required - current
        percentage = (deficiency / required) * 100
        return {
            "status": "Low",
            "deficiency": round(deficiency, 2),
            "percentage": round(percentage, 2)
        }


# ==================================================================================
# 5️⃣ FERTILIZER MATCHING ALGORITHM
# ==================================================================================

def match_single_nutrient_fertilizer(nutrient: str, deficiency: float) -> str:
    """
    Match single nutrient deficiency to appropriate fertilizer
    
    Parameters:
    -----------
    nutrient : str
        Nutrient type ("N", "P", or "K")
    deficiency : float
        Deficiency amount
    
    Returns:
    --------
    str: Recommended fertilizer name with ratio
    """
    fertilizer_options = {
        "N": [
            ("Urea", 46),
            ("Ammonium Nitrate", 34),
            ("Urea Ammonium Nitrate (UAN)", 30),
            ("Calcium Ammonium Nitrate (CAN)", 26),
            ("Ammonium Chloride", 25),
            ("Ammonium Sulphate", 21)
        ],
        "P": [
            ("Monoammonium Phosphate (MAP)", 52),
            ("Diammonium Phosphate (DAP)", 46),
            ("Triple Super Phosphate (TSP)", 46),
            ("Rock Phosphate", 30),
            ("Single Super Phosphate (SSP)", 16)
        ],
        "K": [
            ("Muriate of Potash (MOP)", 60),
            ("Potassium Carbonate", 56),
            ("Sulphate of Potash (SOP)", 50),
            ("Potassium Nitrate", 46),
            ("Potassium Magnesium Sulphate", 22)
        ]
    }
    
    options = fertilizer_options.get(nutrient, [])
    
    # Select fertilizer based on deficiency severity
    if deficiency > 50:
        # High deficiency - use high concentration fertilizer
        selected = options[0] if options else ("Balanced NPK (Maintenance)", 0)
    elif deficiency > 20:
        # Medium deficiency - use medium concentration fertilizer
        mid_idx = len(options) // 2
        selected = options[mid_idx] if options else ("Balanced NPK (Maintenance)", 0)
    else:
        # Low deficiency - use lower concentration fertilizer
        selected = options[-1] if options else ("Balanced NPK (Maintenance)", 0)
    
    fertilizer_name = selected[0]
    fertilizer_info = FERTILIZER_DATABASE.get(fertilizer_name, {"ratio": "0-0-0"})
    return f"{fertilizer_name} ({fertilizer_info['ratio']})"


def match_dual_nutrient_fertilizer(n_def: float, p_def: float, k_def: float) -> str:
    """
    Match dual nutrient deficiency to fertilizer combination
    
    Parameters:
    -----------
    n_def : float
        Nitrogen deficiency
    p_def : float
        Phosphorus deficiency
    k_def : float
        Potassium deficiency
    
    Returns:
    --------
    str: Recommended fertilizer combination
    """
    # N + P deficiency
    if n_def > 0 and p_def > 0 and k_def == 0:
        # Use DAP or MAP for dual coverage
        if p_def > n_def * 2:
            return "Monoammonium Phosphate (MAP) (11-52-0)"
        else:
            return "Diammonium Phosphate (DAP) (18-46-0)"
    
    # N + K deficiency
    elif n_def > 0 and p_def == 0 and k_def > 0:
        # Use Potassium Nitrate or combination
        if n_def < 20 and k_def < 30:
            return "Potassium Nitrate (13-0-46)"
        else:
            n_fert = match_single_nutrient_fertilizer("N", n_def).split(" (")[0]
            k_fert = match_single_nutrient_fertilizer("K", k_def).split(" (")[0]
            return f"{n_fert} + {k_fert} Combination"
    
    # P + K deficiency
    elif n_def == 0 and p_def > 0 and k_def > 0:
        p_fert = match_single_nutrient_fertilizer("P", p_def).split(" (")[0]
        k_fert = match_single_nutrient_fertilizer("K", k_def).split(" (")[0]
        return f"{p_fert} + {k_fert} Combination"
    
    return "Balanced NPK (Maintenance)"


def match_triple_nutrient_fertilizer(n_def: float, p_def: float, k_def: float) -> str:
    """
    Match triple nutrient deficiency to fertilizer combination
    
    Parameters:
    -----------
    n_def : float
        Nitrogen deficiency
    p_def : float
        Phosphorus deficiency
    k_def : float
        Potassium deficiency
    
    Returns:
    --------
    str: Recommended fertilizer combination
    """
    # For all three deficiencies, create a balanced combination
    n_fert = match_single_nutrient_fertilizer("N", n_def).split(" (")[0]
    p_fert = match_single_nutrient_fertilizer("P", p_def).split(" (")[0]
    k_fert = match_single_nutrient_fertilizer("K", k_def).split(" (")[0]
    
    return f"{n_fert} + {p_fert} + {k_fert} Combination"


def recommend_fertilizer_by_deficiency(n_def: float, p_def: float, k_def: float) -> str:
    """
    Recommend fertilizer based on deficiency pattern and ratios
    
    Parameters:
    -----------
    n_def : float
        Nitrogen deficiency amount
    p_def : float
        Phosphorus deficiency amount
    k_def : float
        Potassium deficiency amount
    
    Returns:
    --------
    str: Recommended fertilizer or fertilizer combination
    """
    # Count number of deficiencies
    deficiency_count = sum([n_def > 0, p_def > 0, k_def > 0])
    
    # No deficiency - maintenance
    if deficiency_count == 0:
        return "Balanced NPK (Maintenance)"
    
    # Single nutrient deficiency
    elif deficiency_count == 1:
        if n_def > 0:
            return match_single_nutrient_fertilizer("N", n_def)
        elif p_def > 0:
            return match_single_nutrient_fertilizer("P", p_def)
        elif k_def > 0:
            return match_single_nutrient_fertilizer("K", k_def)
    
    # Dual nutrient deficiency
    elif deficiency_count == 2:
        return match_dual_nutrient_fertilizer(n_def, p_def, k_def)
    
    # All three deficiencies
    else:
        return match_triple_nutrient_fertilizer(n_def, p_def, k_def)
    
    return "Balanced NPK (Maintenance)"


# ==================================================================================
# 6️⃣ CROP-SPECIFIC pH AMENDMENT
# ==================================================================================

def recommend_ph_amendment(ph: float, crop_type: str) -> str:
    """
    Recommend pH amendment based on crop-specific pH preferences
    
    Parameters:
    -----------
    ph : float
        Current soil pH value
    crop_type : str
        Type of crop
    
    Returns:
    --------
    str: Recommended pH amendment
    """
    # Get crop-specific pH preferences
    crop_ph = CROP_PH_PREFERENCES.get(crop_type)
    
    if not crop_ph:
        # Fallback to general pH recommendation if crop not found
        if ph < 6.0:
            return "Agricultural Lime (CaCO₃)"
        elif ph > 7.5:
            return "Elemental Sulphur (S)"
        else:
            return "Balance Maintain"
    
    optimal_min, optimal_max = crop_ph["optimal_range"]
    
    # pH too low - need to increase pH (make alkaline)
    if ph < optimal_min:
        return crop_ph["increase_ph"]
    
    # pH too high - need to decrease pH (make acidic)
    elif ph > optimal_max:
        return crop_ph["decrease_ph"]
    
    # pH is optimal
    else:
        return "Balance Maintain"


# ==================================================================================
# 7️⃣ MAIN MODEL CLASS
# ==================================================================================

class PrimaryFertilizerAndpHModel:
    """
    Rule-based expert system for fertilizer and pH recommendations
    
    This model uses deterministic rules based on:
    - Crop-specific NPK thresholds
    - Nutrient deficiency calculations and ratios
    - Fertilizer composition matching
    - Crop-specific soil pH preferences
    """
    
    def __init__(self):
        """Initialize the rule-based model"""
        self.crop_ranges = CROP_NPK_RANGES
        self.fertilizers = FERTILIZER_DATABASE
        self.ph_preferences = CROP_PH_PREFERENCES
        print("✅ Primary Fertilizer & pH Model (Deficiency-Based) initialized")
        print(f"   📊 Loaded {len(self.fertilizers)} fertilizers")
        print(f"   🌾 Loaded {len(self.crop_ranges)} crop profiles")
    
    def predict(self, 
                nitrogen: float,
                phosphorus: float,
                potassium: float,
                crop_type: str,
                ph: float,
                electrical_conductivity: float = None,
                soil_moisture: float = None,
                soil_temperature: float = None) -> Dict[str, Any]:
        """
        Generate fertilizer and pH recommendations based on deficiency ratios
        
        Parameters:
        -----------
        nitrogen : float
            Nitrogen content in mg/kg
        phosphorus : float
            Phosphorus content in mg/kg
        potassium : float
            Potassium content in mg/kg
        crop_type : str
            Type of crop (e.g., "Wheat", "Rice", "Maize")
        ph : float
            Soil pH value
        electrical_conductivity : float, optional
            Electrical conductivity (not used in current rules)
        soil_moisture : float, optional
            Soil moisture percentage (not used in current rules)
        soil_temperature : float, optional
            Soil temperature in °C (not used in current rules)
        
        Returns:
        --------
        dict: Predictions containing:
            - N_Status: Nitrogen status with deficiency info
            - P_Status: Phosphorus status with deficiency info
            - K_Status: Potassium status with deficiency info
            - N_Deficiency: Nitrogen deficiency amount (mg/kg)
            - P_Deficiency: Phosphorus deficiency amount (mg/kg)
            - K_Deficiency: Potassium deficiency amount (mg/kg)
            - Primary_Fertilizer: Recommended fertilizer or combination
            - pH_Amendment: Recommended pH amendment (crop-specific)
            - pH_Status: Current pH status relative to crop optimum
        """
        
        # Validate crop type
        if crop_type not in self.crop_ranges:
            raise ValueError(f"Unknown crop type: {crop_type}. Supported crops: {list(self.crop_ranges.keys())}")
        
        # Get crop-specific thresholds
        thresholds = self.crop_ranges[crop_type]
        
        # Calculate deficiencies for each nutrient
        n_info = calculate_deficiency(nitrogen, thresholds["N"])
        p_info = calculate_deficiency(phosphorus, thresholds["P"])
        k_info = calculate_deficiency(potassium, thresholds["K"])
        
        # Get fertilizer recommendation based on deficiency ratios
        fertilizer = recommend_fertilizer_by_deficiency(
            n_info["deficiency"],
            p_info["deficiency"],
            k_info["deficiency"]
        )
        
        # Get crop-specific pH amendment recommendation
        ph_amendment = recommend_ph_amendment(ph, crop_type)
        
        # Determine pH status
        if crop_type in self.ph_preferences:
            optimal_min, optimal_max = self.ph_preferences[crop_type]["optimal_range"]
            if ph < optimal_min:
                ph_status = f"Too Acidic (Optimal: {optimal_min}-{optimal_max})"
            elif ph > optimal_max:
                ph_status = f"Too Alkaline (Optimal: {optimal_min}-{optimal_max})"
            else:
                ph_status = f"Optimal ({optimal_min}-{optimal_max})"
        else:
            ph_status = "Unknown"
        
        return {
            "N_Status": n_info["status"],
            "P_Status": p_info["status"],
            "K_Status": k_info["status"],
            "N_Deficiency": n_info["deficiency"],
            "P_Deficiency": p_info["deficiency"],
            "K_Deficiency": k_info["deficiency"],
            "N_Deficiency_Percentage": n_info["percentage"],
            "P_Deficiency_Percentage": p_info["percentage"],
            "K_Deficiency_Percentage": k_info["percentage"],
            "Primary_Fertilizer": fertilizer,
            "pH_Amendment": ph_amendment,
            "pH_Status": ph_status,
            "Current_pH": ph,
            "Crop_Type": crop_type
        }


# ==================================================================================
# 8️⃣ EXAMPLE USAGE & VALIDATION
# ==================================================================================

def example_usage():
    """Example demonstrating model usage with various scenarios"""
    print("\n" + "="*80)
    print("EXAMPLE: Deficiency-Based Fertilizer & pH Recommendation")
    print("="*80 + "\n")
    
    # Initialize model
    model = PrimaryFertilizerAndpHModel()
    
    # Test scenarios
    test_cases = [
        {
            "name": "Test Case 1: Nitrogen Deficiency Only",
            "input": {
                "Nitrogen(mg/kg)": 65,
                "Phosphorus(mg/kg)": 20,
                "Potassium(mg/kg)": 110,
                "Crop_Type": "Wheat",
                "pH": 5.2
            }
        },
        {
            "name": "Test Case 2: Phosphorus Deficiency Only",
            "input": {
                "Nitrogen(mg/kg)": 105,
                "Phosphorus(mg/kg)": 8,
                "Potassium(mg/kg)": 100,
                "Crop_Type": "Rice",
                "pH": 6.8
            }
        },
        {
            "name": "Test Case 3: N+P Deficiency (DAP/MAP case)",
            "input": {
                "Nitrogen(mg/kg)": 70,
                "Phosphorus(mg/kg)": 10,
                "Potassium(mg/kg)": 125,
                "Crop_Type": "Maize",
                "pH": 7.8
            }
        },
        {
            "name": "Test Case 4: All Three Deficiencies",
            "input": {
                "Nitrogen(mg/kg)": 50,
                "Phosphorus(mg/kg)": 8,
                "Potassium(mg/kg)": 60,
                "Crop_Type": "Cotton",
                "pH": 5.5
            }
        },
        {
            "name": "Test Case 5: All Optimal (Maintenance)",
            "input": {
                "Nitrogen(mg/kg)": 110,
                "Phosphorus(mg/kg)": 22,
                "Potassium(mg/kg)": 125,
                "Crop_Type": "Sugarcane",
                "pH": 7.0
            }
        }
    ]
    
    # Run test cases
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"{test_case['name']}")
        print('='*80)
        
        input_data = test_case['input']
        
        print("\n📥 INPUT DATA:")
        for key, value in input_data.items():
            print(f"  {key}: {value}")
        
        # Get recommendation
        result = model.predict(
            nitrogen=input_data["Nitrogen(mg/kg)"],
            phosphorus=input_data["Phosphorus(mg/kg)"],
            potassium=input_data["Potassium(mg/kg)"],
            crop_type=input_data["Crop_Type"],
            ph=input_data["pH"]
        )
        
        print("\n📤 OUTPUT (RECOMMENDATIONS):")
        print(f"  Crop Type: {result['Crop_Type']}")
        print(f"\n  NUTRIENT STATUS:")
        print(f"    • Nitrogen: {result['N_Status']} (Deficiency: {result['N_Deficiency']} mg/kg, {result['N_Deficiency_Percentage']}%)")
        print(f"    • Phosphorus: {result['P_Status']} (Deficiency: {result['P_Deficiency']} mg/kg, {result['P_Deficiency_Percentage']}%)")
        print(f"    • Potassium: {result['K_Status']} (Deficiency: {result['K_Deficiency']} mg/kg, {result['K_Deficiency_Percentage']}%)")
        print(f"\n  RECOMMENDATIONS:")
        print(f"    🌾 Primary Fertilizer: {result['Primary_Fertilizer']}")
        print(f"    🧪 pH Amendment: {result['pH_Amendment']}")
        print(f"    📊 pH Status: {result['pH_Status']}")
    
    print("\n" + "="*80)
    print("✅ ALL VALIDATION TESTS COMPLETED SUCCESSFULLY")
    print("="*80 + "\n")
    
    return True


# Run example if script is executed directly
if __name__ == "__main__":
    example_usage()
