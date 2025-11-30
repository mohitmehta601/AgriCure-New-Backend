"""
Quick test to verify the soil prediction integration is working
Run this to test the /soil-data endpoint
"""

import requests
import json

# Test configuration
API_URL = "http://localhost:8000"

def test_health():
    """Test if the server is running"""
    print("\n" + "=" * 70)
    print("Testing Server Health...")
    print("=" * 70)
    
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        data = response.json()
        
        print(f"✓ Status: {data['status']}")
        print(f"✓ Model Loaded: {data['model_loaded']}")
        print(f"✓ Message: {data['message']}")
        return True
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return False

def test_soil_data():
    """Test the /soil-data endpoint (main integration point)"""
    print("\n" + "=" * 70)
    print("Testing Soil Data Endpoint (Add Farm Integration)")
    print("=" * 70)
    
    # Test location: New Delhi
    test_location = {
        "latitude": 28.6139,
        "longitude": 77.2090
    }
    
    print(f"\nTest Location:")
    print(f"  Latitude:  {test_location['latitude']}")
    print(f"  Longitude: {test_location['longitude']}")
    print(f"  (Approximately New Delhi, India)")
    
    try:
        response = requests.post(
            f"{API_URL}/soil-data",
            json=test_location,
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        data = response.json()
        
        print(f"\n✓ Request successful!")
        print(f"\nSoil Prediction Results:")
        print(f"  Soil Type: {data['soil_type']}")
        print(f"  Confidence: {data['confidence']:.2%}")
        print(f"  Success: {data['success']}")
        print(f"  Sources: {', '.join(data['sources'])}")
        
        if data['location_info']:
            print(f"\nLocation Info:")
            print(f"  Country: {data['location_info']['country']}")
        
        print(f"\nLocation Data:")
        print(f"  Latitude:  {data['location']['latitude']}")
        print(f"  Longitude: {data['location']['longitude']}")
        print(f"  Timestamp: {data['location']['timestamp']}")
        
        return True
    except Exception as e:
        print(f"✗ Soil data test failed: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response: {e.response.text}")
        return False

def test_multiple_locations():
    """Test with multiple locations across India"""
    print("\n" + "=" * 70)
    print("Testing Multiple Locations Across India")
    print("=" * 70)
    
    test_locations = [
        {"name": "New Delhi", "latitude": 28.6139, "longitude": 77.2090},
        {"name": "Mumbai", "latitude": 19.0760, "longitude": 72.8777},
        {"name": "Bangalore", "latitude": 12.9716, "longitude": 77.5946},
        {"name": "Punjab", "latitude": 31.1471, "longitude": 75.3412},
        {"name": "Tamil Nadu", "latitude": 11.1271, "longitude": 78.6569},
    ]
    
    results = []
    
    for loc in test_locations:
        try:
            response = requests.post(
                f"{API_URL}/soil-data",
                json={"latitude": loc["latitude"], "longitude": loc["longitude"]},
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            data = response.json()
            
            results.append({
                "location": loc["name"],
                "soil_type": data["soil_type"],
                "confidence": data["confidence"]
            })
            
            print(f"\n{loc['name']:15} → {data['soil_type']:20} (Confidence: {data['confidence']:.2%})")
            
        except Exception as e:
            print(f"\n{loc['name']:15} → Error: {str(e)[:50]}")
    
    if results:
        print(f"\n✓ Successfully tested {len(results)}/{len(test_locations)} locations")
        return True
    else:
        print(f"\n✗ No locations tested successfully")
        return False

def main():
    """Run all tests"""
    print("\n" + "=" * 70)
    print("🌾 AgriCure Soil Prediction Integration Test")
    print("=" * 70)
    
    results = {
        "Health Check": test_health(),
        "Soil Data Endpoint": test_soil_data(),
        "Multiple Locations": test_multiple_locations()
    }
    
    print("\n" + "=" * 70)
    print("Test Summary")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✓ PASSED" if passed else "✗ FAILED"
        print(f"  {test_name:25} {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 70)
    if all_passed:
        print("✅ All tests passed! Integration is working correctly.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    print("=" * 70 + "\n")
    
    return all_passed

if __name__ == "__main__":
    import sys
    success = main()
    sys.exit(0 if success else 1)
