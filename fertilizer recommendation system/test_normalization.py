#!/usr/bin/env python3
"""
Test fertilizer name normalization with ML model output
"""

# Test cases from the ML model dataset
test_cases = [
    "DAP (Di-Ammonium Phosphate)",
    "MAP (Mono-Ammonium Phosphate)",
    "MOP (Muriate of Potash)",
    "DAP (Di-Ammonium Phosphate) + MOP (Muriate of Potash)",
    "Urea + MOP (Muriate of Potash)",
    "Balanced NPK (14-14-14)",
    "SSP (Single Super Phosphate)",
    "TSP (Triple Super Phosphate)",
    "SOP (Sulphate of Potash)",
    "UAN (Urea Ammonium Nitrate)",
    "Urea",
    "Ammonium Nitrate",
    "Ammonium Sulphate",
    "Ammonium Chloride",
    "Rock Phosphate",
    "Potassium Nitrate",
    "Potassium Carbonate",
    "Potassium-Magnesium Sulphate"
]

# Import the normalize function
import sys
sys.path.append('.')
from LLM_model import normalize_fertilizer_name, get_price, DEFAULT_PRICES

print("=" * 80)
print("TESTING FERTILIZER NAME NORMALIZATION")
print("=" * 80)

for fertilizer in test_cases:
    normalized = normalize_fertilizer_name(fertilizer)
    price = get_price(fertilizer)
    in_prices = normalized in DEFAULT_PRICES if normalized else False
    
    print(f"\n📦 Original: '{fertilizer}'")
    print(f"   ✓ Normalized: '{normalized}'")
    print(f"   {'✓' if in_prices else '✗'} In DEFAULT_PRICES: {in_prices}")
    print(f"   💰 Price: ₹{price}/kg")
    
    if not in_prices and price == 0.0:
        print(f"   ⚠️ WARNING: No price found!")

print("\n" + "=" * 80)
print("TEST COMPLETE")
print("=" * 80)
