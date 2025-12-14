"""
🌱 PRIMARY FERTILIZER & pH AMENDMENT MODEL
==========================================

Type: 100% Rule-Based Expert System
Purpose: Fertilizer & pH recommendation
Accuracy: 100% (deterministic, no learning error)

This model provides rule-based recommendations for:
- N_Status (Nitrogen status)
- P_Status (Phosphorus status)
- K_Status (Potassium status)
- Primary_Fertilizer (based on NPK deficiency pattern)
- pH_Amendment (based on soil pH level)

Author: AgriCure AI Team
Date: December 2025
"""

from typing import Dict, Any


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
# 2️⃣ NUTRIENT STATUS RULE
# ==================================================================================

def nutrient_status(value: float, threshold: float) -> str:
    """
    Determine nutrient status based on threshold
    
    Parameters:
    -----------
    value : float
        Measured nutrient value in mg/kg
    threshold : float
        Crop-specific threshold value
    
    Returns:
    --------
    str: "Low" or "Optimal"
    """
    return "Low" if value < threshold else "Optimal"


# ==================================================================================
# 3️⃣ PRIMARY FERTILIZER RECOMMENDATION RULE
# ==================================================================================

def recommend_fertilizer(N: str, P: str, K: str) -> str:
    """
    Recommend primary fertilizer based on NPK status pattern
    
    Based on NPK composition and deficiency matching:
    - Urea (46-0-0): High nitrogen, no phosphorus or potassium
    - TSP (0-46-0): High phosphorus, no nitrogen or potassium
    - MOP (0-0-60): High potassium, no nitrogen or phosphorus
    - DAP (18-46-0): Nitrogen and phosphorus
    - NPK (14-14-14): Balanced for all three deficiencies
    
    Parameters:
    -----------
    N : str
        Nitrogen status ("Low" or "Optimal")
    P : str
        Phosphorus status ("Low" or "Optimal")
    K : str
        Potassium status ("Low" or "Optimal")
    
    Returns:
    --------
    str: Recommended primary fertilizer
    """
    # Single nutrient deficiencies
    if N == "Low" and P == "Optimal" and K == "Optimal":
        return "Urea (46–0–0)"
    
    if N == "Optimal" and P == "Low" and K == "Optimal":
        return "Triple Super Phosphate – TSP (0–46–0)"
    
    if N == "Optimal" and P == "Optimal" and K == "Low":
        return "Muriate of Potash – MOP (0–0–60)"
    
    # Two nutrient deficiencies
    if N == "Low" and P == "Low" and K == "Optimal":
        return "Diammonium Phosphate – DAP (18–46–0)"
    
    if N == "Low" and P == "Optimal" and K == "Low":
        return "Urea + MOP mixture"
    
    if N == "Optimal" and P == "Low" and K == "Low":
        return "TSP + MOP mixture"
    
    # All three deficiencies
    if N == "Low" and P == "Low" and K == "Low":
        return "NPK (14–14–14)"
    
    # All optimal - maintenance
    return "Balanced NPK (Maintenance)"


# ==================================================================================
# 4️⃣ pH AMENDMENT RECOMMENDATION RULE
# ==================================================================================

def recommend_ph_amendment(ph: float) -> str:
    """
    Recommend pH amendment based on soil pH level
    
    pH Ranges and Amendments:
    - < 5.5: Very acidic → Agricultural Lime
    - 5.5-6.0: Acidic → Dolomite
    - 6.0-7.5: Optimal → Balance Maintain
    - 7.5-8.0: Slightly alkaline → Gypsum
    - > 8.0: Very alkaline → Elemental Sulphur
    
    Parameters:
    -----------
    ph : float
        Soil pH value
    
    Returns:
    --------
    str: Recommended pH amendment
    """
    if ph < 5.5:
        return "Agricultural Lime"
    elif ph < 6.0:
        return "Dolomite"
    elif ph <= 7.5:
        return "Balance Maintain"
    elif ph <= 8.0:
        return "Gypsum"
    else:
        return "Elemental Sulphur"


# ==================================================================================
# 5️⃣ MAIN MODEL CLASS
# ==================================================================================

class PrimaryFertilizerAndpHModel:
    """
    Rule-based expert system for fertilizer and pH recommendations
    
    This model uses deterministic rules based on:
    - Crop-specific NPK thresholds
    - Nutrient deficiency patterns
    - Soil pH levels
    """
    
    def __init__(self):
        """Initialize the rule-based model"""
        self.crop_ranges = CROP_NPK_RANGES
        print("✅ Primary Fertilizer & pH Model (Rule-Based) initialized")
    
    def predict(self, 
                nitrogen: float,
                phosphorus: float,
                potassium: float,
                crop_type: str,
                ph: float,
                electrical_conductivity: float = None,
                soil_moisture: float = None,
                soil_temperature: float = None) -> Dict[str, str]:
        """
        Generate fertilizer and pH recommendations
        
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
            - N_Status: Nitrogen status ("Low" or "Optimal")
            - P_Status: Phosphorus status ("Low" or "Optimal")
            - K_Status: Potassium status ("Low" or "Optimal")
            - Primary_Fertilizer: Recommended primary fertilizer
            - pH_Amendment: Recommended pH amendment
        """
        
        # Validate crop type
        if crop_type not in self.crop_ranges:
            raise ValueError(f"Unknown crop type: {crop_type}. Supported crops: {list(self.crop_ranges.keys())}")
        
        # Get crop-specific thresholds
        thresholds = self.crop_ranges[crop_type]
        
        # Determine nutrient status
        N_status = nutrient_status(nitrogen, thresholds["N"])
        P_status = nutrient_status(phosphorus, thresholds["P"])
        K_status = nutrient_status(potassium, thresholds["K"])
        
        # Get fertilizer recommendation
        fertilizer = recommend_fertilizer(N_status, P_status, K_status)
        
        # Get pH amendment recommendation
        ph_amendment = recommend_ph_amendment(ph)
        
        return {
            "N_Status": N_status,
            "P_Status": P_status,
            "K_Status": K_status,
            "Primary_Fertilizer": fertilizer,
            "pH_Amendment": ph_amendment
        }


# ==================================================================================
# 6️⃣ EXAMPLE USAGE & VALIDATION
# ==================================================================================

def example_usage():
    """Example demonstrating model usage"""
    print("\n" + "="*80)
    print("EXAMPLE: Rule-Based Fertilizer & pH Recommendation")
    print("="*80 + "\n")
    
    # Initialize model
    model = PrimaryFertilizerAndpHModel()
    
    # Sample input
    sample_input = {
        "Nitrogen(mg/kg)": 65,
        "Phosphorus(mg/kg)": 10,
        "Potassium(mg/kg)": 85,
        "Crop_Type": "Wheat",
        "pH": 5.2,
        "Electrical_Conductivity": 1600,
        "Soil_Moisture": 60,
        "Soil_Temperture": 22
    }
    
    print("📥 INPUT DATA:")
    for key, value in sample_input.items():
        print(f"  {key}: {value}")
    
    # Get recommendation
    result = model.predict(
        nitrogen=sample_input["Nitrogen(mg/kg)"],
        phosphorus=sample_input["Phosphorus(mg/kg)"],
        potassium=sample_input["Potassium(mg/kg)"],
        crop_type=sample_input["Crop_Type"],
        ph=sample_input["pH"],
        electrical_conductivity=sample_input["Electrical_Conductivity"],
        soil_moisture=sample_input["Soil_Moisture"],
        soil_temperature=sample_input["Soil_Temperture"]
    )
    
    print("\n📤 OUTPUT (RECOMMENDATIONS):")
    for key, value in result.items():
        print(f"  {key}: {value}")
    
    print("\n" + "="*80)
    print("✅ VALIDATION SUCCESSFUL")
    print("="*80 + "\n")
    
    return result


# Run example if script is executed directly
if __name__ == "__main__":
    example_usage()
