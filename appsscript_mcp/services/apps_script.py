from googleapiclient.discovery import build
from typing import List, Dict, Any, Optional
from appsscript_mcp.auth import get_credentials
from appsscript_mcp.exceptions import APIError, ProjectNotFoundError
from appsscript_mcp.schemas.project import ProjectCreate, ProjectInfo
from appsscript_mcp.schemas.file import ProjectFiles

class AppsScriptService:
    def __init__(self):
        self.creds = get_credentials()
        self.service = build('script', 'v1', credentials=self.creds)

    def _handle_api_error(self, e):
        # A simple helper to map Google API errors to our custom errors
        import json
        try:
            error_details = json.loads(e.content).get('error', {})
            status = error_details.get('code')
            message = error_details.get('message', str(e))
            if status == 404:
                raise ProjectNotFoundError(f"Project not found: {message}", status, error_details)
            raise APIError(f"API Error ({status}): {message}", status, error_details)
        except Exception:
            raise APIError(f"Unexpected API Error: {str(e)}")

    def create_project(self, request: ProjectCreate) -> Dict[str, Any]:
        """Creates a new Apps Script project."""
        body = {"title": request.title}
        if request.parentId:
            body["parentId"] = request.parentId
        
        try:
            return self.service.projects().create(body=body).execute()
        except Exception as e:
            self._handle_api_error(e)

    def get_project(self, script_id: str) -> Dict[str, Any]:
        """Gets project info."""
        try:
            return self.service.projects().get(scriptId=script_id).execute()
        except Exception as e:
            self._handle_api_error(e)

    def get_project_files(self, script_id: str) -> Dict[str, Any]:
        """Gets all files in a project."""
        try:
            return self.service.projects().getContent(scriptId=script_id).execute()
        except Exception as e:
            self._handle_api_error(e)

    def update_project_files(self, script_id: str, files: ProjectFiles) -> Dict[str, Any]:
        """Updates all files in a project. Note: This replaces all existing files."""
        body = {"files": [f.model_dump() for f in files.files]}
        try:
            return self.service.projects().updateContent(scriptId=script_id, body=body).execute()
        except Exception as e:
            self._handle_api_error(e)

    def run_function(self, script_id: str, function: str, parameters: List[Any], dev_mode: bool = False) -> Dict[str, Any]:
        """Runs a function via the Apps Script API (Script needs to be deployed as API Executable)."""
        body = {
            "function": function,
            "parameters": parameters,
            "devMode": dev_mode
        }
        try:
            # We use scripts.run (requires the script to be an API Executable)
            return self.service.scripts().run(scriptId=script_id, body=body).execute()
        except Exception as e:
            self._handle_api_error(e)

    def create_version(self, script_id: str, description: Optional[str] = None) -> Dict[str, Any]:
        """Creates a new version."""
        body = {"description": description} if description else {}
        try:
            return self.service.projects().versions().create(scriptId=script_id, body=body).execute()
        except Exception as e:
            self._handle_api_error(e)
            
    def list_deployments(self, script_id: str) -> Dict[str, Any]:
        """Lists deployments."""
        try:
            return self.service.projects().deployments().list(scriptId=script_id).execute()
        except Exception as e:
            self._handle_api_error(e)

    def create_deployment(self, script_id: str, version_number: int, description: Optional[str] = None) -> Dict[str, Any]:
        """Creates a deployment."""
        body = {
            "versionNumber": version_number,
            "description": description
        }
        try:
            return self.service.projects().deployments().create(scriptId=script_id, body=body).execute()
        except Exception as e:
            self._handle_api_error(e)
