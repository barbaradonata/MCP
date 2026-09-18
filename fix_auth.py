import sys
import os
import json
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from appsscript_mcp.services.apps_script import AppsScriptService
from appsscript_mcp.schemas.file import ProjectFiles, File

def main():
    service = AppsScriptService()
    script_id = "1YeN-8z_E-9a0iKrIZ9G1qqLdDiM9OcjFo-t6ujVPV0BGvS6oKhq0tKRs"
    
    print("Fetching current files...")
    current_content = service.get_project_files(script_id)
    files = current_content.get("files", [])
    
    new_files = []
    
    for f in files:
        if f["name"] == "appsscript":
            # Update appsscript.json to include explicitly the MailApp scope
            manifest = json.loads(f["source"])
            manifest["oauthScopes"] = [
                "https://www.googleapis.com/auth/script.send_mail",
                "https://www.googleapis.com/auth/userinfo.email"
            ]
            f["source"] = json.dumps(manifest, indent=2)
            
        new_files.append(File(name=f["name"], type=f["type"], source=f["source"]))
            
    print("Publishing updated files...")
    project_files = ProjectFiles(files=new_files)
    result = service.update_project_files(script_id, project_files)
    
    print("Successfully updated the script with OAuth Scopes!")

if __name__ == "__main__":
    main()
