# debug_n8n_workflow.py
import requests
import json
import time

def debug_n8n_workflow():
    print("🔍 Debugging n8n Workflow Execution")
    print("=" * 50)
    
    # Test payload that matches what FastAPI sends
    test_payload = {
        "assignment_id": 999,
        "student_id": 1,
        "student_email": "test@test.com",
        "filename": "test_debug.txt",
        "text": "Machine learning algorithms including neural networks and decision trees are transforming various industries through pattern recognition and predictive analytics.",
        "word_count": 25,
        "file_path": "/uploads/test.txt",
        "debug": True
    }
    
    print("📨 Sending test payload to n8n...")
    print(f"Payload: {json.dumps(test_payload, indent=2)}")
    
    try:
        response = requests.post(
            'http://localhost:5678/webhook/assignment',
            json=test_payload,
            timeout=30
        )
        
        print(f"✅ Webhook Response Status: {response.status_code}")
        print(f"Response Body: {response.text}")
        
        # Check if we got an execution ID
        if response.text and 'executionId' in response.text:
            print("🎯 Workflow execution started!")
        else:
            print("⚠️  No execution ID in response - workflow might not be active")
            
    except Exception as e:
        print(f"❌ Webhook Error: {e}")

def check_n8n_executions():
    """Check recent n8n executions"""
    print("\n📋 Checking n8n Executions...")
    try:
        # This is a basic check - n8n API might require authentication
        response = requests.get('http://localhost:5678/rest/executions', timeout=10)
        if response.status_code == 200:
            print("✅ Can access executions API")
            data = response.json()
            print(f"Found {len(data.get('data', []))} executions")
        else:
            print(f"❌ Executions API returned: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Cannot check executions: {e}")

if __name__ == "__main__":
    debug_n8n_workflow()
    check_n8n_executions()