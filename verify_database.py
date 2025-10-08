# test_fixed_endpoint.py
import requests
import json

def test_fixed_endpoint():
    print("🧪 Testing Fixed Analysis Endpoint")
    print("=" * 50)
    
    # Login first
    login_data = {
        "email": "testuser@university.edu",
        "password": "SecurePass123"
    }
    
    login_response = requests.post("http://localhost:8000/auth/login", json=login_data)
    token = login_response.json().get("access_token")
    
    print(f"🔑 Token: {token[:50]}...")
    
    # Test with assignment 65
    headers = {"Authorization": f"Bearer {token}"}
    
    print("📨 Testing /analysis/65...")
    response = requests.get("http://localhost:8000/analysis/65", headers=headers)
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 500:
        print("❌ Still getting 500 error")
        print(f"Error: {response.text}")
    elif response.status_code == 200:
        print("✅ Success! Analysis found:")
        print(json.dumps(response.json(), indent=2))
    elif response.status_code == 404:
        print("ℹ️ Analysis not ready yet (this is expected if n8n is still processing)")
    else:
        print(f"Unexpected status: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    test_fixed_endpoint()