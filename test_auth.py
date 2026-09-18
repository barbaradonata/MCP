import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from appsscript_mcp.services.apps_script import AppsScriptService

def main():
    print("Starting authentication flow...")
    print("Look at your browser to authenticate!")
    service = AppsScriptService()
    
    script_id = "1YeN-8z_E-9a0iKrIZ9G1qqLdDiM9OcjFo-t6ujVPV0BGvS6oKhq0tKRs"
    print(f"Fetching info for script: {script_id}")
    
    try:
        info = service.get_project(script_id)
        print("Success! Project Info:")
        print(info)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
