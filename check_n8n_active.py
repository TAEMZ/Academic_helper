# check_n8n_active.py
import requests
import base64

def check_and_activate_workflow():
    print("🔧 Checking n8n Workflow Status")
    print("=" * 50)
    
    # n8n API credentials
    auth = base64.b64encode(b"sinkupicas9@gmail.com:Admin1234567").decode('utf-8')
    headers = {'Authorization': f'Basic {auth}'}
    
    try:
        # Get all workflows
        response = requests.get(
            'http://localhost:5678/rest/workflows',
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            workflows = response.json().get('data', [])
            print(f"📋 Found {len(workflows)} workflows")
            
            assignment_workflow = None
            for wf in workflows:
                if 'assignment' in wf.get('name', '').lower():
                    assignment_workflow = wf
                    print(f"\n🎯 Found Assignment Workflow:")
                    print(f"   Name: {wf.get('name')}")
                    print(f"   ID: {wf.get('id')}")
                    print(f"   Active: {wf.get('active')}")
                    print(f"   Updated: {wf.get('updatedAt')}")
                    
                    if not wf.get('active'):
                        print("   ❌ WORKFLOW IS NOT ACTIVE!")
                        print("\n   💡 To activate:")
                        print("   1. Go to http://localhost:5678")
                        print("   2. Login: admin / admin123")
                        print("   3. Find this workflow and toggle it ON")
                        print("   4. Save the workflow")
                    else:
                        print("   ✅ Workflow is ACTIVE!")
            
            if not assignment_workflow:
                print("❌ No assignment workflow found!")
                print("   You need to import the workflow first")
                
        else:
            print(f"❌ Failed to get workflows: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_and_activate_workflow()