import sys
import os
import asyncio
from fastapi.testclient import TestClient

# Ensure the app directory is in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

def test_google_shopping_endpoint():
    print("Initializing TestClient...")
    client = TestClient(app)
    
    query = "cooker"
    print(f"Sending GET request to /api/v1/search?q={query}")
    
    # Send request
    response = client.get(f"/api/v1/search?q={query}")
    
    print(f"Status Code: {response.status_code}")
    print("Response JSON:")
    
    import json
    try:
        print(json.dumps(response.json(), indent=2))
    except Exception as e:
        print(f"Failed to parse JSON: {e}")
        print(response.text)

if __name__ == "__main__":
    test_google_shopping_endpoint()
