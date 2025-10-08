# debug_n8n_execution.py
import requests
import json
import time

def debug_n8n_execution():
    print("🔍 Debugging n8n Workflow Execution")
    print("=" * 50)
    
    webhook_url = "http://localhost:5678/webhook/assignment"
    
    # Test with a simple, well-structured payload
    test_payload = {
        "assignment_id": 16,
        "text": "Machine learning is transforming education through personalized learning systems that adapt to individual student needs.",
        "word_count": 25,
        "student_email": "testuser@university.edu"
    }
    
    print("📨 Sending test payload:")
    print(json.dumps(test_payload, indent=2))
    
    try:
        start_time = time.time()
        response = requests.post(webhook_url, json=test_payload, timeout=60)
        response_time = time.time() - start_time
        
        print(f"\n📊 Response Analysis:")
        print(f"   Status: {response.status_code}")
        print(f"   Response Time: {response_time:.2f}s")
        print(f"   Content Length: {len(response.text)}")
        
        if response.text:
            print(f"   Content: {response.text}")
        else:
            print("   ❌ Empty response - workflow is failing silently")
            
        # Check if anything was stored in the database
        check_database_for_results(16)
        
    except Exception as e:
        print(f"❌ Request failed: {e}")

def check_database_for_results(assignment_id):
    print(f"\n🔍 Checking database for assignment {assignment_id}...")
    import subprocess
    
    query = f"SELECT * FROM analysis_results WHERE assignment_id = {assignment_id};"
    
    try:
        result = subprocess.run([
            'docker', 'exec', '-i', 'academic_postgres',
            'psql', '-U', 'student', '-d', 'academic_helper', '-c', query
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            if "0 rows" in result.stdout:
                print("   ❌ No analysis results found in database")
            else:
                print("   ✅ Analysis results found!")
                print(result.stdout)
        else:
            print(f"   ❌ Database query failed: {result.stderr}")
            
    except Exception as e:
        print(f"   ❌ Error checking database: {e}")

if __name__ == "__main__":
    debug_n8n_execution()