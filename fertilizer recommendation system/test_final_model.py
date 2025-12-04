"""
Example Usage of Final_Model.py
================================

This script demonstrates different ways to use the Final Fertilizer Recommendation System
"""

from Final_Model import FinalFertilizerRecommendationSystem
import json


def example_1_basic_usage():
    """Example 1: Basic usage with default parameters"""
    
    print("\n" + "="*80)
    print("EXAMPLE 1: BASIC USAGE")
    print("="*80)
    
    # Initialize the system
    system = FinalFertilizerRecommendationSystem()
    
    # Make a prediction
    recommendation = system.predict(
        size=2.5,                      # 2.5 hectares
        crop='Wheat',
        soil='Loamy',
        sowing_date='2025-11-15',
        nitrogen=180.0,                # mg/kg
        phosphorus=25.0,               # mg/kg
        potassium=150.0,               # mg/kg
        soil_ph=6.8,
        soil_moisture=55.0,            # %
        electrical_conductivity=450.0,
        soil_temperature=28.5,         # °C
        use_llm=False                  # Use basic mode (no API needed)
    )
    
    # Display ML predictions
    print("\n📊 ML Predictions:")
    print("-" * 80)
    ml_preds = recommendation['ml_predictions']
    for key, value in ml_preds.items():
        print(f"   {key}: {value}")
    
    # Display cost estimate
    if 'cost_estimate' in recommendation:
        print("\n💰 Cost Estimate:")
        print("-" * 80)
        costs = recommendation['cost_estimate']
        for key, value in costs.items():
            print(f"   {key}: {value}")
    
    return recommendation


def example_2_different_crops():
    """Example 2: Testing with different crops"""
    
    print("\n" + "="*80)
    print("EXAMPLE 2: TESTING DIFFERENT CROPS")
    print("="*80)
    
    system = FinalFertilizerRecommendationSystem()
    
    crops = ['Rice', 'Maize', 'Cotton', 'Sugarcane']
    
    results = {}
    
    for crop in crops:
        print(f"\n🌾 Testing {crop}...")
        
        recommendation = system.predict(
            size=1.0,
            crop=crop,
            soil='Alluvial',
            sowing_date='2025-06-01',
            nitrogen=120.0,
            phosphorus=15.0,
            potassium=180.0,
            soil_ph=7.2,
            soil_moisture=45.0,
            electrical_conductivity=600.0,
            soil_temperature=30.0,
            use_llm=False
        )
        
        ml_preds = recommendation['ml_predictions']
        print(f"   Primary Fertilizer: {ml_preds['Primary_Fertilizer']}")
        print(f"   Secondary Fertilizer: {ml_preds['Secondary_Fertilizer']}")
        
        results[crop] = ml_preds
    
    return results


def example_3_soil_deficiency():
    """Example 3: Testing low nutrient soil"""
    
    print("\n" + "="*80)
    print("EXAMPLE 3: LOW NUTRIENT SOIL")
    print("="*80)
    
    system = FinalFertilizerRecommendationSystem()
    
    print("\n📉 Testing soil with low nutrients...")
    
    recommendation = system.predict(
        size=3.0,
        crop='Wheat',
        soil='Sandy',
        sowing_date='2025-10-15',
        nitrogen=50.0,    # Low nitrogen
        phosphorus=5.0,   # Low phosphorus
        potassium=80.0,   # Low potassium
        soil_ph=6.0,
        soil_moisture=30.0,
        electrical_conductivity=300.0,
        soil_temperature=25.0,
        use_llm=False
    )
    
    ml_preds = recommendation['ml_predictions']
    
    print("\n📊 Nutrient Status:")
    print(f"   N Status: {ml_preds['N_Status']}")
    print(f"   P Status: {ml_preds['P_Status']}")
    print(f"   K Status: {ml_preds['K_Status']}")
    
    print("\n💊 Recommended Fertilizers:")
    print(f"   Primary: {ml_preds['Primary_Fertilizer']}")
    print(f"   Secondary: {ml_preds['Secondary_Fertilizer']}")
    print(f"   pH Amendment: {ml_preds['pH_Amendment']}")
    
    return recommendation


def example_4_high_nutrient_soil():
    """Example 4: Testing high nutrient soil"""
    
    print("\n" + "="*80)
    print("EXAMPLE 4: HIGH NUTRIENT SOIL")
    print("="*80)
    
    system = FinalFertilizerRecommendationSystem()
    
    print("\n📈 Testing soil with high nutrients...")
    
    recommendation = system.predict(
        size=1.5,
        crop='Rice',
        soil='Clay',
        sowing_date='2025-07-01',
        nitrogen=300.0,   # High nitrogen
        phosphorus=80.0,  # High phosphorus
        potassium=350.0,  # High potassium
        soil_ph=7.5,
        soil_moisture=65.0,
        electrical_conductivity=800.0,
        soil_temperature=32.0,
        use_llm=False
    )
    
    ml_preds = recommendation['ml_predictions']
    
    print("\n📊 Nutrient Status:")
    print(f"   N Status: {ml_preds['N_Status']}")
    print(f"   P Status: {ml_preds['P_Status']}")
    print(f"   K Status: {ml_preds['K_Status']}")
    
    print("\n💊 Recommended Fertilizers:")
    print(f"   Primary: {ml_preds['Primary_Fertilizer']}")
    print(f"   Secondary: {ml_preds['Secondary_Fertilizer']}")
    print(f"   pH Amendment: {ml_preds['pH_Amendment']}")
    
    return recommendation


def example_5_save_results():
    """Example 5: Save results to file"""
    
    print("\n" + "="*80)
    print("EXAMPLE 5: SAVE RESULTS TO FILE")
    print("="*80)
    
    system = FinalFertilizerRecommendationSystem()
    
    recommendation = system.predict(
        size=2.0,
        crop='Maize',
        soil='Loamy',
        sowing_date='2025-05-20',
        nitrogen=150.0,
        phosphorus=30.0,
        potassium=200.0,
        soil_ph=6.5,
        soil_moisture=50.0,
        electrical_conductivity=500.0,
        soil_temperature=27.0,
        use_llm=False
    )
    
    # Save to JSON file
    output_file = "example_recommendation.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(recommendation, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Recommendation saved to: {output_file}")
    
    # Display summary
    ml_preds = recommendation['ml_predictions']
    print("\n📋 Summary:")
    print(f"   Crop: Maize")
    print(f"   Field Size: 2.0 hectares")
    print(f"   Primary Fertilizer: {ml_preds['Primary_Fertilizer']}")
    print(f"   Secondary Fertilizer: {ml_preds['Secondary_Fertilizer']}")
    
    return recommendation


def example_6_batch_predictions():
    """Example 6: Batch predictions for multiple fields"""
    
    print("\n" + "="*80)
    print("EXAMPLE 6: BATCH PREDICTIONS")
    print("="*80)
    
    system = FinalFertilizerRecommendationSystem()
    
    # Define multiple test cases
    test_cases = [
        {
            'name': 'Field A - Wheat',
            'params': {
                'size': 2.5, 'crop': 'Wheat', 'soil': 'Loamy',
                'sowing_date': '2025-11-01', 'nitrogen': 180.0,
                'phosphorus': 25.0, 'potassium': 150.0, 'soil_ph': 6.8,
                'soil_moisture': 55.0, 'electrical_conductivity': 450.0,
                'soil_temperature': 28.5, 'use_llm': False
            }
        },
        {
            'name': 'Field B - Rice',
            'params': {
                'size': 1.8, 'crop': 'Rice', 'soil': 'Clay',
                'sowing_date': '2025-06-15', 'nitrogen': 140.0,
                'phosphorus': 18.0, 'potassium': 190.0, 'soil_ph': 7.0,
                'soil_moisture': 60.0, 'electrical_conductivity': 520.0,
                'soil_temperature': 30.0, 'use_llm': False
            }
        },
        {
            'name': 'Field C - Cotton',
            'params': {
                'size': 3.2, 'crop': 'Cotton', 'soil': 'Sandy',
                'sowing_date': '2025-04-20', 'nitrogen': 110.0,
                'phosphorus': 12.0, 'potassium': 130.0, 'soil_ph': 6.5,
                'soil_moisture': 42.0, 'electrical_conductivity': 380.0,
                'soil_temperature': 29.0, 'use_llm': False
            }
        }
    ]
    
    results = {}
    
    for test_case in test_cases:
        print(f"\n🌾 Processing {test_case['name']}...")
        
        recommendation = system.predict(**test_case['params'])
        ml_preds = recommendation['ml_predictions']
        
        print(f"   Primary: {ml_preds['Primary_Fertilizer']}")
        print(f"   Secondary: {ml_preds['Secondary_Fertilizer']}")
        
        results[test_case['name']] = ml_preds
    
    # Save batch results
    batch_file = "batch_recommendations.json"
    with open(batch_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Batch results saved to: {batch_file}")
    
    return results


def main():
    """Run all examples"""
    
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*22 + "FINAL MODEL - USAGE EXAMPLES" + " "*23 + "║")
    print("╚" + "="*78 + "╝")
    
    try:
        # Run examples
        example_1_basic_usage()
        example_2_different_crops()
        example_3_soil_deficiency()
        example_4_high_nutrient_soil()
        example_5_save_results()
        example_6_batch_predictions()
        
        print("\n" + "="*80)
        print("✅ ALL EXAMPLES COMPLETED SUCCESSFULLY")
        print("="*80)
        print("\nGenerated files:")
        print("  - example_recommendation.json")
        print("  - batch_recommendations.json")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
