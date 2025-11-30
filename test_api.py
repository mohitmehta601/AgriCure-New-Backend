"""Simple test to check if API works"""
import requests
import time

# Wait for server to be ready
time.sleep(2)

try:
    # Test health endpoint
    response = requests.get("http://localhost:8000/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    # Test soil-data endpoint
    print("\nTesting soil-data endpoint...")
    soil_response = requests.post(
        "http://localhost:8000/soil-data",
        json={"latitude": 28.6139, "longitude": 77.2090}
    )
    print(f"Status Code: {soil_response.status_code}")
    print(f"Response: {soil_response.json()}")
    
except Exception as e:
    print(f"Error: {e}")
