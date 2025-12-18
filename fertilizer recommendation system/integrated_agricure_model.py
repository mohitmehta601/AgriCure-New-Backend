"""
INTEGRATED AGRICURE MODEL
=========================
Unified fertilizer recommendation system for primary, secondary, and pH amendment predictions.
This replaces the older separate models with a single, consolidated engine.

Author: AgriCure AI Team
Date: December 2025
"""

from typing import Dict

# =========================================================
# 1. CROP IDEAL NPK REQUIREMENTS (mg/kg)
# =========================================================

CROP_NPK = {
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
    "Onion":     {"N": 150, "P": 20, "K": 120},
}

# =========================================================
# 2. MICRONUTRIENT → FERTILIZER MAP
# =========================================================

MICRO_FERT = {
    "Zn": "Zinc Sulphate",
    "Fe": "Ferrous Sulphate",
    "B":  "Borax",
    "Mn": "Manganese Sulphate",
    "Cu": "Copper Sulphate",
    "Mo": "Ammonium Molybdate",
    "Ca": "Calcium Chloride",
}

CROP_MICRO_NEEDS = {
    "Wheat": ["Zn","Fe","Mn","Cu","B","Mo"],
    "Rice": ["Zn","Fe","Mn","Cu","B","Mo"],
    "Maize": ["Zn","Fe","Mn","Cu","B","Mo"],
    "Groundnut": ["Ca","B","Mn","Fe","Zn","Mo"],
    "Onion": ["Zn","B","Mn","Fe","Cu","Mo"],
    "Mustard": ["B","Mo","Mn","Zn","Fe"],
}

# =========================================================
# 3. CORE UTILITIES (SINGLE SOURCE)
# =========================================================

def deficit_pct(measured: float, required: float) -> float:
    """Calculate deficit percentage"""
    return max(0.0, (required - measured) / required * 100)

def severity(pct: float) -> str:
    """Determine severity level from deficit percentage"""
    if pct == 0: return "Optimal"
    if pct < 20: return "Mild"
    if pct < 40: return "Moderate"
    return "Severe"

def ph_amendment(ph: float) -> str:
    """Determine pH amendment based on pH level"""
    if ph < 5.5: return "Agricultural Lime"
    if ph < 6.0: return "Dolomite"
    if ph <= 7.5: return "No amendment required"
    if ph <= 8.0: return "Gypsum"
    return "Elemental Sulphur"

# =========================================================
# 4. PRIMARY FERTILIZER LOGIC (NO REDUNDANCY)
# =========================================================

def recommend_primary(Nd, Pd, Kd, Ns, Ps, Ks, ph, chloride_sensitive=False):
    """
    Recommend primary fertilizer based on NPK deficits and severities
    
    Parameters:
    -----------
    Nd, Pd, Kd : float
        Deficit percentages for N, P, K
    Ns, Ps, Ks : str
        Severity levels for N, P, K
    ph : float
        Soil pH level
    chloride_sensitive : bool
        Whether crop is sensitive to chloride
    
    Returns:
    --------
    str: Recommended primary fertilizer
    """
    low = [n for n, s in zip(["N","P","K"], [Ns, Ps, Ks]) if s != "Optimal"]

    # ---- SINGLE DEFICIENCY ----
    if len(low) == 1:
        return {
            "N": "Urea (46-0-0)" if Ns == "Severe" else "CAN (26-0-0)",
            "P": "TSP (0-46-0)" if Ps == "Severe" else "SSP (0-16-0)",
            "K": "MOP (0-0-60)"
        }[low[0]]

    # ---- TWO DEFICIENCIES ----
    if len(low) == 2:
        pair = set(low)
        if pair == {"N","P"}: return "DAP (18-46-0)"
        if pair == {"N","K"}: return "Urea (46-0-0) + MOP (0-0-60)"
        if pair == {"P","K"}: return "TSP (0-46-0) + MOP (0-0-60)"

    # ---- THREE DEFICIENCIES (CALCULATED MIX) ----
    if Nd >= Pd and Nd >= Kd:
        return "Urea (46-0-0) + DAP (18-46-0) + MOP (0-0-60)"
    if Pd >= Nd and Pd >= Kd:
        return "SSP (0-16-0) + Urea (46-0-0) + MOP (0-0-60)" if ph < 6 \
               else "TSP (0-46-0) + Urea (46-0-0) + MOP (0-0-60)"
    if chloride_sensitive:
        return "SOP (0-0-50) + Urea (46-0-0) + DAP (18-46-0)"

    return "MOP (0-0-60) + Urea (46-0-0) + DAP (18-46-0)"

# =========================================================
# 5. SECONDARY (MICRONUTRIENT) LOGIC
# =========================================================

def recommend_secondary(ph, ec, moisture, crop):
    """
    Recommend secondary fertilizer based on soil conditions
    
    Parameters:
    -----------
    ph : float
        Soil pH
    ec : float
        Electrical conductivity
    moisture : float
        Soil moisture percentage
    crop : str
        Crop type
    
    Returns:
    --------
    str: Recommended secondary fertilizer
    """
    deficient = set()

    if ph > 7.5: deficient.update(["Zn","Fe","Mn"])
    if ph < 5.5: deficient.update(["Mo","Ca"])
    if ec < 200: deficient.update(["Zn","Fe"])
    if moisture < 15: deficient.add("B")

    crop = crop.title()
    if crop in CROP_MICRO_NEEDS:
        deficient &= set(CROP_MICRO_NEEDS[crop])

    if not deficient:
        return "No Secondary Fertilizer Required"

    return " + ".join(MICRO_FERT[x] for x in sorted(deficient))

# =========================================================
# 6. FINAL ENGINE (SINGLE FLOW)
# =========================================================

class IntegratedAgriCure:
    """
    Integrated AgriCure Fertilizer Recommendation Engine
    
    This class provides a unified interface for:
    - Primary fertilizer recommendations
    - Secondary fertilizer recommendations
    - pH amendment recommendations
    """

    def recommend(self,
                  nitrogen: float,
                  phosphorus: float,
                  potassium: float,
                  crop_type: str,
                  ph: float,
                  ec: float,
                  moisture: float,
                  chloride_sensitive: bool = False) -> Dict:
        """
        Generate complete fertilizer recommendation
        
        Parameters:
        -----------
        nitrogen : float
            Measured nitrogen content (mg/kg)
        phosphorus : float
            Measured phosphorus content (mg/kg)
        potassium : float
            Measured potassium content (mg/kg)
        crop_type : str
            Type of crop being grown
        ph : float
            Soil pH level
        ec : float
            Electrical conductivity (µS/cm)
        moisture : float
            Soil moisture percentage
        chloride_sensitive : bool
            Whether crop is sensitive to chloride (default: False)
        
        Returns:
        --------
        dict: Complete recommendation including:
            - Crop
            - N_Status, P_Status, K_Status
            - Primary_Fertilizer
            - Secondary_Fertilizer
            - pH_Amendment
            - Deficit_% (N, P, K)
        """
        crop = crop_type.title()
        if crop not in CROP_NPK:
            raise ValueError(f"Unsupported crop: {crop}")

        req = CROP_NPK[crop]

        Nd = deficit_pct(nitrogen, req["N"])
        Pd = deficit_pct(phosphorus, req["P"])
        Kd = deficit_pct(potassium, req["K"])

        Ns, Ps, Ks = severity(Nd), severity(Pd), severity(Kd)

        return {
            "Crop": crop,
            "N_Status": Ns,
            "P_Status": Ps,
            "K_Status": Ks,
            "Primary_Fertilizer": recommend_primary(Nd, Pd, Kd, Ns, Ps, Ks, ph, chloride_sensitive),
            "Secondary_Fertilizer": recommend_secondary(ph, ec, moisture, crop),
            "pH_Amendment": ph_amendment(ph),
            "Deficit_%": {
                "N": round(Nd, 2),
                "P": round(Pd, 2),
                "K": round(Kd, 2)
            }
        }

# =========================================================
# 7. EXAMPLE USAGE
# =========================================================

if __name__ == "__main__":
    engine = IntegratedAgriCure()

    result = engine.recommend(
        nitrogen=55,
        phosphorus=8,
        potassium=70,
        crop_type="Wheat",
        ph=5.3,
        ec=180,
        moisture=14
    )

    print("\n" + "="*60)
    print("INTEGRATED AGRICURE RECOMMENDATION")
    print("="*60)
    for k, v in result.items():
        print(f"{k}: {v}")
    print("="*60)
