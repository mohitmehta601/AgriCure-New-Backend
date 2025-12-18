"""
Quick API Test for Integrated Model
Tests the main.py FastAPI server with the new integrated model
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000"

def test_fertilizer_recommendation():
    """Test the fertilizer recommendation endpoint"""
    print("\n" + "="*80)
    print("API TEST: Fertilizer Recommendation Endpoint")
    print("="*80)
    
    # Test payload
    payload = {
        "size": 2.5,
        "unit": "hectares",
        "crop": "Wheat",
        "sowing_date": "2025-11-15",
        "nitrogen": 65.0,
        "phosphorus": 10.0,
        "potassium": 75.0,
        "soil_ph": 5.8,
        "soil_moisture": 20.0,
        "electrical_conductivity": 250.0,
        "soil_temperature": 25.0
    }
    
    print("\n📤 Sending Request:")
    print(json.dumps(payload, indent=2))
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/fertilizer/recommend",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n✅ Success! Response received:")
            
            if 'ml_predictions' in result:
                ml_preds = result['ml_predictions']
                print(f"\n🎯 ML Predictions:")
                print(f"   N Status: {ml_preds.get('N_Status')}")
                print(f"   P Status: {ml_preds.get('P_Status')}")
                print(f"   K Status: {ml_preds.get('K_Status')}")
                print(f"   Primary Fertilizer: {ml_preds.get('Primary_Fertilizer')}")
                print(f"   Secondary Fertilizer: {ml_preds.get('Secondary_Fertilizer')}")
                print(f"   pH Amendment: {ml_preds.get('pH_Amendment')}")
                
                if 'Deficit_%' in ml_preds:
                    deficits = ml_preds['Deficit_%']
                    print(f"\n📊 Deficit Percentages:")
                    print(f"   N: {deficits.get('N')}%")
                    print(f"   P: {deficits.get('P')}%")
                    print(f"   K: {deficits.get('K')}%")
            
            return True
        else:
            print(f"\n❌ Error: HTTP {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n⚠️ Connection Error: Server not running")
        print("   Please start the server with: python run_server.py")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*80)
    print("API TEST: Health Check Endpoint")
    print("="*80)
    
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            print("\n✅ Server is healthy")
            print(response.json())
            return True
        else:
            print(f"\n❌ Health check failed: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("\n⚠️ Server not running at", BASE_URL)
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*80)
    print("INTEGRATED MODEL API TEST SUITE")
    print("="*80)
    
    print("\n📋 Note: This test requires the API server to be running.")
    print("   Start it with: python run_server.py")
    print("   Or: uvicorn main:app --reload")
    
    input("\nPress Enter when the server is ready...")
    
    # Run tests
    health_ok = test_health_check()
    
    if health_ok:
        test_fertilizer_recommendation()
    else:
        print("\n⚠️ Skipping recommendation test - server not available")
    
    print("\n" + "="*80)
    print("API TESTS COMPLETED")
    print("="*80 + "\n")
