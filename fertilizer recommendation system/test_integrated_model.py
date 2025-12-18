"""
Test script to verify the Integrated AgriCure Model
"""

from integrated_agricure_model import IntegratedAgriCure

def test_scenario(name, params):
    """Test a specific scenario"""
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}")
    
    engine = IntegratedAgriCure()
    result = engine.recommend(**params)
    
    print(f"\nCrop: {result['Crop']}")
    print(f"NPK Status: N={result['N_Status']}, P={result['P_Status']}, K={result['K_Status']}")
    print(f"Primary Fertilizer: {result['Primary_Fertilizer']}")
    print(f"Secondary Fertilizer: {result['Secondary_Fertilizer']}")
    print(f"pH Amendment: {result['pH_Amendment']}")
    print(f"Deficit %: N={result['Deficit_%']['N']}%, P={result['Deficit_%']['P']}%, K={result['Deficit_%']['K']}%")
    
    return result

if __name__ == "__main__":
    print("\n" + "="*70)
    print("INTEGRATED AGRICURE MODEL - COMPREHENSIVE TEST SUITE")
    print("="*70)
    
    # Test 1: Severe deficiencies (Low NPK)
    test_scenario(
        "Severe NPK Deficiency - Wheat",
        {
            "nitrogen": 55,
            "phosphorus": 8,
            "potassium": 70,
            "crop_type": "Wheat",
            "ph": 5.3,
            "ec": 180,
            "moisture": 14
        }
    )
    
    # Test 2: Optimal conditions
    test_scenario(
        "Optimal Conditions - Rice",
        {
            "nitrogen": 100,
            "phosphorus": 20,
            "potassium": 120,
            "crop_type": "Rice",
            "ph": 6.5,
            "ec": 500,
            "moisture": 25
        }
    )
    
    # Test 3: High pH alkaline soil
    test_scenario(
        "Alkaline Soil - Maize",
        {
            "nitrogen": 80,
            "phosphorus": 12,
            "potassium": 90,
            "crop_type": "Maize",
            "ph": 8.2,
            "ec": 150,
            "moisture": 18
        }
    )
    
    # Test 4: Low pH acidic soil
    test_scenario(
        "Acidic Soil - Groundnut",
        {
            "nitrogen": 35,
            "phosphorus": 10,
            "potassium": 55,
            "crop_type": "Groundnut",
            "ph": 5.0,
            "ec": 300,
            "moisture": 20
        }
    )
    
    # Test 5: Single N deficiency
    test_scenario(
        "N Deficiency Only - Sugarcane",
        {
            "nitrogen": 100,
            "phosphorus": 20,
            "potassium": 150,
            "crop_type": "Sugarcane",
            "ph": 7.0,
            "ec": 400,
            "moisture": 30
        }
    )
    
    # Test 6: Onion with micronutrient needs
    test_scenario(
        "Onion with Specific Micronutrient Needs",
        {
            "nitrogen": 120,
            "phosphorus": 16,
            "potassium": 100,
            "crop_type": "Onion",
            "ph": 7.8,
            "ec": 150,
            "moisture": 12
        }
    )
    
    print("\n" + "="*70)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
    print("="*70 + "\n")
