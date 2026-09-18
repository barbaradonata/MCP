import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from appsscript_mcp.services.apps_script import AppsScriptService

def main():
    service = AppsScriptService()
    script_id = "1YeN-8z_E-9a0iKrIZ9G1qqLdDiM9OcjFo-t6ujVPV0BGvS6oKhq0tKRs"
    
    print("Fetching current files...")
    current_content = service.get_project_files(script_id)
    files = current_content.get("files", [])
    
    with open("downloaded_script.json", "w", encoding="utf-8") as f:
        json.dump(files, f, indent=2, ensure_ascii=False)
        
    print("Files downloaded to downloaded_script.json")

if __name__ == "__main__":
    main()
