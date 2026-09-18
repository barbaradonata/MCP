from googleapiclient.discovery import build
from typing import Dict, Any
from appsscript_mcp.auth import get_credentials
from appsscript_mcp.exceptions import APIError

class DriveService:
    def __init__(self):
        self.creds = get_credentials()
        self.service = build('drive', 'v3', credentials=self.creds)

    def _handle_api_error(self, e):
        import json
        try:
            error_details = json.loads(e.content).get('error', {})
            status = error_details.get('code')
            message = error_details.get('message', str(e))
            raise APIError(f"Drive API Error ({status}): {message}", status, error_details)
        except Exception:
            raise APIError(f"Unexpected Drive API Error: {str(e)}")

    def share_project(self, script_id: str, email: str, role: str) -> Dict[str, Any]:
        """
        Shares the script project file with a specific user.
        role: 'reader', 'commenter', 'writer'
        """
        body = {
            "type": "user",
            "role": role,
            "emailAddress": email
        }
        try:
            return self.service.permissions().create(
                fileId=script_id,
                body=body,
                fields="id, emailAddress, role"
            ).execute()
        except Exception as e:
            self._handle_api_error(e)
            
    def list_projects(self) -> Dict[str, Any]:
        """
        Lists Apps Script projects stored in the user's Google Drive.
        """
        try:
            return self.service.files().list(
                q="mimeType='application/vnd.google-apps.script'",
                spaces='drive',
                fields='nextPageToken, files(id, name)'
            ).execute()
        except Exception as e:
            self._handle_api_error(e)
