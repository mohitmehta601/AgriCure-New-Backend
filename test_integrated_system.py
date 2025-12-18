"""
Integration Test for the Complete System
Tests the API endpoints with the new Integrated AgriCure Model
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "fertilizer recommendation system"))

from Final_Model import FinalFertilizerRecommendationSystem
import json

def test_basic_recommendation():
    """Test basic fertilizer recommendation"""
    print("\n" + "="*80)
    print("TEST 1: Basic Fertilizer Recommendation")
    print("="*80)
    
    system = FinalFertilizerRecommendationSystem()
    
    params = {
        'size': 2.0,
        'crop': 'Wheat',
        'sowing_date': '2025-11-15',
        'nitrogen': 65.0,
        'phosphorus': 10.0,
        'potassium': 75.0,
        'soil_ph': 5.8,
        'soil_moisture': 20.0,
        'electrical_conductivity': 250.0,
        'soil_temperature': 25.0,
        'use_llm': False  # Disable LLM for faster testing
    }
    
    result = system.predict(**params)
    
    print("\n✅ Recommendation Generated Successfully!")
    print(f"   N Status: {result['ml_predictions']['N_Status']}")
    print(f"   P Status: {result['ml_predictions']['P_Status']}")
    print(f"   K Status: {result['ml_predictions']['K_Status']}")
    print(f"   Primary Fertilizer: {result['ml_predictions']['Primary_Fertilizer']}")
    print(f"   Secondary Fertilizer: {result['ml_predictions']['Secondary_Fertilizer']}")
    print(f"   pH Amendment: {result['ml_predictions']['pH_Amendment']}")
    
    return result

def test_multiple_crops():
    """Test recommendations for multiple crops"""
    print("\n" + "="*80)
    print("TEST 2: Multiple Crop Types")
    print("="*80)
    
    system = FinalFertilizerRecommendationSystem()
    
    crops = ['Rice', 'Maize', 'Cotton', 'Groundnut']
    
    for crop in crops:
        print(f"\nTesting {crop}...")
        params = {
            'size': 1.5,
            'crop': crop,
            'sowing_date': '2025-12-01',
            'nitrogen': 80.0,
            'phosphorus': 15.0,
            'potassium': 100.0,
            'soil_ph': 6.5,
            'soil_moisture': 25.0,
            'electrical_conductivity': 400.0,
            'soil_temperature': 28.0,
            'use_llm': False
        }
        
        result = system.predict(**params)
        print(f"   ✓ {crop}: {result['ml_predictions']['Primary_Fertilizer']}")

def test_extreme_conditions():
    """Test recommendations under extreme conditions"""
    print("\n" + "="*80)
    print("TEST 3: Extreme Soil Conditions")
    print("="*80)
    
    system = FinalFertilizerRecommendationSystem()
    
    # Test 1: Very acidic soil
    print("\n1. Very Acidic Soil (pH 4.5)...")
    params_acidic = {
        'size': 1.0,
        'crop': 'Wheat',
        'sowing_date': '2025-11-01',
        'nitrogen': 70.0,
        'phosphorus': 12.0,
        'potassium': 90.0,
        'soil_ph': 4.5,
        'soil_moisture': 22.0,
        'electrical_conductivity': 200.0,
        'soil_temperature': 24.0,
        'use_llm': False
    }
    
    result = system.predict(**params_acidic)
    print(f"   pH Amendment: {result['ml_predictions']['pH_Amendment']}")
    print(f"   Secondary Fertilizer: {result['ml_predictions']['Secondary_Fertilizer']}")
    
    # Test 2: Very alkaline soil
    print("\n2. Very Alkaline Soil (pH 8.5)...")
    params_alkaline = {
        'size': 1.0,
        'crop': 'Rice',
        'sowing_date': '2025-11-01',
        'nitrogen': 85.0,
        'phosphorus': 18.0,
        'potassium': 110.0,
        'soil_ph': 8.5,
        'soil_moisture': 28.0,
        'electrical_conductivity': 180.0,
        'soil_temperature': 26.0,
        'use_llm': False
    }
    
    result = system.predict(**params_alkaline)
    print(f"   pH Amendment: {result['ml_predictions']['pH_Amendment']}")
    print(f"   Secondary Fertilizer: {result['ml_predictions']['Secondary_Fertilizer']}")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("INTEGRATED SYSTEM TEST SUITE")
    print("Testing Final_Model.py with Integrated AgriCure Model")
    print("="*80)
    
    try:
        # Run all tests
        test_basic_recommendation()
        test_multiple_crops()
        test_extreme_conditions()
        
        print("\n" + "="*80)
        print("✅ ALL INTEGRATION TESTS PASSED!")
        print("="*80 + "\n")
        
    except Exception as e:
        print(f"\n❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
