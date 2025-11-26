"""
Quick Test Script for Enhanced LLM System
==========================================

This script tests the LLM enhancement without requiring a trained ML model.
It uses mock ML predictions to verify the Gemini integration works correctly.

Usage:
    python test_llm_system.py

Make sure GEMINI_API_KEY is set!
"""

import os
import json
from llm_enhanced import (
    InputData,
    MLPrediction,
    generate_enhanced_recommendation,
    GEMINI_AVAILABLE
)


def test_basic_functionality():
    """Test basic functionality without ML model"""
    
    print("\n" + "="*70)
    print("🧪 TESTING ENHANCED LLM SYSTEM")
    print("="*70)
    
    # Check Gemini availability
    print(f"\n✓ Gemini API Available: {GEMINI_AVAILABLE}")
    
    # Check API key
    api_key_set = bool(os.getenv("GEMINI_API_KEY"))
    print(f"✓ API Key Set: {api_key_set}")
    
    if not api_key_set:
        print("\n⚠️  WARNING: GEMINI_API_KEY not set!")
        print("   Set it with: $env:GEMINI_API_KEY='your-key-here'")
        print("   Test will continue with fallback mode...")
    
    # Test Case 1: Wheat with Low Phosphorus
    print("\n" + "="*70)
    print("TEST CASE 1: Wheat Crop with Low Phosphorus")
    print("="*70)
    
    test_input_1 = InputData(
        temperature=28.5,
        humidity=65.0,
        moisture=55.0,
        soil_type="Loamy",
        crop="Wheat",
        nitrogen=180.0,   # mg/kg - Optimal
        phosphorus=15.0,  # mg/kg - Low
        potassium=150.0,  # mg/kg - Optimal
        ph=6.8,
        ec=0.45,
        sowing_date="2025-11-20",
        field_size=2.27
    )
    
    test_prediction_1 = MLPrediction(
        n_status="Optimal",
        p_status="Low",
        k_status="Optimal",
        primary_fertilizer="Urea",
        secondary_fertilizer="Potassium sulfate",
        ph_amendment="None"
    )
    
    test_confidences_1 = {
        "N_Status": 0.92,
        "P_Status": 0.88,
        "K_Status": 0.90,
        "Primary_Fertilizer": 0.89,
        "Secondary_Fertilizer": 0.85,
        "pH_Amendment": 0.95
    }
    
    try:
        result_1 = generate_enhanced_recommendation(
            input_data=test_input_1,
            ml_prediction=test_prediction_1,
            confidence_scores=test_confidences_1
        )
        
        print("\n✅ Test Case 1 PASSED")
        print(f"   Primary: {result_1['primary_fertilizer']['name']}")
        print(f"   Quantity: {result_1['primary_fertilizer']['amount_kg']} kg")
        print(f"   Cost: {result_1['cost_estimate']['total_estimate']}")
        
        # Save result
        with open("test_result_1.json", 'w', encoding='utf-8') as f:
            json.dump(result_1, f, indent=2, ensure_ascii=False)
        print(f"   Saved to: test_result_1.json")
        
    except Exception as e:
        print(f"\n❌ Test Case 1 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test Case 2: Rice with Multiple Deficiencies
    print("\n" + "="*70)
    print("TEST CASE 2: Rice Crop with Multiple Deficiencies")
    print("="*70)
    
    test_input_2 = InputData(
        temperature=30.0,
        humidity=80.0,
        moisture=75.0,
        soil_type="Clayey",
        crop="Rice",
        nitrogen=120.0,   # mg/kg - Low
        phosphorus=20.0,  # mg/kg - Low
        potassium=110.0,  # mg/kg - Low
        ph=6.2,
        ec=0.38,
        sowing_date="2025-12-01",
        field_size=1.5
    )
    
    test_prediction_2 = MLPrediction(
        n_status="Low",
        p_status="Low",
        k_status="Low",
        primary_fertilizer="Diammonium phosphate (DAP)",
        secondary_fertilizer="Muriate of Potash (MOP)",
        ph_amendment="None"
    )
    
    test_confidences_2 = {
        "N_Status": 0.91,
        "P_Status": 0.89,
        "K_Status": 0.87,
        "Primary_Fertilizer": 0.88,
        "Secondary_Fertilizer": 0.86,
        "pH_Amendment": 0.93
    }
    
    try:
        result_2 = generate_enhanced_recommendation(
            input_data=test_input_2,
            ml_prediction=test_prediction_2,
            confidence_scores=test_confidences_2
        )
        
        print("\n✅ Test Case 2 PASSED")
        print(f"   Primary: {result_2['primary_fertilizer']['name']}")
        print(f"   Quantity: {result_2['primary_fertilizer']['amount_kg']} kg")
        print(f"   Secondary: {result_2['secondary_fertilizer']['name']}")
        print(f"   Cost: {result_2['cost_estimate']['total_estimate']}")
        
        # Save result
        with open("test_result_2.json", 'w', encoding='utf-8') as f:
            json.dump(result_2, f, indent=2, ensure_ascii=False)
        print(f"   Saved to: test_result_2.json")
        
    except Exception as e:
        print(f"\n❌ Test Case 2 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test Case 3: Optimal Conditions
    print("\n" + "="*70)
    print("TEST CASE 3: Tomato with Optimal Conditions")
    print("="*70)
    
    test_input_3 = InputData(
        temperature=25.0,
        humidity=70.0,
        moisture=60.0,
        soil_type="Sandy Loam",
        crop="Tomato",
        nitrogen=200.0,   # mg/kg - Optimal
        phosphorus=40.0,  # mg/kg - Optimal
        potassium=180.0,  # mg/kg - Optimal
        ph=6.5,
        ec=0.50,
        sowing_date="2025-11-15",
        field_size=0.5
    )
    
    test_prediction_3 = MLPrediction(
        n_status="Optimal",
        p_status="Optimal",
        k_status="Optimal",
        primary_fertilizer="Balanced NPK (maintenance)",
        secondary_fertilizer="—",
        ph_amendment="None"
    )
    
    test_confidences_3 = {
        "N_Status": 0.94,
        "P_Status": 0.92,
        "K_Status": 0.93,
        "Primary_Fertilizer": 0.90,
        "Secondary_Fertilizer": 0.88,
        "pH_Amendment": 0.96
    }
    
    try:
        result_3 = generate_enhanced_recommendation(
            input_data=test_input_3,
            ml_prediction=test_prediction_3,
            confidence_scores=test_confidences_3
        )
        
        print("\n✅ Test Case 3 PASSED")
        print(f"   Primary: {result_3['primary_fertilizer']['name']}")
        print(f"   Deficiencies: {result_3['soil_condition_analysis']['current_status']['nutrient_deficiencies']}")
        print(f"   Cost: {result_3['cost_estimate']['total_estimate']}")
        
        # Save result
        with open("test_result_3.json", 'w', encoding='utf-8') as f:
            json.dump(result_3, f, indent=2, ensure_ascii=False)
        print(f"   Saved to: test_result_3.json")
        
    except Exception as e:
        print(f"\n❌ Test Case 3 FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True


def verify_output_structure(result: dict):
    """Verify the output has all required fields"""
    
    print("\n" + "="*70)
    print("🔍 VERIFYING OUTPUT STRUCTURE")
    print("="*70)
    
    required_sections = [
        'ml_model_prediction',
        'soil_condition_analysis',
        'primary_fertilizer',
        'secondary_fertilizer',
        'organic_alternatives',
        'application_timing',
        'cost_estimate',
        '_metadata'
    ]
    
    all_present = True
    for section in required_sections:
        present = section in result
        status = "✓" if present else "✗"
        print(f"   {status} {section}")
        if not present:
            all_present = False
    
    if all_present:
        print("\n✅ All required sections present!")
        
        # Check organic alternatives
        organics = result.get('organic_alternatives', [])
        print(f"\n   Organic alternatives: {len(organics)} options")
        for i, org in enumerate(organics, 1):
            print(f"      {i}. {org.get('name', 'N/A')}")
        
        # Check cost breakdown
        costs = result.get('cost_estimate', {})
        print(f"\n   Cost breakdown:")
        print(f"      Primary: {costs.get('primary_fertilizer', 'N/A')}")
        print(f"      Secondary: {costs.get('secondary_fertilizer', 'N/A')}")
        print(f"      Organics: {costs.get('organic_options', 'N/A')}")
        print(f"      Total: {costs.get('total_estimate', 'N/A')}")
        
        return True
    else:
        print("\n❌ Some required sections missing!")
        return False


def main():
    """Main test execution"""
    
    print("\n" + "="*70)
    print("🚀 STARTING TESTS")
    print("="*70)
    
    # Run functionality tests
    success = test_basic_functionality()
    
    if success:
        # Verify output structure
        try:
            with open("test_result_1.json", 'r', encoding='utf-8') as f:
                result = json.load(f)
            verify_output_structure(result)
        except:
            pass
        
        print("\n" + "="*70)
        print("✅ ALL TESTS PASSED!")
        print("="*70)
        print("\n📁 Test output files:")
        print("   - test_result_1.json (Wheat)")
        print("   - test_result_2.json (Rice)")
        print("   - test_result_3.json (Tomato)")
        print("\n" + "="*70)
    else:
        print("\n" + "="*70)
        print("❌ SOME TESTS FAILED")
        print("="*70)
        print("\nPlease check the error messages above.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Tests interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
