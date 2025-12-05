"""
Test script to verify compound fertilizer cost calculation fix
"""

from LLM_model import calculate_compound_fertilizer_cost, get_price, normalize_fertilizer_name

def test_single_fertilizer():
    """Test single fertilizer (should work same as before)"""
    print("=" * 70)
    print("TEST 1: Single Fertilizer - Borax")
    print("=" * 70)
    
    result = calculate_compound_fertilizer_cost(
        fertilizer_name="Borax",
        field_size=2.5,
        nutrient_status="Low",
        fertilizer_type="secondary"
    )
    
    print(f"Fertilizer: Borax")
    print(f"Total Quantity: {result['total_quantity']} kg")
    print(f"Total Cost: ₹{result['total_cost']:.2f}")
    print(f"Number of Components: {len(result['components'])}")
    print(f"Components:")
    for comp in result['components']:
        print(f"  - {comp['name']}: {comp['quantity_kg']} kg × ₹{comp['price_per_kg']}/kg = ₹{comp['cost']:.2f}")
    print()


def test_compound_fertilizer():
    """Test compound fertilizer (THIS IS THE BUG FIX)"""
    print("=" * 70)
    print("TEST 2: Compound Fertilizer - Borax + Ferrous Sulphate + Zinc Sulphate")
    print("=" * 70)
    
    result = calculate_compound_fertilizer_cost(
        fertilizer_name="Borax + Ferrous Sulphate + Zinc Sulphate",
        field_size=2.5,
        nutrient_status="Low",
        fertilizer_type="secondary"
    )
    
    print(f"Fertilizer: Borax + Ferrous Sulphate + Zinc Sulphate")
    print(f"Total Quantity: {result['total_quantity']} kg")
    print(f"Total Cost: ₹{result['total_cost']:.2f}")
    print(f"Number of Components: {len(result['components'])}")
    print(f"\nComponent Breakdown:")
    for comp in result['components']:
        print(f"  - {comp['name']}: {comp['quantity_kg']} kg × ₹{comp['price_per_kg']}/kg = ₹{comp['cost']:.2f}")
    
    print(f"\n✅ EXPECTED: Total cost should be sum of all three components")
    print(f"✅ ACTUAL: Total cost = ₹{result['total_cost']:.2f}")
    print()


def test_price_lookup():
    """Test individual price lookups"""
    print("=" * 70)
    print("TEST 3: Individual Price Lookups")
    print("=" * 70)
    
    fertilizers = ["Borax", "Ferrous Sulphate", "Zinc Sulphate"]
    
    for fert in fertilizers:
        price = get_price(fert)
        normalized = normalize_fertilizer_name(fert)
        print(f"{fert}:")
        print(f"  Normalized: {normalized}")
        print(f"  Price: ₹{price}/kg")
    print()


def test_old_vs_new():
    """Compare old method (wrong) vs new method (correct)"""
    print("=" * 70)
    print("TEST 4: Old Method vs New Method Comparison")
    print("=" * 70)
    
    compound = "Borax + Ferrous Sulphate + Zinc Sulphate"
    field_size = 2.5
    
    # New method (correct)
    result = calculate_compound_fertilizer_cost(
        fertilizer_name=compound,
        field_size=field_size,
        nutrient_status="Low",
        fertilizer_type="secondary"
    )
    
    # Simulate old method (only first component)
    old_normalized = normalize_fertilizer_name(compound)
    old_price = get_price(old_normalized)
    print(f"Old Method (BUG - only used first component):")
    print(f"  Normalized: {old_normalized}")
    print(f"  Price used: ₹{old_price}/kg")
    print(f"  Would have calculated cost for ONLY: {old_normalized}")
    
    print(f"\nNew Method (FIXED - uses all components):")
    print(f"  Total cost: ₹{result['total_cost']:.2f}")
    print(f"  Component breakdown:")
    for comp in result['components']:
        print(f"    - {comp['name']}: ₹{comp['cost']:.2f}")
    
    # Calculate what the old method would have given
    from LLM_model import calculate_fertilizer_quantity
    old_quantity = calculate_fertilizer_quantity(compound, field_size, "Low", "secondary")
    old_cost = old_quantity * old_price
    
    print(f"\n📊 COMPARISON:")
    print(f"  Old Method Total Cost (WRONG): ₹{old_cost:.2f}")
    print(f"  New Method Total Cost (CORRECT): ₹{result['total_cost']:.2f}")
    print(f"  Difference: ₹{result['total_cost'] - old_cost:.2f}")
    print(f"  Missing {result['total_cost'] / old_cost - 1:.1%} of the actual cost!")
    print()


if __name__ == "__main__":
    print("\n")
    print("🧪 COMPOUND FERTILIZER COST CALCULATION TEST")
    print("=" * 70)
    print("Testing the fix for compound fertilizer cost calculation bug")
    print("=" * 70)
    print()
    
    test_single_fertilizer()
    test_compound_fertilizer()
    test_price_lookup()
    test_old_vs_new()
    
    print("=" * 70)
    print("✅ ALL TESTS COMPLETE!")
    print("=" * 70)
    print()
