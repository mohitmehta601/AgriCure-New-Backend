"""
Enhanced LLM-Based Fertilizer Recommendation System
====================================================

This module uses Google Gemini API to generate comprehensive fertilizer recommendations
including:
- Primary and Secondary fertilizers with detailed application methods
- Organic alternatives from predefined list
- Application timing based on crop sowing date
- Cost analysis with field size considerations
- Soil condition analysis
- NPK values in mg/kg units

Author: AgriCure AI Team
Date: November 2025
"""

import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file automatically
except ImportError:
    print("Warning: python-dotenv not available. Install with: pip install python-dotenv")

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    print("Warning: google-generativeai not available. Install with: pip install google-generativeai")
    GEMINI_AVAILABLE = False


# ==================================================================================
# ORGANIC ALTERNATIVES - Predefined List
# ==================================================================================
ORGANIC_ALTERNATIVES = [
    "Mulch",
    "Vermicompost",
    "Mustard cake",
    "Bone meal",
    "Compost",
    "Poultry manure",
    "Neem cake",
    "Banana wastes",
    "Azolla",
    "PSB (Phosphate Solubilizing Bacteria)",
    "Rhizobium biofertilizer",
    "Green manure",
    "Farmyard manure (FYM)",
    "Seaweed extract",
    "Fish emulsion",
    "Cow dung slurry",
    "Bio-slurry",
    "Trichoderma compost",
    "Beejamrit",
    "Panchagavya",
    "Jeevamrut"
]


# ==================================================================================
# PRICE TABLE - Default Prices (₹/kg)
# ==================================================================================
DEFAULT_PRICES = {
    # -------------------------------
    # 🌾 PRIMARY FERTILIZERS (Chemical)
    # -------------------------------
    'avoid_n': 0,  # advisory
    'rock_phosphate': 15,
    'calcium_ammonium_nitrate': 26,  # ₹1300–1350 per 50kg
    'stop_k': 0,  # advisory
    'monoammonium_phosphate_map': 18,  # ₹900 per 50kg
    'urea': 5.4,  # ₹242 per 45kg (govt subsidized)
    'ammonium_chloride': 20,
    'stop_p': 0,
    'ammonium_sulphate': 25,
    'split_n_doses': 0,
    'reduce_n': 0,
    'single_super_phosphate_ssp': 7.2,  # ₹362 per 50kg
    'avoid_potash': 0,
    'avoid_phosphate_application': 0,
    'diammonium_phosphate_dap': 27,  # ₹1350 per 50kg
    'ammonium_nitrate': 27,
    'sulphate_of_potash_sop': 30,
    'urea_ammonium_nitrate_uan': 26,
    'calcium_ammonium_nitrate_can': 26,
    'muriate_of_potash_mop': 34,
    'balanced_npk_maintenance': 32,
    'triple_super_phosphate_tsp': 30,

    # -------------------------------
    # 🧪 SECONDARY FERTILIZERS (Micronutrients / Blends)
    # -------------------------------
    'ammonium_molybdate_zinc_sulphate_mixture': 70,
    'borax_elemental_sulphur_mixture': 50,
    'borax_ammonium_molybdate_mixture': 75,
    'borax_zinc_sulphate_mixture': 55,
    'ferrous_sulphate_zinc_sulphate_mixture': 40,
    'ferrous_sulphate_manganese_sulphate_mixture': 42,
    'zinc_sulphate': 58,
    'manganese_sulphate': 52,
    'zinc_sulphate_borax_mixture': 50,
    'rhizobium_biofertilizer_zinc_sulphate_mixture': 85,
    'magnesium_sulphate_zinc_sulphate_mixture': 65,
    'magnesium_sulphate': 45,
    'ferrous_sulphate': 28,
    'gypsum_borax_mixture': 25,
    'zinc_sulphate_manganese_sulphate_mixture': 48,

    # -------------------------------
    # 🌿 ORGANIC & BIO-BASED ALTERNATIVES
    # -------------------------------
    'mulch': 3,  # natural residue or straw mulch cost/kg eq.
    'vermicompost': 8,  # ₹400 per 50kg bag
    'mustard_cake': 12,  # ₹600 per 50kg
    'bone_meal': 30,  # ₹1500 per 50kg
    'compost': 6,  # ₹300 per 50kg
    'poultry_manure': 5,  # ₹250 per 50kg
    'neem_cake': 25,  # ₹1250 per 50kg
    'banana_wastes': 2,  # raw organic residue cost
    'azolla': 10,  # ₹200 per 20kg fresh
    'psb_phosphate_solubilizing_bacteria': 130,  # biofertilizer liquid ₹130/litre
    'rhizobium_biofertilizer': 150,  # ₹150 per litre (liquid form)
    'green_manure': 5,  # field-grown organic source
    'farmyard_manure_fym': 4,  # ₹200 per 50kg
    'seaweed_extract': 180,  # ₹900 per 5L bottle
    'fish_emulsion': 160,  # ₹800 per 5L
    'cow_dung_slurry': 3,
    'bio_slurry': 4,
    'trichoderma_compost': 60,  # ₹1200 per 20kg
    'beejamrit': 25,
    'panchagavya': 50,  # ₹250 per 5L
    'jeevamrut': 20,  # ₹100 per 5L
    
    # Legacy aliases for backward compatibility
    'dap': 27,  # alias for diammonium_phosphate_dap
    'mop': 34,  # alias for muriate_of_potash_mop
    'ssp': 7.2,  # alias for single_super_phosphate_ssp
    'rhizobium': 150,  # alias for rhizobium_biofertilizer
    'cow_manure': 4,  # alias for farmyard_manure_fym
    'gypsum': 10,
    'lime': 8,
    'sulphur': 20,
    'azospirillum': 140,
    'azotobacter': 145,
    'phosphate_solubilizing_bacteria': 130
}


# ==================================================================================
# DATA CLASSES
# ==================================================================================
@dataclass
class MLPrediction:
    """ML Model predictions"""
    n_status: str
    p_status: str
    k_status: str
    primary_fertilizer: str
    secondary_fertilizer: str
    ph_amendment: str


@dataclass
class InputData:
    """User input data"""
    temperature: float
    humidity: float
    moisture: float
    soil_type: str
    crop: str
    nitrogen: float  # mg/kg
    phosphorus: float  # mg/kg
    potassium: float  # mg/kg
    ph: float
    ec: float  # mmhos/cm2
    sowing_date: str  # ISO format YYYY-MM-DD
    field_size: float  # in hectares


# ==================================================================================
# GEMINI API CONFIGURATION
# ==================================================================================
def configure_gemini_api():
    """Configure Gemini API with API key from environment or .env file"""
    if not GEMINI_AVAILABLE:
        raise RuntimeError("google-generativeai package not installed")
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY not found. Please set it in one of these ways:\n"
            "  1. Create a .env file with: GEMINI_API_KEY=your-key-here\n"
            "  2. Set environment variable: $env:GEMINI_API_KEY='your-key-here' (Windows)\n"
            "  3. Set environment variable: export GEMINI_API_KEY='your-key-here' (Linux/Mac)"
        )
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')


# ==================================================================================
# UTILITY FUNCTIONS
# ==================================================================================
def normalize_fertilizer_name(name: str) -> str:
    """Normalize fertilizer name for price lookup"""
    if not name or name in ['—', 'None', 'NA']:
        return None
    
    # Convert to lowercase and replace spaces with underscores
    normalized = name.lower().replace(' ', '_').replace('(', '').replace(')', '')
    
 # 🧭 Handle common fertilizer name variations and abbreviations
    variations = {
    # -------------------------------
    # 🌾 Chemical Fertilizers (Primary)
    # -------------------------------
    'dap': 'diammonium_phosphate_dap',
    'map': 'monoammonium_phosphate_map',
    'mop': 'muriate_of_potash_mop',
    'sop': 'sulphate_of_potash_sop',
    'ssp': 'single_super_phosphate_ssp',
    'tsp': 'triple_super_phosphate_tsp',
    'can': 'calcium_ammonium_nitrate_can',
    'uan': 'urea_ammonium_nitrate_uan',
    'as': 'ammonium_sulphate',
    'an': 'ammonium_nitrate',
    'urea46': 'urea',
    'rockp': 'rock_phosphate',
    'npk': 'balanced_npk_maintenance',

    # -------------------------------
    # 🧪 Secondary & Micronutrients
    # -------------------------------
    'znso4': 'zinc_sulphate',
    'fes': 'ferrous_sulphate',
    'mns': 'manganese_sulphate',
    'mgs': 'magnesium_sulphate',
    'gypsum': 'gypsum_borax_mixture',  # sometimes referred collectively
    'boraxmix': 'borax_zinc_sulphate_mixture',

    # -------------------------------
    # 🌿 Organic & Natural Inputs
    # -------------------------------
    'fym': 'farmyard_manure_fym',
    'vermi': 'vermicompost',
    'compost': 'compost',
    'neem': 'neem_cake',
    'mustard': 'mustard_cake',
    'bonemeal': 'bone_meal',
    'poultry': 'poultry_manure',
    'green': 'green_manure',
    'mulch': 'mulch',
    'banana': 'banana_wastes',
    'azolla': 'azolla',

    # -------------------------------
    # 🧫 Biofertilizers / Microbial
    # -------------------------------
    'psb': 'psb_phosphate_solubilizing_bacteria',
    'rhizobium': 'rhizobium_biofertilizer',
    'trichoderma': 'trichoderma_compost',
    'seaweed': 'seaweed_extract',
    'fish': 'fish_emulsion',

    # -------------------------------
    # 🪴 Indigenous Preparations
    # -------------------------------
    'cowdung': 'cow_dung_slurry',
    'bioslurry': 'bio_slurry',
    'beejamrit': 'beejamrit',
    'panchagavya': 'panchagavya',
    'jeevamrut': 'jeevamrut',

    # -------------------------------
    # 💡 Advisory / Control Keywords
    # -------------------------------
    'avoidn': 'avoid_n',
    'stopp': 'stop_p',
    'stopk': 'stop_k',
    'reducen': 'reduce_n'
  }

    
    return variations.get(normalized, normalized)


def get_price(fertilizer_name: str) -> float:
    """Get price per kg for a fertilizer"""
    normalized = normalize_fertilizer_name(fertilizer_name)
    if not normalized:
        return 0.0
    
    return DEFAULT_PRICES.get(normalized, 0.0)


def calculate_application_dates(sowing_date_str: str) -> Dict[str, str]:
    """Calculate application timing based on sowing date"""
    try:
        sowing_date = datetime.fromisoformat(sowing_date_str)
    except:
        # Fallback to relative timing if date parsing fails
        return {
            "primary": "Apply 1-2 weeks before planting or as top dressing during vegetative growth",
            "secondary": "Apply during active growth phase or as recommended for specific fertilizer",
            "organics": "Apply 3-4 weeks before planting to allow decomposition"
        }
    
    # Calculate specific dates
    primary_date = sowing_date - timedelta(days=7)  # 1 week before sowing
    secondary_date = sowing_date + timedelta(days=21)  # 3 weeks after sowing
    organics_date = sowing_date - timedelta(days=21)  # 3 weeks before sowing
    
    return {
        "primary": f"Apply 1-2 weeks before planting (around {primary_date.strftime('%d %B %Y')}) or as top dressing during vegetative growth",
        "secondary": f"Apply during fruit development stage (around {secondary_date.strftime('%d %B %Y')}) or as recommended for specific fertilizer",
        "organics": f"Apply 3-4 weeks before planting (around {organics_date.strftime('%d %B %Y')}) to allow decomposition"
    }


def calculate_fertilizer_quantity(
    fertilizer_name: str,
    field_size: float,
    nutrient_status: str,
    fertilizer_type: str = "primary"
) -> float:
    """
    Calculate fertilizer quantity based on field size and nutrient status
    
    Args:
        fertilizer_name: Name of fertilizer
        field_size: Field size in hectares
        nutrient_status: Low/Optimal/High
        fertilizer_type: primary/secondary/organic
    
    Returns:
        Quantity in kg
    """
    if not fertilizer_name or fertilizer_name in ['—', 'None', 'NA']:
        return 0.0
    
    # Base rates per hectare (conservative estimates)
    base_rates = {
    # ----------------------------------------
    # 🌾 Nitrogen & Phosphorus Sources
    # ----------------------------------------
    'urea': 150,  # main N source (low dose, high N%)
    'calcium_ammonium_nitrate': 150,
    'ammonium_sulphate': 150,
    'diammonium_phosphate_dap': 120,  # also supplies P
    'monoammonium_phosphate_map': 120,
    'ammonium_nitrate': 150,
    'calcium_ammonium_nitrate_can': 150,
    'urea_ammonium_nitrate_uan': 150,
    'triple_super_phosphate_tsp': 100,
    'single_super_phosphate_ssp': 150,
    'rock_phosphate': 200,

    # ----------------------------------------
    # 🧂 Potassium Sources
    # ----------------------------------------
    'muriate_of_potash_mop': 80,
    'sulphate_of_potash_sop': 80,
    'potassium_sulfate': 80,  # alias for SOP
    'balanced_npk_maintenance': 100,

    # ----------------------------------------
    # 🧪 Secondary & Micronutrient Sources
    # ----------------------------------------
    'zinc_sulphate': 10,
    'manganese_sulphate': 8,
    'ferrous_sulphate': 8,
    'magnesium_sulphate': 10,
    'borax_zinc_sulphate_mixture': 10,
    'ferrous_sulphate_manganese_sulphate_mixture': 10,
    'zinc_sulphate_manganese_sulphate_mixture': 10,
    'gypsum_borax_mixture': 15,
    'ammonium_molybdate_zinc_sulphate_mixture': 8,

    # ----------------------------------------
    # 🌿 Organic Sources (bulk material)
    # ----------------------------------------
    'vermicompost': 2500,
    'compost': 5000,
    'farmyard_manure_fym': 5000,
    'neem_cake': 500,
    'poultry_manure': 2000,
    'mustard_cake': 500,
    'bone_meal': 300,
    'green_manure': 1000,
    'banana_wastes': 2000,
    'mulch': 3000,

    # ----------------------------------------
    # 🧫 Biofertilizers (liquid / microbial)
    # ----------------------------------------
    'psb_phosphate_solubilizing_bacteria': 5,
    'rhizobium_biofertilizer': 5,
    'rhizobium_biofertilizer_zinc_sulphate_mixture': 5,
    'azolla': 100,
    'trichoderma_compost': 200,
    'seaweed_extract': 5,
    'fish_emulsion': 5,

    # ----------------------------------------
    # 🪴 Natural & Traditional Amendments
    # ----------------------------------------
    'cow_dung_slurry': 1000,
    'bio_slurry': 1000,
    'beejamrit': 10,
    'panchagavya': 10,
    'jeevamrut': 10
  }
  
    normalized = normalize_fertilizer_name(fertilizer_name)
    base_rate = base_rates.get(normalized, 100)  # Default 100 kg/ha
    
    # Adjust based on nutrient status
    if nutrient_status and nutrient_status.lower() == 'low':
        multiplier = 1.25  # 25% increase for low status
    elif nutrient_status and nutrient_status.lower() == 'high':
        multiplier = 0.5  # 50% reduction for high status
    else:
        multiplier = 1.0  # Normal for optimal
    
    # Calculate total quantity
    quantity = base_rate * field_size * multiplier
    
    return round(quantity)


# ==================================================================================
# GEMINI PROMPT GENERATION
# ==================================================================================
def generate_gemini_prompt(
    input_data: InputData,
    ml_prediction: MLPrediction
) -> str:
    """Generate comprehensive prompt for Gemini API"""
    
    prompt = f"""You are an expert agricultural consultant specializing in fertilizer recommendations for Indian farmers.

Based on the following information, provide detailed recommendations:

**Soil and Environmental Data:**
- Temperature: {input_data.temperature}°C
- Humidity: {input_data.humidity}%
- Moisture: {input_data.moisture}%
- Soil Type: {input_data.soil_type}
- Soil pH: {input_data.ph}
- EC (Electrical Conductivity): {input_data.ec} mmhos/cm²

**Soil Nutrient Levels (mg/kg):**
- Nitrogen (N): {input_data.nitrogen} mg/kg
- Phosphorus (P): {input_data.phosphorus} mg/kg
- Potassium (K): {input_data.potassium} mg/kg

**Crop Information:**
- Crop: {input_data.crop}
- Sowing Date: {input_data.sowing_date}
- Field Size: {input_data.field_size} hectares

**ML Model Predictions:**
- Nitrogen Status: {ml_prediction.n_status}
- Phosphorus Status: {ml_prediction.p_status}
- Potassium Status: {ml_prediction.k_status}
- Primary Fertilizer Recommended: {ml_prediction.primary_fertilizer}
- Secondary Fertilizer Recommended: {ml_prediction.secondary_fertilizer}
- pH Amendment: {ml_prediction.ph_amendment}

**Task:**
Provide recommendations in the following JSON format:

{{
    "primary_fertilizer": {{
        "name": "{ml_prediction.primary_fertilizer}",
        "npk": "Provide NPK ratio like 46-0-0 for Urea",
        "reason": "Explain why this fertilizer is recommended based on soil nutrient levels (mention the mg/kg values)",
        "application_method": "Detailed method: when to apply, how to apply (broadcast/banding), and any precautions"
    }},
    "secondary_fertilizer": {{
        "name": "{ml_prediction.secondary_fertilizer}",
        "reason": "Explain why this secondary fertilizer addresses the deficiency",
        "application_method": "Detailed application instructions specific to this fertilizer"
    }},
    "organic_alternatives": [
        {{
            "name": "Select from: {', '.join(ORGANIC_ALTERNATIVES[:10])}",
            "quantity_kg": "Estimate quantity for {input_data.field_size} hectares",
            "reason": "Benefits of this organic alternative",
            "timing": "Best time to apply (e.g., '3-4 weeks before sowing')"
        }},
        {{
            "name": "Select another from: {', '.join(ORGANIC_ALTERNATIVES[10:])}",
            "quantity_kg": "Estimate quantity for {input_data.field_size} hectares",
            "reason": "Benefits of this organic alternative",
            "timing": "Best time to apply"
        }},
        {{
            "name": "Select third option from the provided list",
            "quantity_kg": "Estimate quantity for {input_data.field_size} hectares",
            "reason": "Benefits of this organic alternative",
            "timing": "Best time to apply"
        }}
    ],
    "soil_recommendations": [
        "List 4-5 specific recommendations for maintaining soil health based on current pH ({input_data.ph}), EC ({input_data.ec}), and nutrient status",
        "Include advice on moisture management",
        "Include advice on testing frequency",
        "Include crop rotation suggestions if applicable"
    ]
}}

**Important Guidelines:**
1. All organic alternatives MUST be selected ONLY from this list: {', '.join(ORGANIC_ALTERNATIVES)}
2. NPK values are provided in mg/kg (not kg/ha)
3. Consider the specific crop ({input_data.crop}) requirements
4. Provide practical, farmer-friendly advice
5. Return ONLY valid JSON, no additional text
"""
    
    return prompt


# ==================================================================================
# MAIN RECOMMENDATION GENERATION FUNCTION
# ==================================================================================
def generate_enhanced_recommendation(
    input_data: InputData,
    ml_prediction: MLPrediction,
    confidence_scores: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Generate comprehensive fertilizer recommendation using Gemini API
    
    Args:
        input_data: User input data
        ml_prediction: ML model predictions
        confidence_scores: Confidence scores from ML model
    
    Returns:
        Complete recommendation report
    """
    
    print("🌱 Generating Enhanced Fertilizer Recommendation...")
    print("="*70)
    
    # Configure Gemini API
    try:
        model = configure_gemini_api()
    except Exception as e:
        print(f"❌ Error configuring Gemini API: {e}")
        return generate_fallback_recommendation(input_data, ml_prediction, confidence_scores)
    
    # Generate prompt
    prompt = generate_gemini_prompt(input_data, ml_prediction)
    
    # Get Gemini response
    try:
        print("📡 Calling Gemini API...")
        response = model.generate_content(prompt)
        
        # Extract JSON from response
        response_text = response.text.strip()
        
        # Remove markdown code blocks if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        gemini_data = json.loads(response_text.strip())
        print("✅ Successfully received Gemini recommendations")
        
    except Exception as e:
        print(f"⚠️ Error with Gemini API: {e}")
        print("📋 Using fallback recommendation...")
        return generate_fallback_recommendation(input_data, ml_prediction, confidence_scores)
    
    # Calculate quantities and costs
    print("💰 Calculating quantities and costs...")
    
    # Primary fertilizer
    primary_quantity = calculate_fertilizer_quantity(
        ml_prediction.primary_fertilizer,
        input_data.field_size,
        ml_prediction.n_status,
        "primary"
    )
    primary_price_per_kg = get_price(ml_prediction.primary_fertilizer)
    primary_cost = primary_quantity * primary_price_per_kg
    
    # Secondary fertilizer
    secondary_quantity = calculate_fertilizer_quantity(
        ml_prediction.secondary_fertilizer,
        input_data.field_size,
        ml_prediction.k_status,
        "secondary"
    )
    secondary_price_per_kg = get_price(ml_prediction.secondary_fertilizer)
    secondary_cost = secondary_quantity * secondary_price_per_kg
    
    # Organic alternatives
    organic_costs = []
    organic_details = []
    
    for org in gemini_data.get("organic_alternatives", []):
        org_name = org.get("name", "")
        # Extract quantity if provided by Gemini, else calculate
        try:
            org_quantity = int(org.get("quantity_kg", 0))
        except:
            org_quantity = calculate_fertilizer_quantity(
                org_name,
                input_data.field_size,
                "optimal",
                "organic"
            )
        
        org_price = get_price(org_name)
        org_cost = org_quantity * org_price
        organic_costs.append(org_cost)
        
        organic_details.append({
            "name": org_name,
            "amount_kg": org_quantity,
            "price_per_kg": org_price,
            "cost": org_cost,
            "reason": org.get("reason", ""),
            "timing": org.get("timing", "")
        })
    
    total_organic_cost = sum(organic_costs)
    total_cost = primary_cost + secondary_cost + total_organic_cost
    
    # Calculate application timing
    application_timing = calculate_application_dates(input_data.sowing_date)
    
    # Calculate average confidence
    if confidence_scores:
        avg_confidence = sum(confidence_scores.values()) / len(confidence_scores)
        confidence_percent = int(avg_confidence * 100)
    else:
        confidence_percent = 90  # Default
    
    # Determine nutrient deficiencies
    nutrient_deficiencies = []
    if ml_prediction.n_status.lower() == "low":
        nutrient_deficiencies.append("Nitrogen")
    if ml_prediction.p_status.lower() == "low":
        nutrient_deficiencies.append("Phosphorus")
    if ml_prediction.k_status.lower() == "low":
        nutrient_deficiencies.append("Potassium")
    
    # Build comprehensive report
    report = {
        "ml_model_prediction": {
            "name": ml_prediction.primary_fertilizer,
            "confidence_percent": confidence_percent,
            "npk": gemini_data.get("primary_fertilizer", {}).get("npk", "46-0-0")
        },
        
        "soil_condition_analysis": {
            "current_status": {
                "pH_status": "Optimal" if abs(input_data.ph - 6.5) < 0.5 else ("Acidic" if input_data.ph < 6.0 else "Alkaline"),
                "moisture_status": "Optimal" if 40 <= input_data.moisture <= 70 else ("Low" if input_data.moisture < 40 else "High"),
                "nutrient_deficiencies": nutrient_deficiencies
            },
            "soil_test_values": {
                "nitrogen_mg_kg": input_data.nitrogen,
                "phosphorus_mg_kg": input_data.phosphorus,
                "potassium_mg_kg": input_data.potassium,
                "pH": input_data.ph,
                "EC_mmhos_cm2": input_data.ec
            },
            "recommendations": gemini_data.get("soil_recommendations", [])
        },
        
        "primary_fertilizer": {
            "name": ml_prediction.primary_fertilizer,
            "amount_kg": primary_quantity,
            "npk": gemini_data.get("primary_fertilizer", {}).get("npk", "—"),
            "reason": gemini_data.get("primary_fertilizer", {}).get("reason", ""),
            "application_method": gemini_data.get("primary_fertilizer", {}).get("application_method", "")
        },
        
        "secondary_fertilizer": {
            "name": ml_prediction.secondary_fertilizer if ml_prediction.secondary_fertilizer not in ['—', 'None'] else "Not required",
            "amount_kg": secondary_quantity,
            "reason": gemini_data.get("secondary_fertilizer", {}).get("reason", ""),
            "application_method": gemini_data.get("secondary_fertilizer", {}).get("application_method", "")
        },
        
        "organic_alternatives": organic_details,
        
        "application_timing": {
            "primary_fertilizer": application_timing["primary"],
            "secondary_fertilizer": application_timing["secondary"],
            "organic_options": application_timing["organics"]
        },
        
        "cost_estimate": {
            "primary_fertilizer": f"₹{int(primary_cost):,}",
            "secondary_fertilizer": f"₹{int(secondary_cost):,}",
            "organic_options": f"₹{int(total_organic_cost):,}",
            "total_estimate": f"₹{int(total_cost):,}",
            "field_size": f"For {input_data.field_size:.2f} hectares ({input_data.field_size * 2.471:.2f} acres)",
            "breakdown": {
                "primary": {
                    "fertilizer": ml_prediction.primary_fertilizer,
                    "quantity_kg": primary_quantity,
                    "price_per_kg": f"₹{primary_price_per_kg:.2f}",
                    "total": f"₹{int(primary_cost):,}"
                },
                "secondary": {
                    "fertilizer": ml_prediction.secondary_fertilizer,
                    "quantity_kg": secondary_quantity,
                    "price_per_kg": f"₹{secondary_price_per_kg:.2f}",
                    "total": f"₹{int(secondary_cost):,}"
                },
                "organics": [
                    {
                        "fertilizer": org["name"],
                        "quantity_kg": org["amount_kg"],
                        "price_per_kg": f"₹{org['price_per_kg']:.2f}",
                        "total": f"₹{int(org['cost']):,}"
                    }
                    for org in organic_details
                ]
            }
        },
        
        "_metadata": {
            "generated_at": datetime.now().isoformat(),
            "crop": input_data.crop,
            "soil_type": input_data.soil_type,
            "sowing_date": input_data.sowing_date,
            "field_size_hectares": input_data.field_size,
            "model_used": "Gemini-1.5-Flash + ML Stacking Model",
            "nutrient_units": "mg/kg"
        }
    }
    
    print("✅ Recommendation generated successfully!")
    print(f"📊 Total Cost: ₹{int(total_cost):,}")
    print("="*70)
    
    return report


def generate_fallback_recommendation(
    input_data: InputData,
    ml_prediction: MLPrediction,
    confidence_scores: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Generate basic recommendation without Gemini API (fallback)
    """
    
    print("📋 Generating fallback recommendation...")
    
    # Calculate quantities
    primary_quantity = calculate_fertilizer_quantity(
        ml_prediction.primary_fertilizer,
        input_data.field_size,
        ml_prediction.n_status,
        "primary"
    )
    
    secondary_quantity = calculate_fertilizer_quantity(
        ml_prediction.secondary_fertilizer,
        input_data.field_size,
        ml_prediction.k_status,
        "secondary"
    )
    
    # Select default organic alternatives
    default_organics = ["Vermicompost", "Neem cake", "Compost"]
    organic_details = []
    organic_costs = []
    
    for org_name in default_organics:
        org_quantity = calculate_fertilizer_quantity(org_name, input_data.field_size, "optimal", "organic")
        org_price = get_price(org_name)
        org_cost = org_quantity * org_price
        organic_costs.append(org_cost)
        
        organic_details.append({
            "name": org_name,
            "amount_kg": org_quantity,
            "price_per_kg": org_price,
            "cost": org_cost,
            "reason": f"Provides organic nutrients and improves soil structure for {input_data.crop}",
            "timing": "Apply 3-4 weeks before sowing"
        })
    
    # Calculate costs
    primary_price = get_price(ml_prediction.primary_fertilizer)
    secondary_price = get_price(ml_prediction.secondary_fertilizer)
    
    primary_cost = primary_quantity * primary_price
    secondary_cost = secondary_quantity * secondary_price
    total_organic_cost = sum(organic_costs)
    total_cost = primary_cost + secondary_cost + total_organic_cost
    
    # Application timing
    application_timing = calculate_application_dates(input_data.sowing_date)
    
    # Build basic report
    report = {
        "ml_model_prediction": {
            "name": ml_prediction.primary_fertilizer,
            "confidence_percent": 85,
            "npk": "46-0-0" if "urea" in ml_prediction.primary_fertilizer.lower() else "18-46-0"
        },
        "soil_condition_analysis": {
            "current_status": {
                "pH_status": "Optimal" if abs(input_data.ph - 6.5) < 0.5 else "Needs adjustment",
                "moisture_status": "Optimal",
                "nutrient_deficiencies": []
            },
            "soil_test_values": {
                "nitrogen_mg_kg": input_data.nitrogen,
                "phosphorus_mg_kg": input_data.phosphorus,
                "potassium_mg_kg": input_data.potassium
            },
            "recommendations": [
                "Maintain current pH levels",
                "Regular soil testing recommended",
                "Consider crop rotation"
            ]
        },
        "primary_fertilizer": {
            "name": ml_prediction.primary_fertilizer,
            "amount_kg": primary_quantity,
            "npk": "Check fertilizer label",
            "reason": f"Recommended based on {ml_prediction.n_status} nitrogen status",
            "application_method": "Apply in split doses during vegetative growth"
        },
        "secondary_fertilizer": {
            "name": ml_prediction.secondary_fertilizer,
            "amount_kg": secondary_quantity,
            "reason": f"Addresses {ml_prediction.k_status} potassium status",
            "application_method": "Apply during active growth phase"
        },
        "organic_alternatives": organic_details,
        "application_timing": {
            "primary_fertilizer": application_timing["primary"],
            "secondary_fertilizer": application_timing["secondary"],
            "organic_options": application_timing["organics"]
        },
        "cost_estimate": {
            "primary_fertilizer": f"₹{int(primary_cost):,}",
            "secondary_fertilizer": f"₹{int(secondary_cost):,}",
            "organic_options": f"₹{int(total_organic_cost):,}",
            "total_estimate": f"₹{int(total_cost):,}",
            "field_size": f"For {input_data.field_size:.2f} hectares"
        },
        "_metadata": {
            "generated_at": datetime.now().isoformat(),
            "model_used": "ML Stacking Model (Fallback Mode)",
            "nutrient_units": "mg/kg"
        }
    }
    
    return report


# ==================================================================================
# EXAMPLE USAGE
# ==================================================================================
if __name__ == "__main__":
    # Example: Load ML predictions from your stacking model
    # This would come from multioutput_stacking_fertilizer.py
    
    # Sample input data
    sample_input = InputData(
        temperature=28.5,
        humidity=65.0,
        moisture=55.0,
        soil_type="Loamy",
        crop="Wheat",
        nitrogen=180.0,  # mg/kg
        phosphorus=25.0,  # mg/kg
        potassium=150.0,  # mg/kg
        ph=6.8,
        ec=0.45,
        sowing_date="2025-11-15",
        field_size=2.27  # hectares (approx 5.6 acres)
    )
    
    # Sample ML predictions
    sample_prediction = MLPrediction(
        n_status="Optimal",
        p_status="Low",
        k_status="Optimal",
        primary_fertilizer="Urea",
        secondary_fertilizer="Potassium sulfate",
        ph_amendment="None"
    )
    
    # Sample confidence scores
    sample_confidences = {
        "N_Status": 0.92,
        "P_Status": 0.88,
        "K_Status": 0.90,
        "Primary_Fertilizer": 0.89,
        "Secondary_Fertilizer": 0.85,
        "pH_Amendment": 0.95
    }
    
    # Generate recommendation
    try:
        recommendation = generate_enhanced_recommendation(
            input_data=sample_input,
            ml_prediction=sample_prediction,
            confidence_scores=sample_confidences
        )
        
        # Print results
        print("\n" + "="*70)
        print("FERTILIZER RECOMMENDATION REPORT")
        print("="*70)
        print(json.dumps(recommendation, indent=2, ensure_ascii=False))
        
        # Save to file
        output_file = "recommendation_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(recommendation, f, indent=2, ensure_ascii=False)
        print(f"\n✅ Report saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
