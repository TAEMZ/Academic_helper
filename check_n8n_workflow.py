# find_workflow_files.py
import os
import glob

def find_workflow_files():
    print("🔍 Looking for n8n workflow files...")
    print("=" * 50)
    
    # Common locations for workflow files
    search_patterns = [
        "*.json",
        "**/*workflow*.json", 
        "**/*n8n*.json",
        "n8n/*.json"
    ]
    
    found_files = []
    
    for pattern in search_patterns:
        files = glob.glob(pattern, recursive=True)
        found_files.extend(files)
    
    if found_files:
        print("✅ Found workflow files:")
        for file in found_files:
            print(f"   📄 {file}")
            
            # Check file size
            size = os.path.getsize(file)
            print(f"      Size: {size} bytes")
            
            # Quick peek at content
            try:
                with open(file, 'r') as f:
                    content = f.read(200)
                    if 'n8n' in content.lower() or 'workflow' in content.lower():
                        print(f"      🎯 This looks like a workflow file!")
            except:
                pass
    else:
        print("❌ No workflow JSON files found!")
        print("\n💡 You might need to:")
        print("   1. Check if the workflow file exists in your project")
        print("   2. Download it from the original source")
        print("   3. Create it from scratch in n8n")

if __name__ == "__main__":
    find_workflow_files()