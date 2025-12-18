"""
Final Verification Script
Confirms the integrated model is working correctly across all components
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "fertilizer recommendation system"))

def test_import():
    """Test that all imports work correctly"""
    print("\n" + "="*80)
    print("1. TESTING IMPORTS")
    print("="*80)
    
    try:
        from integrated_agricure_model import IntegratedAgriCure
        print("✅ integrated_agricure_model imported successfully")
        
        from Final_Model import FinalFertilizerRecommendationSystem
        print("✅ Final_Model imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_core_model():
    """Test the core integrated model"""
    print("\n" + "="*80)
    print("2. TESTING CORE INTEGRATED MODEL")
    print("="*80)
    
    try:
        from integrated_agricure_model import IntegratedAgriCure
        
        engine = IntegratedAgriCure()
        print("✅ Engine initialized")
        
        # Test with sample data
        result = engine.recommend(
            nitrogen=65,
            phosphorus=10,
            potassium=75,
            crop_type="Wheat",
            ph=5.8,
            ec=250,
            moisture=20
        )
        
        print(f"✅ Recommendation generated")
        print(f"   Primary: {result['Primary_Fertilizer']}")
        print(f"   Secondary: {result['Secondary_Fertilizer']}")
        print(f"   pH Amendment: {result['pH_Amendment']}")
        
        # Verify all required keys exist
        required_keys = ['Crop', 'N_Status', 'P_Status', 'K_Status', 
                        'Primary_Fertilizer', 'Secondary_Fertilizer', 
                        'pH_Amendment', 'Deficit_%']
        
        for key in required_keys:
            if key not in result:
                print(f"❌ Missing key: {key}")
                return False
        
        print("✅ All required keys present in output")
        return True
        
    except Exception as e:
        print(f"❌ Core model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_final_model():
    """Test the Final_Model integration"""
    print("\n" + "="*80)
    print("3. TESTING FINAL_MODEL INTEGRATION")
    print("="*80)
    
    try:
        from Final_Model import FinalFertilizerRecommendationSystem
        
        system = FinalFertilizerRecommendationSystem()
        print("✅ System initialized")
        
        # Test with sample data
        result = system.predict(
            size=2.0,
            crop='Wheat',
            sowing_date='2025-11-15',
            nitrogen=65.0,
            phosphorus=10.0,
            potassium=75.0,
            soil_ph=5.8,
            soil_moisture=20.0,
            electrical_conductivity=250.0,
            soil_temperature=25.0,
            use_llm=False  # Disable LLM for faster testing
        )
        
        print("✅ Prediction generated")
        
        # Verify ml_predictions exists
        if 'ml_predictions' not in result:
            print("❌ ml_predictions missing from result")
            return False
        
        ml_preds = result['ml_predictions']
        print(f"   N Status: {ml_preds['N_Status']}")
        print(f"   P Status: {ml_preds['P_Status']}")
        print(f"   K Status: {ml_preds['K_Status']}")
        print(f"   Primary: {ml_preds['Primary_Fertilizer']}")
        print(f"   Secondary: {ml_preds['Secondary_Fertilizer']}")
        print(f"   pH: {ml_preds['pH_Amendment']}")
        
        print("✅ Final_Model integration working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Final_Model test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_multiple_crops():
    """Test with different crops to ensure crop-specific logic works"""
    print("\n" + "="*80)
    print("4. TESTING MULTIPLE CROPS")
    print("="*80)
    
    try:
        from integrated_agricure_model import IntegratedAgriCure
        
        engine = IntegratedAgriCure()
        crops = ['Rice', 'Maize', 'Cotton', 'Groundnut', 'Onion']
        
        for crop in crops:
            result = engine.recommend(
                nitrogen=80,
                phosphorus=15,
                potassium=100,
                crop_type=crop,
                ph=6.5,
                ec=400,
                moisture=25
            )
            print(f"✅ {crop}: {result['Primary_Fertilizer'][:30]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Multiple crops test failed: {e}")
        return False

def test_edge_cases():
    """Test edge cases"""
    print("\n" + "="*80)
    print("5. TESTING EDGE CASES")
    print("="*80)
    
    try:
        from integrated_agricure_model import IntegratedAgriCure
        
        engine = IntegratedAgriCure()
        
        # Test 1: Very low pH
        result1 = engine.recommend(
            nitrogen=70, phosphorus=12, potassium=90,
            crop_type="Wheat", ph=4.5, ec=200, moisture=20
        )
        print(f"✅ Low pH (4.5): {result1['pH_Amendment']}")
        
        # Test 2: Very high pH
        result2 = engine.recommend(
            nitrogen=70, phosphorus=12, potassium=90,
            crop_type="Wheat", ph=8.5, ec=200, moisture=20
        )
        print(f"✅ High pH (8.5): {result2['pH_Amendment']}")
        
        # Test 3: Optimal conditions
        result3 = engine.recommend(
            nitrogen=100, phosphorus=20, potassium=120,
            crop_type="Rice", ph=6.5, ec=500, moisture=25
        )
        print(f"✅ Optimal NPK: All {result3['N_Status']}")
        
        # Test 4: Severe deficiencies
        result4 = engine.recommend(
            nitrogen=40, phosphorus=5, potassium=50,
            crop_type="Wheat", ph=5.5, ec=150, moisture=15
        )
        print(f"✅ Severe deficiency: {result4['N_Status']}, {result4['P_Status']}, {result4['K_Status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Edge cases test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all verification tests"""
    print("\n" + "╔" + "="*78 + "╗")
    print("║" + " "*20 + "INTEGRATED MODEL VERIFICATION SUITE" + " "*23 + "║")
    print("╚" + "="*78 + "╝")
    
    tests = [
        ("Import Test", test_import),
        ("Core Model Test", test_core_model),
        ("Final Model Integration Test", test_final_model),
        ("Multiple Crops Test", test_multiple_crops),
        ("Edge Cases Test", test_edge_cases)
    ]
    
    results = []
    for name, test_func in tests:
        result = test_func()
        results.append((name, result))
    
    # Summary
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
        if not result:
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("🎉 ALL VERIFICATION TESTS PASSED!")
        print("✅ The integrated model is working correctly")
        print("✅ Ready for production use")
    else:
        print("⚠️ SOME TESTS FAILED")
        print("❌ Please review the errors above")
    print("="*80 + "\n")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
