# test_predictions.py
# Test the model with various India soil scenarios

from predict_single import predict_soil_type
import pandas as pd

# Test cases representing different regions and soil types in India
test_cases = [
    {
        "name": "Indo-Gangetic Plains (Alluvial)",
        "input": {
            "lat": 26.5,
            "lon": 84.0,
            "elevation": 150,
            "rainfall": 1100,
            "temperature": 26,
            "aridity_index": 0.55,
            "dist_river_km": 8.0,
            "dist_coast_km": 850.0,
            "ndvi": 0.6,
            "landcover": "rice_paddy",
            "geology": "alluvium"
        }
    },
    {
        "name": "Deccan Plateau (Black Soil)",
        "input": {
            "lat": 19.5,
            "lon": 76.2,
            "elevation": 500,
            "rainfall": 750,
            "temperature": 28,
            "aridity_index": 0.45,
            "dist_river_km": 25.0,
            "dist_coast_km": 350.0,
            "ndvi": 0.4,
            "landcover": "cotton_field",
            "geology": "basalt"
        }
    },
    {
        "name": "Thar Desert (Arid Soil)",
        "input": {
            "lat": 28.5,
            "lon": 72.0,
            "elevation": 250,
            "rainfall": 250,
            "temperature": 31,
            "aridity_index": 0.15,
            "dist_river_km": 80.0,
            "dist_coast_km": 900.0,
            "ndvi": 0.2,
            "landcover": "desert",
            "geology": "sandstone"
        }
    },
    {
        "name": "Karnataka Plateau (Red Soil)",
        "input": {
            "lat": 15.5,
            "lon": 77.8,
            "elevation": 650,
            "rainfall": 900,
            "temperature": 25,
            "aridity_index": 0.6,
            "dist_river_km": 35.0,
            "dist_coast_km": 420.0,
            "ndvi": 0.5,
            "landcover": "plantation",
            "geology": "granite"
        }
    },
    {
        "name": "Western Ghats (Laterite Soil)",
        "input": {
            "lat": 12.8,
            "lon": 75.5,
            "elevation": 350,
            "rainfall": 2200,
            "temperature": 28,
            "aridity_index": 0.75,
            "dist_river_km": 15.0,
            "dist_coast_km": 45.0,
            "ndvi": 0.7,
            "landcover": "tropical_forest",
            "geology": "laterite"
        }
    },
    {
        "name": "Punjab Plains (Clayey Soil)",
        "input": {
            "lat": 22.5,
            "lon": 80.0,
            "elevation": 350,
            "rainfall": 1050,
            "temperature": 27,
            "aridity_index": 0.55,
            "dist_river_km": 18.0,
            "dist_coast_km": 520.0,
            "ndvi": 0.5,
            "landcover": "mixed_agriculture",
            "geology": "clay"
        }
    },
    {
        "name": "Gujarat Semi-Arid (Alkaline Soil)",
        "input": {
            "lat": 29.0,
            "lon": 74.5,
            "elevation": 280,
            "rainfall": 400,
            "temperature": 30,
            "aridity_index": 0.35,
            "dist_river_km": 45.0,
            "dist_coast_km": 650.0,
            "ndvi": 0.25,
            "landcover": "scrubland",
            "geology": "saline"
        }
    }
]

print("=" * 80)
print("INDIA SOIL TYPE PREDICTION - MODEL TEST RESULTS")
print("=" * 80)
print()

results = []

for i, case in enumerate(test_cases, 1):
    print(f"{i}. {case['name']}")
    print("-" * 80)
    
    soil_type, probabilities = predict_soil_type(case['input'])
    
    print(f"   📍 Location: Lat {case['input']['lat']:.2f}, Lon {case['input']['lon']:.2f}")
    print(f"   🌡️  Climate: {case['input']['rainfall']:.0f}mm rainfall, {case['input']['temperature']:.0f}°C")
    print(f"   🗺️  Terrain: {case['input']['elevation']:.0f}m elevation, {case['input']['landcover']}")
    print()
    print(f"   ✅ PREDICTED SOIL TYPE: {soil_type}")
    print(f"   🎯 Confidence: {probabilities[soil_type]*100:.1f}%")
    print()
    
    # Show top 3 predictions
    sorted_probs = sorted(probabilities.items(), key=lambda x: x[1], reverse=True)
    print("   Top 3 predictions:")
    for j, (soil, prob) in enumerate(sorted_probs[:3], 1):
        bar = "█" * int(prob * 50)
        print(f"      {j}. {soil:12s} {prob*100:5.1f}% {bar}")
    
    print()
    
    results.append({
        "Region": case['name'],
        "Predicted": soil_type,
        "Confidence": f"{probabilities[soil_type]*100:.1f}%"
    })

print("=" * 80)
print("SUMMARY")
print("=" * 80)

df_results = pd.DataFrame(results)
print(df_results.to_string(index=False))

print()
print(f"✓ Model tested on {len(test_cases)} different Indian soil scenarios")
print(f"✓ All predictions completed successfully")
print()
