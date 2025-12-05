"""
Test script for Secondary Fertilizer Model with Dataset Integration
Demonstrates the dataset-based lookup functionality
"""

from secondary_fertilizer_model import SecondaryFertilizerModel

def test_dataset_integration():
    """Test the secondary fertilizer model with dataset integration."""
    
    # Initialize model
    model = SecondaryFertilizerModel()
    
    print("=" * 80)
    print("TESTING SECONDARY FERTILIZER MODEL - DATASET INTEGRATION")
    print("=" * 80)
    
    # Test Case 1: Alluvial soil, Acidic pH, Low EC, Rice
    print("\n📋 TEST CASE 1: Alluvial + Acidic pH + Low EC + Rice")
    print("-" * 80)
    test1 = {
        'Nitrogen': 150,
        'Phosphorus': 25,
        'Potassium': 200,
        'Crop_Type': 'rice',
        'pH': 5.5,
        'Electrical_Conductivity': 400,
        'Soil_Moisture': 18,
        'Soil_Temperature': 28,
        'Soil_Type': 'Alluvial'
    }
    
    ph_range = model.categorize_ph(test1['pH'])
    ec_range = model.categorize_ec(test1['Electrical_Conductivity'])
    
    print(f"Input: Soil={test1['Soil_Type']}, Crop={test1['Crop_Type']}")
    print(f"       pH={test1['pH']} ({ph_range}), EC={test1['Electrical_Conductivity']} µS/cm ({ec_range})")
    
    result1 = model.predict(test1)
    deficiencies1 = model.identify_deficiencies(
        nitrogen=test1['Nitrogen'],
        phosphorus=test1['Phosphorus'],
        potassium=test1['Potassium'],
        pH=test1['pH'],
        ec=test1['Electrical_Conductivity'],
        moisture=test1['Soil_Moisture'],
        temperature=test1['Soil_Temperature'],
        crop_type=test1['Crop_Type'],
        soil_type=test1['Soil_Type']
    )
    
    print(f"\n✅ Recommendation: {result1}")
    print(f"🔍 Deficiencies: {', '.join(deficiencies1) if deficiencies1 else 'None'}")
    
    # Test Case 2: Black soil, Neutral pH, Medium EC, Wheat
    print("\n\n📋 TEST CASE 2: Black + Neutral pH + Medium EC + Wheat")
    print("-" * 80)
    test2 = {
        'Nitrogen': 200,
        'Phosphorus': 30,
        'Potassium': 250,
        'Crop_Type': 'wheat',
        'pH': 7.0,
        'Electrical_Conductivity': 1000,
        'Soil_Moisture': 20,
        'Soil_Temperature': 22,
        'Soil_Type': 'Black'
    }
    
    ph_range2 = model.categorize_ph(test2['pH'])
    ec_range2 = model.categorize_ec(test2['Electrical_Conductivity'])
    
    print(f"Input: Soil={test2['Soil_Type']}, Crop={test2['Crop_Type']}")
    print(f"       pH={test2['pH']} ({ph_range2}), EC={test2['Electrical_Conductivity']} µS/cm ({ec_range2})")
    
    result2 = model.predict(test2)
    deficiencies2 = model.identify_deficiencies(
        nitrogen=test2['Nitrogen'],
        phosphorus=test2['Phosphorus'],
        potassium=test2['Potassium'],
        pH=test2['pH'],
        ec=test2['Electrical_Conductivity'],
        moisture=test2['Soil_Moisture'],
        temperature=test2['Soil_Temperature'],
        crop_type=test2['Crop_Type'],
        soil_type=test2['Soil_Type']
    )
    
    print(f"\n✅ Recommendation: {result2}")
    print(f"🔍 Deficiencies: {', '.join(deficiencies2) if deficiencies2 else 'None'}")
    
    # Test Case 3: Red soil, Alkaline pH, High EC, Cotton
    print("\n\n📋 TEST CASE 3: Red + Alkaline pH + High EC + Cotton")
    print("-" * 80)
    test3 = {
        'Nitrogen': 180,
        'Phosphorus': 35,
        'Potassium': 280,
        'Crop_Type': 'cotton',
        'pH': 8.0,
        'Electrical_Conductivity': 2500,
        'Soil_Moisture': 15,
        'Soil_Temperature': 30,
        'Soil_Type': 'Red'
    }
    
    ph_range3 = model.categorize_ph(test3['pH'])
    ec_range3 = model.categorize_ec(test3['Electrical_Conductivity'])
    
    print(f"Input: Soil={test3['Soil_Type']}, Crop={test3['Crop_Type']}")
    print(f"       pH={test3['pH']} ({ph_range3}), EC={test3['Electrical_Conductivity']} µS/cm ({ec_range3})")
    
    result3 = model.predict(test3)
    deficiencies3 = model.identify_deficiencies(
        nitrogen=test3['Nitrogen'],
        phosphorus=test3['Phosphorus'],
        potassium=test3['Potassium'],
        pH=test3['pH'],
        ec=test3['Electrical_Conductivity'],
        moisture=test3['Soil_Moisture'],
        temperature=test3['Soil_Temperature'],
        crop_type=test3['Crop_Type'],
        soil_type=test3['Soil_Type']
    )
    
    print(f"\n✅ Recommendation: {result3}")
    print(f"🔍 Deficiencies: {', '.join(deficiencies3) if deficiencies3 else 'None'}")
    
    # Test Case 4: Fallback to rule-based (crop not in dataset)
    print("\n\n📋 TEST CASE 4: Rule-Based Fallback (Tomato - not in dataset)")
    print("-" * 80)
    test4 = {
        'Nitrogen': 120,
        'Phosphorus': 20,
        'Potassium': 180,
        'Crop_Type': 'tomato',
        'pH': 6.5,
        'Electrical_Conductivity': 600,
        'Soil_Moisture': 22,
        'Soil_Temperature': 25,
        'Soil_Type': 'Alluvial'
    }
    
    ph_range4 = model.categorize_ph(test4['pH'])
    ec_range4 = model.categorize_ec(test4['Electrical_Conductivity'])
    
    print(f"Input: Soil={test4['Soil_Type']}, Crop={test4['Crop_Type']}")
    print(f"       pH={test4['pH']} ({ph_range4}), EC={test4['Electrical_Conductivity']} µS/cm ({ec_range4})")
    print(f"Note: Crop not in dataset - using rule-based fallback")
    
    result4 = model.predict(test4)
    deficiencies4 = model.identify_deficiencies(
        nitrogen=test4['Nitrogen'],
        phosphorus=test4['Phosphorus'],
        potassium=test4['Potassium'],
        pH=test4['pH'],
        ec=test4['Electrical_Conductivity'],
        moisture=test4['Soil_Moisture'],
        temperature=test4['Soil_Temperature'],
        crop_type=test4['Crop_Type'],
        soil_type=test4['Soil_Type']
    )
    
    print(f"\n✅ Recommendation: {result4}")
    print(f"🔍 Deficiencies: {', '.join(deficiencies4) if deficiencies4 else 'None'}")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print(f"\n📊 Dataset Summary:")
    print(f"   Total records in dataset: {len(model.dataset)}")
    print(f"   Supported soil types: {', '.join(model.soil_types)}")
    print(f"   Supported crops in requirements: {len(model.crop_micronutrients)}")
    print("=" * 80)


if __name__ == "__main__":
    test_dataset_integration()
