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
# ORGANIC FERTILIZER NUTRIENT INFORMATION
# ==================================================================================
ORGANIC_NUTRIENTS = {
    "Vermicompost": {
        "npk": "1.5-1.0-1.5",
        "primary_nutrients": ["Nitrogen", "Phosphorus", "Potassium"],
        "secondary_nutrients": ["Calcium", "Magnesium"],
        "micronutrients": ["Zinc", "Iron", "Copper", "Manganese"],
        "benefits": "Improves soil structure, water retention, and microbial activity; Rich in humus and beneficial microorganisms",
        "best_for": "All crops, especially vegetables and fruits"
    },
    "Farmyard manure (FYM)": {
        "npk": "0.5-0.2-0.5",
        "primary_nutrients": ["Nitrogen", "Phosphorus", "Potassium"],
        "secondary_nutrients": ["Calcium", "Magnesium", "Sulfur"],
        "micronutrients": ["Iron", "Zinc", "Copper", "Boron"],
        "benefits": "Adds organic matter, improves soil tilth, enhances water holding capacity; Slow nutrient release",
        "best_for": "Field crops, improves clay and sandy soils"
    },
    "Compost": {
        "npk": "0.8-0.5-0.8",
        "primary_nutrients": ["Nitrogen", "Phosphorus", "Potassium"],
        "secondary_nutrients": ["Calcium", "Magnesium"],
        "micronutrients": ["Iron", "Manganese", "Boron"],
        "benefits": "Balances soil pH, increases nutrient availability, promotes beneficial microbes; Excellent organic matter source",
        "best_for": "All crops, soil conditioning"
    },
    "Poultry manure": {
        "npk": "3.0-2.5-1.5",
        "primary_nutrients": ["Nitrogen", "Phosphorus"],
        "secondary_nutrients": ["Calcium"],
        "micronutrients": ["Zinc", "Copper", "Manganese"],
        "benefits": "High nitrogen content, quick nutrient release; Rich in calcium; Excellent for nitrogen-deficient soils",
        "best_for": "Leafy vegetables, nitrogen-demanding crops"
    },
    "Neem cake": {
        "npk": "5.0-1.0-1.5",
        "primary_nutrients": ["Nitrogen"],
        "secondary_nutrients": ["Sulfur"],
        "micronutrients": [],
        "benefits": "Natural pest repellent, improves nitrogen availability; Slow nitrogen release; Controls soil nematodes",
        "best_for": "All crops, especially where pest control is needed"
    },
    "Bone meal": {
        "npk": "3.0-15.0-0.0",
        "primary_nutrients": ["Phosphorus"],
        "secondary_nutrients": ["Calcium"],
        "micronutrients": [],
        "benefits": "Excellent phosphorus source, promotes root development and flowering; Slow release; Adds calcium",
        "best_for": "Flowering plants, root vegetables, phosphorus-deficient soils"
    },
    "Mustard cake": {
        "npk": "5.0-2.0-1.0",
        "primary_nutrients": ["Nitrogen", "Phosphorus"],
        "secondary_nutrients": ["Sulfur"],
        "micronutrients": [],
        "benefits": "High nitrogen content, pest deterrent properties; Improves soil structure; Natural nematicide",
        "best_for": "Vegetables, oilseed crops"
    },
    "Green manure": {
        "npk": "0.5-0.2-0.3",
        "primary_nutrients": ["Nitrogen"],
        "secondary_nutrients": [],
        "micronutrients": [],
        "benefits": "Fixes atmospheric nitrogen (if legumes), adds organic matter, suppresses weeds; Improves soil structure",
        "best_for": "All field crops, soil rejuvenation"
    },
    "Banana wastes": {
        "npk": "0.5-0.3-3.5",
        "primary_nutrients": ["Potassium"],
        "secondary_nutrients": [],
        "micronutrients": [],
        "benefits": "Excellent potassium source, improves fruit quality; Enhances disease resistance",
        "best_for": "Fruit crops, potassium-deficient soils"
    },
    "Azolla": {
        "npk": "4.0-0.5-2.0",
        "primary_nutrients": ["Nitrogen"],
        "secondary_nutrients": [],
        "micronutrients": [],
        "benefits": "Nitrogen-fixing aquatic fern, rapid biomass production; Free nitrogen from atmosphere",
        "best_for": "Rice paddies, wetland crops"
    },
    "PSB (Phosphate Solubilizing Bacteria)": {
        "npk": "0.0-0.0-0.0",
        "primary_nutrients": ["Phosphorus (makes available)"],
        "secondary_nutrients": [],
        "micronutrients": [],
        "benefits": "Converts unavailable soil phosphorus to plant-available forms; Improves phosphorus uptake efficiency",
        "best_for": "All crops in phosphorus-rich but unavailable soils"
    },
    "Rhizobium biofertilizer": {
        "npk": "0.0-0.0-0.0",
        "primary_nutrients": ["Nitrogen (fixes from air)"],
        "secondary_nutrients": [],
        "micronutrients": [],
        "benefits": "Biological nitrogen fixation in legumes; Reduces nitrogen fertilizer requirement; Free atmospheric nitrogen",
        "best_for": "Legume crops (pulses, beans, peas)"
    },
    "Seaweed extract": {
        "npk": "1.0-0.5-2.0",
        "primary_nutrients": ["Potassium"],
        "secondary_nutrients": ["Magnesium", "Calcium"],
        "micronutrients": ["Iron", "Zinc", "Manganese", "Boron"],
        "benefits": "Rich in growth hormones, micronutrients, and trace elements; Enhances stress tolerance and plant immunity",
        "best_for": "High-value crops, stress conditions"
    },
    "Fish emulsion": {
        "npk": "4.0-2.0-1.0",
        "primary_nutrients": ["Nitrogen", "Phosphorus"],
        "secondary_nutrients": [],
        "micronutrients": ["Iron", "Zinc", "Calcium"],
        "benefits": "Quick-acting liquid fertilizer, balanced nutrients; Promotes vigorous growth",
        "best_for": "Vegetables, ornamentals"
    },
    "Mulch": {
        "npk": "0.2-0.1-0.2",
        "primary_nutrients": [],
        "secondary_nutrients": [],
        "micronutrients": [],
        "benefits": "Conserves soil moisture, suppresses weeds, moderates soil temperature; Slowly adds organic matter",
        "best_for": "All crops, moisture conservation"
    },
    "Cow dung slurry": {
        "npk": "0.6-0.3-0.4",
        "primary_nutrients": ["Nitrogen", "Phosphorus", "Potassium"],
        "secondary_nutrients": [],
        "micronutrients": [],
        "benefits": "Quick nutrient availability in liquid form, improves microbial activity",
        "best_for": "Quick nutrient boost for all crops"
    },
    "Bio-slurry": {
        "npk": "1.5-1.0-1.0",
        "primary_nutrients": ["Nitrogen", "Phosphorus", "Potassium"],
        "secondary_nutrients": [],
        "micronutrients": [],
        "benefits": "Biogas digester byproduct, pathogen-free, rich in available nutrients",
        "best_for": "All crops, organic farming"
    },
    "Trichoderma compost": {
        "npk": "1.0-0.8-1.0",
        "primary_nutrients": ["Nitrogen", "Phosphorus", "Potassium"],
        "secondary_nutrients": [],
        "micronutrients": [],
        "benefits": "Contains beneficial Trichoderma fungi for disease control; Improves soil health and nutrient availability",
        "best_for": "All crops, disease-prone soils"
    },
    "Beejamrit": {
        "npk": "0.5-0.2-0.3",
        "primary_nutrients": [],
        "secondary_nutrients": [],
        "micronutrients": [],
        "benefits": "Seed treatment solution, enhances germination and seedling vigor; Provides beneficial microbes",
        "best_for": "Seed treatment for all crops"
    },
    "Panchagavya": {
        "npk": "0.3-0.2-0.2",
        "primary_nutrients": [],
        "secondary_nutrients": [],
        "micronutrients": ["Various trace elements"],
        "benefits": "Growth promoter, improves plant immunity, enhances soil microbial activity; Traditional organic input",
        "best_for": "All crops, foliar spray"
    },
    "Jeevamrut": {
        "npk": "0.8-0.3-0.5",
        "primary_nutrients": ["Nitrogen"],
        "secondary_nutrients": [],
        "micronutrients": [],
        "benefits": "Liquid manure with beneficial microbes, improves soil fertility and microbial population",
        "best_for": "All crops, soil drench or irrigation"
    }
}


# ==================================================================================
# NPK RATIOS - Nutrient Content of Fertilizers
# ==================================================================================
NPK_RATIOS = {
    # Nitrogen (N) Fertilizers
    'urea': '46-0-0',
    'ammonium_nitrate': '34-0-0',
    'ammonium_sulphate': '21-0-0',
    'ammonium_chloride': '25-0-0',  # Standard NPK ratio for Ammonium Chloride
    'urea_ammonium_nitrate_uan': '32-0-0',
    
    # Phosphate (P) Fertilizers
    'diammonium_phosphate_dap': '18-46-0',
    'monoammonium_phosphate_map': '11-52-0',
    'single_super_phosphate_ssp': '0-16-0',
    'triple_super_phosphate_tsp': '0-46-0',
    'rock_phosphate': '0-20-0',    # Available P2O5 is highly variable (often 20-30%) and slow-releasing
    
    # Potash (K) Fertilizers
    'muriate_of_potash_mop': '0-0-60',
    'sop_sulphate_of_potash': '0-0-50',
    'potassium_nitrate': '13-0-44',
    'potassium_carbonate': '0-0-67', # Often listed as 0-0-67, deriving from K2O content
    'potassium_magnesium_sulphate': '0-0-22', # Typical ratio is 0-0-22 (+11% Mg, +22% S)
    
    # Compound & Blended Fertilizers
    'balanced_npk_14_14_14': '14-14-14',
    
    # Physical Mixtures (Ratios are an approximate mix)
    'dap_mop_mixture': '9-23-30',   # Based on 50% DAP (18-46-0) + 50% MOP (0-0-60)
    'urea_mop_mixture': '23-0-30',   # Based on 50% Urea (46-0-0) + 50% MOP (0-0-60)
}


# ==================================================================================
# PRICE TABLE - Default Prices (₹/kg)
# ==================================================================================
DEFAULT_PRICES = {
    # Primary Fertilizers
    "urea": 28.00,
    "diammonium_phosphate_dap": 120.00,
    "muriate_of_potash_mop": 35.00,
    "monoammonium_phosphate_map": 250.00,
    "single_super_phosphate_ssp": 12.00,
    "ammonium_sulphate": 30.00,
    "potassium_nitrate": 175.00,
    "triple_super_phosphate_tsp": 96.00,
    "ammonium_nitrate": 90.00,
    "ammonium_chloride": 25.00,
    "sulphate_of_potash_sop": 200.00,
    "potassium_carbonate": 90.00,
    "potassium_magnesium_sulphate": 150.00,
    "rock_phosphate": 15.00,
    "urea_ammonium_nitrate_uan": 75.00,
    "balanced_npk_maintenance": 35.00,
    "calcium_ammonium_nitrate_can": 85.00,
    "dap_mop_mixture": 155.00,
    "urea_mop_mixture": 63.00,
    
    # Secondary/Micronutrient Fertilizers
    "zinc_sulphate": 70.00,
    "ferrous_sulphate": 15.00,
    "borax": 75.00,
    "manganese_sulphate": 45.00,
    "copper_sulphate": 220.00,
    "ammonium_molybdate": 2500.00,
    "calcium_chloride": 65.00,
    "nickel_sulphate": 400.00,
    
    # pH Amendments
    "agricultural_lime": 6.00,
    "dolomitic_lime": 8.00,
    "gypsum": 5.00,
    "wood_ash": 12.00,
    "quicklime": 9.00,
    "hydrated_lime": 15.00,
    "ammonium_sulphate": 22.00,
    "ferrous_sulphate_iron_sulphate": 20.00,
    "aluminium_sulphate": 25.00,
    "elemental_sulphur": 70.00,
    "balance_maintain": 0.00,
    
    # Organic Fertilizers
    "vermicompost": 15.00,
    "neem_cake": 35.00,
    "bone_meal": 30.00,
    "compost": 8.00,
    "poultry_manure": 5.00,
    "farmyard_manure_fym": 3.00,
    "mustard_cake": 35.00,
    "fish_emulsion": 180.00,
    "seaweed_extract": 150.00,
    "cow_dung_slurry": 1.50,
    "green_manure": 5.00,
    "bio_slurry": 3.00,
    "trichoderma_compost": 18.00,
    "beejamrit": 10.00,
    "panchagavya": 15.00,
    "jeevamrut": 8.00,
    "mulch": 4.00,
    "banana_wastes": 2.00,
    "azolla": 25.00,
    "psb_phosphate_solubilizing_bacteria": 150.00,
    "rhizobium_biofertilizer": 120.00,
    
    # Legacy aliases
    'dap': 'diammonium_phosphate_dap',     
    'mop': 'muriate_of_potash_mop',       
    'map': 'monoammonium_phosphate_map',  
    'ssp': 'single_super_phosphate_ssp',  
    'tsp': 'triple_super_phosphate_tsp',    
    'sop': 'sulphate_of_potash_sop',         
    'uan': 'urea_ammonium_nitrate_uan',      
    'lime': 'agricultural_lime',             
    'sulphur': 'elemental_sulphur',          
    'psb': 'psb_phosphate_solubilizing_bacteria', 
    'rhizobium': 'rhizobium_biofertilizer', 
    'fym': 'farmyard_manure_fym' 
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
    ph_amendment: str


@dataclass
class InputData:
    """User input data"""
    nitrogen: float  # mg/kg
    phosphorus: float  # mg/kg
    potassium: float  # mg/kg
    ph: float
    ec: float  # mmhos/cm2
    soil_temperature: float  # °C
    soil_moisture: float  # %
    soil_type: str
    crop_type: str
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
# HELPER FUNCTIONS FOR NUTRIENT INFORMATION
# ==================================================================================
def get_fertilizer_nutrients(fertilizer_name: str) -> str:
    """Get nutrient information for a fertilizer"""
    normalized = normalize_fertilizer_name(fertilizer_name)
    
    nutrient_map = {
        'urea': 'High Nitrogen (46% N)',
        'diammonium_phosphate_dap': 'Nitrogen (18%) and Phosphorus (46%)',
        'monoammonium_phosphate_map': 'Nitrogen (11%) and Phosphorus (52%)',
        'muriate_of_potash_mop': 'High Potassium (60% K₂O)',
        'sulphate_of_potash_sop': 'Potassium (50% K₂O) and Sulfur',
        'single_super_phosphate_ssp': 'Phosphorus (16% P₂O₅), Calcium, and Sulfur',
        'triple_super_phosphate_tsp': 'High Phosphorus (46% P₂O₅)',
        'ammonium_sulphate': 'Nitrogen (21% N) and Sulfur (24% S)',
        'calcium_ammonium_nitrate_can': 'Nitrogen (26% N) and Calcium',
        'npk_10_26_26': 'Balanced NPK (10-26-26)',
        'npk_12_32_16': 'Balanced NPK (12-32-16)',
        'npk_20_20_0': 'Nitrogen (20%) and Phosphorus (20%)',
        'npk_19_19_19': 'Balanced NPK (19-19-19)',
    }
    
    return nutrient_map.get(normalized, f'Essential nutrients from {fertilizer_name}')


def get_secondary_nutrients(fertilizer_name: str) -> str:
    """Get nutrient information for secondary/micronutrient fertilizers"""
    if not fertilizer_name or fertilizer_name in ['—', 'None', 'NA', 'Not required']:
        return 'No additional micronutrients needed'
    
    nutrients = []
    fertilizer_lower = fertilizer_name.lower()
    
    if 'zinc' in fertilizer_lower:
        nutrients.append('Zinc (21% Zn)')
    if 'boron' in fertilizer_lower or 'borax' in fertilizer_lower:
        nutrients.append('Boron (11% B)')
    if 'iron' in fertilizer_lower or 'ferrous' in fertilizer_lower:
        nutrients.append('Iron (19% Fe)')
    if 'manganese' in fertilizer_lower:
        nutrients.append('Manganese (30% Mn)')
    if 'copper' in fertilizer_lower:
        nutrients.append('Copper (25% Cu)')
    if 'magnesium' in fertilizer_lower:
        nutrients.append('Magnesium (9% Mg)')
    if 'molybdenum' in fertilizer_lower:
        nutrients.append('Molybdenum (39% Mo)')
    
    if nutrients:
        return ', '.join(nutrients)
    return f'Micronutrients from {fertilizer_name}'


# ==================================================================================
# UTILITY FUNCTIONS
# ==================================================================================
def normalize_fertilizer_name(name: str) -> str:
    """Normalize fertilizer name for price lookup"""
    if not name or name in ['—', 'None', 'NA']:
        return None
    
    # Handle compound fertilizers (e.g., "DAP + MOP")
    # Extract first fertilizer if it's a combination with "+"
    if '+' in name:
        # Split by '+' and take the first part
        name = name.split('+')[0].strip()
    
    # Extract abbreviation if present (e.g., "DAP (Di-Ammonium Phosphate)" -> "DAP")
    if '(' in name:
        # Get the part before the parentheses
        abbreviation = name.split('(')[0].strip()
        if abbreviation:
            name = abbreviation
    
    # Convert to lowercase and replace spaces with underscores
    normalized = name.lower().replace(' ', '_').replace('(', '').replace(')', '')
    
 # 🧭 Handle common fertilizer name variations and abbreviations
    variations = {
    # -------------------------------
    # 🌾 Chemical Fertilizers (Primary)
    # -------------------------------
    'dap': 'diammonium_phosphate_dap',
    'di_ammonium_phosphate': 'diammonium_phosphate_dap',
    'diammonium_phosphate': 'diammonium_phosphate_dap',
    'map': 'monoammonium_phosphate_map',
    'mono_ammonium_phosphate': 'monoammonium_phosphate_map',
    'monoammonium_phosphate': 'monoammonium_phosphate_map',
    'mop': 'muriate_of_potash_mop',
    'muriate_of_potash': 'muriate_of_potash_mop',
    'sop': 'sulphate_of_potash_sop',
    'sulphate_of_potash': 'sulphate_of_potash_sop',
    'ssp': 'single_super_phosphate_ssp',
    'single_super_phosphate': 'single_super_phosphate_ssp',
    'tsp': 'triple_super_phosphate_tsp',
    'triple_super_phosphate': 'triple_super_phosphate_tsp',
    'can': 'calcium_ammonium_nitrate_can',
    'calcium_ammonium_nitrate': 'calcium_ammonium_nitrate_can',
    'uan': 'urea_ammonium_nitrate_uan',
    'urea_ammonium_nitrate': 'urea_ammonium_nitrate_uan',
    'as': 'ammonium_sulphate',
    'an': 'ammonium_nitrate',
    'ammonium_nitrate': 'ammonium_nitrate',
    'ammonium_sulphate': 'ammonium_sulphate',
    'ammonium_chloride': 'ammonium_chloride',
    'urea': 'urea',
    'urea46': 'urea',
    'rockp': 'rock_phosphate',
    'rock_phosphate': 'rock_phosphate',
    'npk': 'balanced_npk_maintenance',
    'balanced_npk': 'balanced_npk_maintenance',
    'balanced_npk_14_14_14': 'balanced_npk_maintenance',
    'balanced_npk_14-14-14': 'balanced_npk_maintenance',
    'potassium_nitrate': 'potassium_nitrate',
    'potassium_carbonate': 'potassium_carbonate',
    'potassium_magnesium_sulphate': 'potassium_magnesium_sulphate',
    'potassium-magnesium_sulphate': 'potassium_magnesium_sulphate',
    'dap_mop': 'dap_mop_mixture',
    'urea_mop': 'urea_mop_mixture',

    # -------------------------------
    # 🧪 Secondary & Micronutrients
    # -------------------------------
    'znso4': 'zinc_sulphate',
    'zinc_sulphate': 'zinc_sulphate',
    'fes': 'ferrous_sulphate',
    'ferrous_sulphate': 'ferrous_sulphate',
    'iron_sulphate': 'ferrous_sulphate_iron_sulphate',
    'mns': 'manganese_sulphate',
    'manganese_sulphate': 'manganese_sulphate',
    'mgs': 'magnesium_sulphate',
    'magnesium_sulphate': 'magnesium_sulphate',
    'copper_sulphate': 'copper_sulphate',
    'ammonium_molybdate': 'ammonium_molybdate',
    'calcium_chloride': 'calcium_chloride',
    'nickel_sulphate': 'nickel_sulphate',
    'borax': 'borax',
    'gypsum': 'gypsum',

    # -------------------------------
    # 🧪 pH Amendments
    # -------------------------------
    'lime': 'agricultural_lime',
    'agricultural_lime': 'agricultural_lime',
    'dolomitic_lime': 'dolomitic_lime',
    'dolomite': 'dolomitic_lime',
    'wood_ash': 'wood_ash',
    'quicklime': 'quicklime',
    'hydrated_lime': 'hydrated_lime',
    'aluminium_sulphate': 'aluminium_sulphate',
    'elemental_sulphur': 'elemental_sulphur',
    'sulphur': 'elemental_sulphur',

    # -------------------------------
    # 🌿 Organic & Natural Inputs
    # -------------------------------
    'fym': 'farmyard_manure_fym',
    'farmyard_manure': 'farmyard_manure_fym',
    'vermi': 'vermicompost',
    'vermicompost': 'vermicompost',
    'compost': 'compost',
    'neem': 'neem_cake',
    'neem_cake': 'neem_cake',
    'mustard': 'mustard_cake',
    'mustard_cake': 'mustard_cake',
    'bonemeal': 'bone_meal',
    'bone_meal': 'bone_meal',
    'poultry': 'poultry_manure',
    'poultry_manure': 'poultry_manure',
    'green': 'green_manure',
    'green_manure': 'green_manure',
    'mulch': 'mulch',
    'banana': 'banana_wastes',
    'banana_wastes': 'banana_wastes',
    'azolla': 'azolla',

    # -------------------------------
    # 🧫 Biofertilizers / Microbial
    # -------------------------------
    'psb': 'psb_phosphate_solubilizing_bacteria',
    'phosphate_solubilizing_bacteria': 'psb_phosphate_solubilizing_bacteria',
    'rhizobium': 'rhizobium_biofertilizer',
    'rhizobium_biofertilizer': 'rhizobium_biofertilizer',
    'trichoderma': 'trichoderma_compost',
    'trichoderma_compost': 'trichoderma_compost',
    'seaweed': 'seaweed_extract',
    'seaweed_extract': 'seaweed_extract',
    'fish': 'fish_emulsion',
    'fish_emulsion': 'fish_emulsion',

    # -------------------------------
    # 🪴 Indigenous Preparations
    # -------------------------------
    'cowdung': 'cow_dung_slurry',
    'cow_dung_slurry': 'cow_dung_slurry',
    'bioslurry': 'bio_slurry',
    'bio_slurry': 'bio_slurry',
    'beejamrit': 'beejamrit',
    'panchagavya': 'panchagavya',
    'jeevamrut': 'jeevamrut',

    # -------------------------------
    # 💡 Advisory / Control Keywords
    # -------------------------------
    'avoidn': 'avoid_n',
    'avoid_n': 'avoid_n',
    'stopp': 'stop_p',
    'stop_p': 'stop_p',
    'stopk': 'stop_k',
    'stop_k': 'stop_k',
    'reducen': 'reduce_n',
    'reduce_n': 'reduce_n',
    'balance_maintain': 'balance_maintain'
  }

    
    return variations.get(normalized, normalized)


def get_price(fertilizer_name: str) -> float:
    """Get price per kg for a fertilizer"""
    normalized = normalize_fertilizer_name(fertilizer_name)
    if not normalized:
        return 0.0
    
    return DEFAULT_PRICES.get(normalized, 0.0)


def calculate_compound_fertilizer_cost(
    fertilizer_name: str,
    field_size: float,
    nutrient_status: str,
    fertilizer_type: str = "secondary"
) -> dict:
    """
    Calculate cost for compound fertilizers (e.g., "Borax + Ferrous Sulphate + Zinc Sulphate")
    Returns total cost and breakdown of each component
    
    Args:
        fertilizer_name: Name of compound fertilizer
        field_size: Field size in hectares
        nutrient_status: Low/Optimal/High
        fertilizer_type: primary/secondary/organic
    
    Returns:
        Dict with total_cost, total_quantity, and components list
    """
    if not fertilizer_name or fertilizer_name in ['—', 'None', 'NA']:
        return {
            "total_cost": 0.0,
            "total_quantity": 0.0,
            "components": []
        }
    
    # Check if it's a compound fertilizer
    if '+' not in fertilizer_name:
        # Single fertilizer - calculate normally
        quantity = calculate_fertilizer_quantity(
            fertilizer_name,
            field_size,
            nutrient_status,
            fertilizer_type
        )
        price = get_price(fertilizer_name)
        cost = quantity * price
        
        return {
            "total_cost": cost,
            "total_quantity": quantity,
            "components": [{
                "name": fertilizer_name,
                "quantity_kg": quantity,
                "price_per_kg": price,
                "cost": cost
            }]
        }
    
    # Compound fertilizer - split and calculate each component
    components = [comp.strip() for comp in fertilizer_name.split('+')]
    component_details = []
    total_cost = 0.0
    total_quantity = 0.0
    
    for component in components:
        # Calculate quantity for each component
        quantity = calculate_fertilizer_quantity(
            component,
            field_size,
            nutrient_status,
            fertilizer_type
        )
        
        # Get price for each component
        price = get_price(component)
        
        # Calculate cost for this component
        cost = quantity * price
        
        component_details.append({
            "name": component,
            "quantity_kg": quantity,
            "price_per_kg": price,
            "cost": cost
        })
        
        total_cost += cost
        total_quantity += quantity
    
    return {
        "total_cost": total_cost,
        "total_quantity": total_quantity,
        "components": component_details
    }


def calculate_application_dates(sowing_date_str: str, crop_type: str = "default") -> Dict[str, str]:
    """
    Calculate precise fertilizer application dates based on crop growth stages.
    All timings are shown after sowing date.
    """
    try:
        sowing_date = datetime.fromisoformat(sowing_date_str)
    except:
        # Fallback to relative timing if date parsing fails
        return {
            "primary": "Apply at sowing (Day 0) and during early vegetative growth (Day 20-30)",
            "secondary": "Apply during active growth phase (Day 40-60)",
            "organics": "Apply at sowing (Day 0) or incorporate into soil before planting"
        }
    
    # Crop-specific growth stage durations (in days)
    crop_stages = {
        "rice": {"tillering": 20, "panicle_initiation": 45, "flowering": 75},
        "wheat": {"tillering": 25, "crown_root_initiation": 40, "jointing": 60},
        "maize": {"knee_high": 25, "tasseling": 50, "silking": 65},
        "barley": {"tillering": 25, "stem_extension": 40, "heading": 65},
        "jowar": {"vegetative": 30, "flag_leaf": 45, "flowering": 65},
        "bajra": {"vegetative": 25, "panicle_emergence": 40, "flowering": 55},
        "ragi": {"tillering": 20, "flag_leaf": 35, "flowering": 55},
        "groundnut": {"vegetative": 25, "flowering": 35, "pegging": 50},
        "mustard": {"vegetative": 25, "branching": 40, "flowering": 60},
        "soyabean": {"vegetative": 25, "flowering": 40, "pod_formation": 60},
        "sugarcane": {"tillering": 45, "grand_growth": 90, "elongation": 150},
        "cotton": {"vegetative": 35, "square_formation": 50, "flowering": 75},
        "chickpea": {"vegetative": 30, "branching": 45, "flowering": 65},
        "moong": {"vegetative": 20, "flowering": 30, "pod_formation": 45},
        "garlic": {"bulb_initiation": 30, "bulb_development": 60, "clove_formation": 90},
        "onion": {"vegetative": 30, "bulb_initiation": 50, "bulb_enlargement": 75},
        "default": {"vegetative": 30, "flowering": 60, "fruit_development": 90}
    }
    
    # Normalize crop name
    crop_normalized = crop_type.lower().strip()
    stages = crop_stages.get(crop_normalized, crop_stages["default"])
    
    # Get stage names and days
    stage_names = list(stages.keys())
    stage_days = list(stages.values())
    
    # Calculate application dates (all after sowing)
    at_sowing = sowing_date.strftime("%d %B %Y")
    first_stage = (sowing_date + timedelta(days=stage_days[0])).strftime("%d %B %Y")
    second_stage = (sowing_date + timedelta(days=stage_days[1])).strftime("%d %B %Y")
    third_stage = (sowing_date + timedelta(days=stage_days[2])).strftime("%d %B %Y")
    
    # Crop-specific notes
    crop_notes = {
        "rice": "For transplanted rice, give first dose 5-7 days after transplanting",
        "wheat": "Split nitrogen: Half at sowing, remaining in 2 doses later",
        "maize": "Give nitrogen fertilizer in 2-3 doses for best results",
        "barley": "Give most nitrogen at tillering time",
        "jowar": "Give nitrogen in 2 doses: Half at sowing, half at knee high stage",
        "bajra": "Give all P and K at sowing, nitrogen in splits",
        "ragi": "Give organic manures at sowing, chemical fertilizers in splits",
        "groundnut": "Don't give too much nitrogen; focus on phosphorus and potassium",
        "mustard": "Use sulphur fertilizers for better yield",
        "soyabean": "Use less nitrogen if seeds are treated with Rhizobium",
        "sugarcane": "Give fertilizers in 3-4 doses over 5-6 months",
        "cotton": "Give potassium during boll formation for better fiber quality",
        "chickpea": "Treat seeds with Rhizobium; give phosphorus at sowing",
        "moong": "Use Rhizobium culture; needs very little nitrogen",
        "garlic": "Give organic manure 7-10 days before planting; nitrogen in doses",
        "onion": "Give nitrogen in 3-4 doses; reduce when bulbs start forming"
    }
    
    crop_note = crop_notes.get(crop_normalized, "Give fertilizers in small doses for better results")
    
    return {
        "primary": f"At sowing: Apply on {at_sowing} (Day 0) | "
                  f"First dose: Apply at {stage_names[0].replace('_', ' ').title()} stage "
                  f"on {first_stage} (Day {stage_days[0]}) | "
                  f"Expert Tip: {crop_note} | "
                  f"Best Time: Early morning (6-8 AM) or evening (4-6 PM) | "
                  f"Weather: Avoid application on very hot days or just before heavy rain",
        
        "secondary": f"Recommended: Apply at {stage_names[1].replace('_', ' ').title()} stage "
                    f"on {second_stage} (Day {stage_days[1]}) | "
                    f"Alternative: You can also apply at {stage_names[2].replace('_', ' ').title()} stage "
                    f"on {third_stage} (Day {stage_days[2]}) if needed | "
                    f"Application Method: Mix with water for foliar spray or apply to soil and water immediately | "
                    f"Precaution: Don't apply during flowering stage unless specifically recommended",
        
        "organics": f"Best Time: Mix with soil when sowing on {at_sowing} (Day 0) | "
                   f"Even Better: Apply 7-10 days before sowing for better decomposition | "
                   f"Method: Mix well with soil at 6-8 inch (15-20 cm) depth | "
                   f"After Application: Water lightly to help decomposition | "
                   f"Benefits: Organic matter needs time to break down and release nutrients slowly"
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
    'potassium_nitrate': 75,
    'potassium_carbonate': 90,
    'potassium_magnesium_sulphate': 85,
    'balanced_npk_maintenance': 100,
    'ammonium_chloride': 160,

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
    ml_prediction: MLPrediction,
    secondary_fertilizer: str
) -> str:
    """Generate comprehensive prompt for Gemini API"""
    
    prompt = f"""You are an expert agricultural consultant specializing in fertilizer recommendations for Indian farmers.

Based on the following information, provide detailed recommendations:

**Soil and Environmental Data:**
- Soil Temperature: {input_data.soil_temperature}°C
- Soil Moisture: {input_data.soil_moisture}%
- Soil Type: {input_data.soil_type}
- Soil pH: {input_data.ph}
- EC (Electrical Conductivity): {input_data.ec} mmhos/cm²

**Soil Nutrient Levels (mg/kg):**
- Nitrogen (N): {input_data.nitrogen} mg/kg
- Phosphorus (P): {input_data.phosphorus} mg/kg
- Potassium (K): {input_data.potassium} mg/kg

**Crop Information:**
- Crop Type: {input_data.crop_type}
- Sowing Date: {input_data.sowing_date}
- Field Size: {input_data.field_size} hectares

**ML Model Predictions:**
- Nitrogen Status: {ml_prediction.n_status}
- Phosphorus Status: {ml_prediction.p_status}
- Potassium Status: {ml_prediction.k_status}
- Primary Fertilizer Recommended: {ml_prediction.primary_fertilizer}
- Secondary Fertilizer Recommended: {secondary_fertilizer}
- pH Amendment: {ml_prediction.ph_amendment}

**Task:**
Provide recommendations in the following JSON format:

{{
    "primary_fertilizer": {{
        "name": "{ml_prediction.primary_fertilizer}",
        "npk": "Provide NPK ratio like 46-0-0 for Urea",
        "reason": "Explain why this fertilizer is recommended based on soil nutrient levels (mention the mg/kg values of N:{input_data.nitrogen}, P:{input_data.phosphorus}, K:{input_data.potassium}) and the deficiency status (N:{ml_prediction.n_status}, P:{ml_prediction.p_status}, K:{ml_prediction.k_status})",
        "nutrients_provided": "Clearly list the specific nutrients this fertilizer provides (e.g., 'High Nitrogen (46% N)' for Urea, or 'Nitrogen (18%) and Phosphorus (46%)' for DAP) and their concentration percentages",
        "benefits": "Explain in 2-3 sentences how this fertilizer helps the {input_data.crop_type} crop: what plant processes it supports (e.g., vegetative growth, root development, flowering), what visible improvements the farmer will see (e.g., greener leaves, stronger stems, better yields), and why it's important for this specific crop and soil condition"
    }},
    "secondary_fertilizer": {{
        "name": "{secondary_fertilizer}",
        "reason": "Explain why this secondary/micronutrient fertilizer is needed based on soil analysis and what specific deficiency it addresses",
        "nutrients_provided": "List the specific micronutrients provided (e.g., 'Zinc (21% Zn)', 'Boron (11% B)', 'Iron (19% Fe)') with their concentrations",
        "benefits": "Explain how these micronutrients help: their role in plant metabolism, enzyme activation, disease resistance, flowering, fruit set, and overall crop quality. Be specific about visible benefits for {input_data.crop_type}"
    }},
    "organic_alternatives": [
        {{
            "name": "Select ONE organic fertilizer from this list that best addresses the SPECIFIC nutrient deficiencies (N:{ml_prediction.n_status}, P:{ml_prediction.p_status}, K:{ml_prediction.k_status}) for {input_data.crop_type} in {input_data.soil_type} soil: {', '.join(ORGANIC_ALTERNATIVES)}",
            "quantity_kg": "Calculate realistic quantity for {input_data.field_size} hectares based on the selected organic fertilizer's typical application rate and current soil nutrient levels (N:{input_data.nitrogen} mg/kg, P:{input_data.phosphorus} mg/kg, K:{input_data.potassium} mg/kg)",
            "npk_content": "Provide the NPK ratio (e.g., 1.5-1.0-1.5)",
            "primary_nutrients": "List primary nutrients provided (e.g., ['Nitrogen', 'Phosphorus', 'Potassium'])",
            "benefits": "Explain specific benefits: why use this fertilizer, what problems it solves, and its unique advantages for {input_data.crop_type}",
            "reason": "Explain specifically how this addresses the nutrient status (N:{ml_prediction.n_status}, P:{ml_prediction.p_status}, K:{ml_prediction.k_status}) and why it's suitable for {input_data.crop_type} in {input_data.soil_type} soil",
            "timing": "Specify timing based on sowing date ({input_data.sowing_date}) and crop growth stages for {input_data.crop_type}"
        }},
        {{
            "name": "Select a DIFFERENT organic fertilizer that complements the primary fertilizer ({ml_prediction.primary_fertilizer}) and addresses secondary needs. Choose from: {', '.join(ORGANIC_ALTERNATIVES)}",
            "quantity_kg": "Calculate quantity considering field size ({input_data.field_size} ha) and the fact that it's supplementing {ml_prediction.primary_fertilizer}",
            "npk_content": "Provide the NPK ratio",
            "primary_nutrients": "List primary nutrients provided",
            "benefits": "Explain specific benefits and why this fertilizer is recommended for this situation",
            "reason": "Explain how this complements {ml_prediction.primary_fertilizer} and {secondary_fertilizer}",
            "timing": "Provide specific timing that suits {input_data.crop_type} cultivation"
        }},
        {{
            "name": "Select a THIRD distinct organic option for long-term soil health. Must be different from previous two. Choose from: {', '.join(ORGANIC_ALTERNATIVES)}",
            "quantity_kg": "Calculate based on {input_data.field_size} hectares and soil improvement needs",
            "npk_content": "Provide the NPK ratio",
            "primary_nutrients": "List primary nutrients provided",
            "benefits": "Explain specific benefits focusing on long-term soil health, conditioning, and overall crop productivity",
            "reason": "Focus on long-term soil conditioning benefits for {input_data.soil_type} soil",
            "timing": "Suggest optimal application timing for maximum soil conditioning benefits"
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
2. Each organic alternative must be DIFFERENT and specifically chosen based on:
   - Current NPK status: N={ml_prediction.n_status}, P={ml_prediction.p_status}, K={ml_prediction.k_status}
   - Soil nutrient levels: N={input_data.nitrogen} mg/kg, P={input_data.phosphorus} mg/kg, K={input_data.potassium} mg/kg
   - Soil type: {input_data.soil_type}
   - Crop type: {input_data.crop_type}
   - Soil conditions: pH={input_data.ph}, EC={input_data.ec}, Temp={input_data.soil_temperature}°C, Moisture={input_data.soil_moisture}%
   - Primary fertilizer being used: {ml_prediction.primary_fertilizer}
   - Secondary fertilizer being used: {secondary_fertilizer}
   - pH amendment needed: {ml_prediction.ph_amendment}
3. Calculate quantities based on actual field size ({input_data.field_size} hectares) and typical application rates
4. Provide distinct reasons for each organic alternative - don't repeat generic statements
5. Consider how each organic fertilizer addresses specific deficiencies or soil conditions
6. Timing should be specific to {input_data.crop_type} growth stages and soil temperature
7. Return ONLY valid JSON, no additional text
"""
    
    return prompt


# ==================================================================================
# MAIN RECOMMENDATION GENERATION FUNCTION
# ==================================================================================
def generate_enhanced_recommendation(
    input_data: InputData,
    ml_prediction: MLPrediction,
    secondary_fertilizer: str,
    confidence_scores: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """
    Generate comprehensive fertilizer recommendation using Gemini API
    
    Args:
        input_data: User input data
        ml_prediction: ML model predictions
        secondary_fertilizer: Secondary fertilizer from secondary_fertilizer_model.py
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
        return generate_fallback_recommendation(input_data, ml_prediction, secondary_fertilizer, confidence_scores)
    
    # Generate prompt
    prompt = generate_gemini_prompt(input_data, ml_prediction, secondary_fertilizer)
    
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
        return generate_fallback_recommendation(input_data, ml_prediction, secondary_fertilizer, confidence_scores)
    
    # Calculate quantities and costs
    print("💰 Calculating quantities and costs...")
    
    # Primary fertilizer
    print(f"🔍 Primary fertilizer from ML: '{ml_prediction.primary_fertilizer}'")
    primary_quantity = calculate_fertilizer_quantity(
        ml_prediction.primary_fertilizer,
        input_data.field_size,
        ml_prediction.n_status,
        "primary"
    )
    primary_price_per_kg = get_price(ml_prediction.primary_fertilizer)
    primary_cost = primary_quantity * primary_price_per_kg
    print(f"   Normalized name: '{normalize_fertilizer_name(ml_prediction.primary_fertilizer)}'")
    print(f"   Quantity: {primary_quantity} kg, Price: ₹{primary_price_per_kg}/kg, Total: ₹{primary_cost:.2f}")
    
    # Secondary fertilizer
    print(f"🔍 Secondary fertilizer from model: '{secondary_fertilizer}'")
    secondary_result = calculate_compound_fertilizer_cost(
        secondary_fertilizer,
        input_data.field_size,
        ml_prediction.k_status,
        "secondary"
    )
    secondary_cost = secondary_result["total_cost"]
    secondary_quantity = secondary_result["total_quantity"]
    secondary_components = secondary_result["components"]
    
    # Print detailed breakdown
    print(f"   Total quantity: {secondary_quantity} kg, Total cost: ₹{secondary_cost:.2f}")
    if len(secondary_components) > 1:
        print(f"   Component breakdown:")
        for comp in secondary_components:
            print(f"     - {comp['name']}: {comp['quantity_kg']} kg × ₹{comp['price_per_kg']}/kg = ₹{comp['cost']:.2f}")
    else:
        print(f"   Normalized name: '{normalize_fertilizer_name(secondary_fertilizer)}'")
        if secondary_components:
            print(f"   Price: ₹{secondary_components[0]['price_per_kg']}/kg")
    
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
        
        # Get nutrient info from database
        nutrient_info = ORGANIC_NUTRIENTS.get(org_name, {})
        
        organic_details.append({
            "name": org_name,
            "amount_kg": org_quantity,
            "price_per_kg": org_price,
            "cost": org_cost,
            "npk_content": org.get("npk_content", nutrient_info.get("npk", "N/A")),
            "primary_nutrients": org.get("primary_nutrients", nutrient_info.get("primary_nutrients", [])),
            "benefits": org.get("benefits", nutrient_info.get("benefits", "Provides organic nutrition and improves soil health")),
            "reason": org.get("reason", ""),
            "timing": org.get("timing", "")
        })
    
    total_organic_cost = sum(organic_costs)
    total_cost = primary_cost + secondary_cost + total_organic_cost
    
    # Calculate application timing
    application_timing = calculate_application_dates(input_data.sowing_date, input_data.crop_type)
    
    # Calculate average confidence
    if confidence_scores:
        avg_confidence = sum(confidence_scores.values()) / len(confidence_scores)
        confidence_percent = int(avg_confidence * 100)
    else:
        confidence_percent = 90  # Default
    
    # Determine nutrient deficiencies
    nutrient_deficiencies_primary = []
    nutrient_deficiencies_secondary = []
    
    if ml_prediction.n_status.lower() == "low":
        nutrient_deficiencies_primary.append("Nitrogen")
    if ml_prediction.p_status.lower() == "low":
        nutrient_deficiencies_primary.append("Phosphorus")
    if ml_prediction.k_status.lower() == "low":
        nutrient_deficiencies_primary.append("Potassium")
    
    # Secondary deficiencies based on secondary fertilizer recommendation
    if secondary_fertilizer and secondary_fertilizer not in ['—', 'None', 'NA']:
        if 'zinc' in secondary_fertilizer.lower():
            nutrient_deficiencies_secondary.append("Zinc")
        if 'boron' in secondary_fertilizer.lower() or 'borax' in secondary_fertilizer.lower():
            nutrient_deficiencies_secondary.append("Boron")
        if 'manganese' in secondary_fertilizer.lower():
            nutrient_deficiencies_secondary.append("Manganese")
        if 'iron' in secondary_fertilizer.lower() or 'ferrous' in secondary_fertilizer.lower():
            nutrient_deficiencies_secondary.append("Iron")
        if 'magnesium' in secondary_fertilizer.lower():
            nutrient_deficiencies_secondary.append("Magnesium")
    
    # Build comprehensive report
    report = {
        "soil_condition_analysis": {
            "current_status": {
                "N_status": ml_prediction.n_status,
                "P_status": ml_prediction.p_status,
                "K_status": ml_prediction.k_status,
                "pH_status": "Optimal" if abs(input_data.ph - 6.5) < 0.5 else ("Acidic" if input_data.ph < 6.0 else "Alkaline"),
                "moisture_status": "Optimal" if 40 <= input_data.soil_moisture <= 70 else ("Low" if input_data.soil_moisture < 40 else "High"),
                "nutrient_deficiencies_primary": nutrient_deficiencies_primary,
                "nutrient_deficiencies_secondary": nutrient_deficiencies_secondary
            },
            "soil_test_values": {
                "nitrogen_mg_kg": input_data.nitrogen,
                "phosphorus_mg_kg": input_data.phosphorus,
                "potassium_mg_kg": input_data.potassium,
                "pH": input_data.ph,
                "EC_mmhos_cm2": input_data.ec,
                "soil_temperature": input_data.soil_temperature,
                "soil_moisture": input_data.soil_moisture
            },
            "recommendations": gemini_data.get("soil_recommendations", [])
        },
        
        "primary_fertilizer": {
            "name": ml_prediction.primary_fertilizer,
            "amount_kg": primary_quantity,
            "npk": gemini_data.get("primary_fertilizer", {}).get("npk", "—"),
            "reason": gemini_data.get("primary_fertilizer", {}).get("reason", ""),
            "nutrients_provided": gemini_data.get("primary_fertilizer", {}).get("nutrients_provided", ""),
            "benefits": gemini_data.get("primary_fertilizer", {}).get("benefits", "")
        },
        
        "secondary_fertilizer": {
            "name": secondary_fertilizer if secondary_fertilizer not in ['—', 'None', 'NA'] else "Not required",
            "amount_kg": secondary_quantity,
            "reason": gemini_data.get("secondary_fertilizer", {}).get("reason", ""),
            "nutrients_provided": gemini_data.get("secondary_fertilizer", {}).get("nutrients_provided", ""),
            "benefits": gemini_data.get("secondary_fertilizer", {}).get("benefits", "")
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
                    "fertilizer": secondary_fertilizer,
                    "quantity_kg": secondary_quantity,
                    "total": f"₹{int(secondary_cost):,}",
                    "components": [
                        {
                            "name": comp["name"],
                            "quantity_kg": comp["quantity_kg"],
                            "price_per_kg": f"₹{comp['price_per_kg']:.2f}",
                            "cost": f"₹{int(comp['cost']):,}"
                        }
                        for comp in secondary_components
                    ]
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
            "crop_type": input_data.crop_type,
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
    secondary_fertilizer: str,
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
    
    # Use compound fertilizer calculation for secondary
    secondary_result = calculate_compound_fertilizer_cost(
        secondary_fertilizer,
        input_data.field_size,
        ml_prediction.k_status,
        "secondary"
    )
    secondary_cost = secondary_result["total_cost"]
    secondary_quantity = secondary_result["total_quantity"]
    secondary_components = secondary_result["components"]
    
    # Select organic alternatives based on soil conditions and crop type
    organic_alternatives_map = {
        # For nitrogen deficiency
        ("low", "n"): ["Poultry manure", "Farmyard manure (FYM)", "Green manure"],
        # For phosphorus deficiency
        ("low", "p"): ["Bone meal", "PSB (Phosphate Solubilizing Bacteria)", "Mustard cake"],
        # For potassium deficiency
        ("low", "k"): ["Banana wastes", "Compost", "Seaweed extract"],
        # For high nitrogen
        ("high", "n"): ["Compost", "Mulch", "Azolla"],
        # For balanced/optimal conditions
        ("optimal", "general"): ["Vermicompost", "Neem cake", "Compost"],
        # For clay soils
        ("clay", "soil"): ["Compost", "Mulch", "Vermicompost"],
        # For sandy soils
        ("sandy", "soil"): ["Farmyard manure (FYM)", "Vermicompost", "Green manure"],
        # For loamy soils
        ("loamy", "soil"): ["Neem cake", "Compost", "Poultry manure"],
        # For alluvial soils
        ("alluvial", "soil"): ["Vermicompost", "Mustard cake", "Bone meal"],
        # For red soils
        ("red", "soil"): ["Green manure", "Compost", "Bone meal"],
        # For black soils
        ("black", "soil"): ["Farmyard manure (FYM)", "Compost", "Neem cake"],
    }
    
    # Determine which organic alternatives to use based on nutrient status
    selected_organics = []
    
    # Check N status first
    if ml_prediction.n_status.lower() == "low":
        selected_organics.extend(organic_alternatives_map.get(("low", "n"), [])[:1])
    elif ml_prediction.n_status.lower() == "high":
        selected_organics.extend(organic_alternatives_map.get(("high", "n"), [])[:1])
    
    # Check P status
    if ml_prediction.p_status.lower() == "low":
        selected_organics.extend(organic_alternatives_map.get(("low", "p"), [])[:1])
    
    # Check K status
    if ml_prediction.k_status.lower() == "low":
        selected_organics.extend(organic_alternatives_map.get(("low", "k"), [])[:1])
    
    # Prioritize soil type specific organics - add all 3 from soil type list
    soil_key = (input_data.soil_type.lower(), "soil")
    if soil_key in organic_alternatives_map:
        soil_organics = organic_alternatives_map[soil_key]
        for org in soil_organics:
            if len(selected_organics) >= 3:
                break
            if org not in selected_organics:
                selected_organics.append(org)
    
    # If we still don't have enough, add from optimal list
    optimal_organics = organic_alternatives_map.get(("optimal", "general"), ["Vermicompost", "Neem cake", "Compost"])
    for org in optimal_organics:
        if len(selected_organics) >= 3:
            break
        if org not in selected_organics:
            selected_organics.append(org)
    
    # Ensure we have exactly 3 unique organic alternatives
    selected_organics = list(dict.fromkeys(selected_organics))[:3]
    if len(selected_organics) < 3:
        all_organics = ["Vermicompost", "Neem cake", "Compost", "Farmyard manure (FYM)", "Poultry manure"]
        for org in all_organics:
            if len(selected_organics) >= 3:
                break
            if org not in selected_organics:
                selected_organics.append(org)
    
    organic_details = []
    organic_costs = []
    
    for org_name in selected_organics:
        org_quantity = calculate_fertilizer_quantity(org_name, input_data.field_size, "optimal", "organic")
        org_price = get_price(org_name)
        org_cost = org_quantity * org_price
        organic_costs.append(org_cost)
        
        # Generate specific reason based on nutrient status and soil conditions
        reasons = []
        if ml_prediction.n_status.lower() == "low" and org_name in organic_alternatives_map.get(("low", "n"), []):
            reasons.append(f"Addresses nitrogen deficiency (current: {input_data.nitrogen} mg/kg)")
        if ml_prediction.p_status.lower() == "low" and org_name in organic_alternatives_map.get(("low", "p"), []):
            reasons.append(f"Provides phosphorus for {input_data.crop_type} (current: {input_data.phosphorus} mg/kg)")
        if ml_prediction.k_status.lower() == "low" and org_name in organic_alternatives_map.get(("low", "k"), []):
            reasons.append(f"Supplements potassium levels (current: {input_data.potassium} mg/kg)")
        
        if not reasons:
            reasons.append(f"Improves soil structure for {input_data.soil_type} soil growing {input_data.crop_type}")
            if input_data.soil_moisture < 40:
                reasons.append("Helps retain moisture")
            elif input_data.ec > 2.0:
                reasons.append("Helps reduce soil salinity")
        
        # Get nutrient info from database
        nutrient_info = ORGANIC_NUTRIENTS.get(org_name, {})
        
        organic_details.append({
            "name": org_name,
            "amount_kg": org_quantity,
            "price_per_kg": org_price,
            "cost": org_cost,
            "npk_content": nutrient_info.get("npk", "N/A"),
            "primary_nutrients": nutrient_info.get("primary_nutrients", []),
            "benefits": nutrient_info.get("benefits", "Provides organic nutrition and improves soil health"),
            "reason": "; ".join(reasons),
            "timing": f"Apply 3-4 weeks before sowing (considering {input_data.crop_type} cultivation and soil temp: {input_data.soil_temperature}°C)"
        })
    
    # Calculate costs
    primary_price = get_price(ml_prediction.primary_fertilizer)
    
    primary_cost = primary_quantity * primary_price
    # secondary_cost already calculated in secondary_result
    total_organic_cost = sum(organic_costs)
    total_cost = primary_cost + secondary_cost + total_organic_cost
    
    # Application timing
    application_timing = calculate_application_dates(input_data.sowing_date, input_data.crop_type)
    
    # Build basic report
    report = {
        "soil_condition_analysis": {
            "current_status": {
                "N_status": ml_prediction.n_status,
                "P_status": ml_prediction.p_status,
                "K_status": ml_prediction.k_status,
                "pH_status": "Optimal" if abs(input_data.ph - 6.5) < 0.5 else "Needs adjustment",
                "moisture_status": "Optimal" if 40 <= input_data.soil_moisture <= 70 else ("Low" if input_data.soil_moisture < 40 else "High"),
                "nutrient_deficiencies_primary": [],
                "nutrient_deficiencies_secondary": []
            },
            "soil_test_values": {
                "nitrogen_mg_kg": input_data.nitrogen,
                "phosphorus_mg_kg": input_data.phosphorus,
                "potassium_mg_kg": input_data.potassium,
                "pH": input_data.ph,
                "EC_mmhos_cm2": input_data.ec,
                "soil_temperature": input_data.soil_temperature,
                "soil_moisture": input_data.soil_moisture
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
            "reason": f"Recommended based on {ml_prediction.n_status} nitrogen status (N: {input_data.nitrogen} mg/kg, P: {input_data.phosphorus} mg/kg, K: {input_data.potassium} mg/kg)",
            "nutrients_provided": get_fertilizer_nutrients(ml_prediction.primary_fertilizer),
            "benefits": f"Addresses nutrient deficiency in {input_data.crop_type}, promotes healthy growth, and improves yield potential based on {input_data.soil_type} soil conditions"
        },
        "secondary_fertilizer": {
            "name": secondary_fertilizer,
            "amount_kg": secondary_quantity,
            "reason": f"Addresses micronutrient deficiencies based on soil analysis for {input_data.crop_type}",
            "nutrients_provided": get_secondary_nutrients(secondary_fertilizer),
            "benefits": "Improves enzyme activation, enhances disease resistance, promotes better flowering and fruit set, and prevents micronutrient deficiency symptoms"
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
            "field_size": f"For {input_data.field_size:.2f} hectares",
            "breakdown": {
                "primary": {
                    "fertilizer": ml_prediction.primary_fertilizer,
                    "quantity_kg": primary_quantity,
                    "price_per_kg": f"₹{primary_price:.2f}",
                    "total": f"₹{int(primary_cost):,}"
                },
                "secondary": {
                    "fertilizer": secondary_fertilizer,
                    "quantity_kg": secondary_quantity,
                    "total": f"₹{int(secondary_cost):,}",
                    "components": [
                        {
                            "name": comp["name"],
                            "quantity_kg": comp["quantity_kg"],
                            "price_per_kg": f"₹{comp['price_per_kg']:.2f}",
                            "cost": f"₹{int(comp['cost']):,}"
                        }
                        for comp in secondary_components
                    ]
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
            "model_used": "ML Stacking Model (Intelligent Fallback - Crop & Soil Specific)",
            "nutrient_units": "mg/kg",
            "crop_type": input_data.crop_type,
            "soil_type": input_data.soil_type,
            "npk_status": f"N:{ml_prediction.n_status}, P:{ml_prediction.p_status}, K:{ml_prediction.k_status}",
            "note": "Organic alternatives selected based on NPK status, soil type, and crop requirements"
        }
    }
    
    return report


# ==================================================================================
# EXAMPLE USAGE
# ==================================================================================
if __name__ == "__main__":
    # Example: Load ML predictions from your stacking model
    # This would come from fertilizer_ml_model.py
    
    # Sample input data
    sample_input = InputData(
        nitrogen=180.0,  # mg/kg
        phosphorus=25.0,  # mg/kg
        potassium=150.0,  # mg/kg
        ph=6.8,
        ec=0.45,
        soil_temperature=28.5,  # °C
        soil_moisture=55.0,  # %
        soil_type="Loamy",
        crop_type="Wheat",
        sowing_date="2025-11-15",
        field_size=2.27  # hectares (approx 5.6 acres)
    )
    
    # Sample ML predictions
    sample_prediction = MLPrediction(
        n_status="Optimal",
        p_status="Low",
        k_status="Optimal",
        primary_fertilizer="Urea",
        ph_amendment="None"
    )
    
    # Sample secondary fertilizer (from secondary_fertilizer_model.py)
    sample_secondary_fertilizer = "Zinc Sulphate"
    
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
            secondary_fertilizer=sample_secondary_fertilizer,
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