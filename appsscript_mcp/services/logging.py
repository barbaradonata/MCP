from googleapiclient.discovery import build
from typing import Dict, Any, Optional
from appsscript_mcp.auth import get_credentials
from appsscript_mcp.config import settings
from appsscript_mcp.exceptions import APIError

class LoggingService:
    def __init__(self):
        self.creds = get_credentials()
        # Logging API requires the Google Cloud Project ID
        self.project_id = settings.google_cloud_project_id
        if self.project_id:
            self.service = build('logging', 'v2', credentials=self.creds)
        else:
            self.service = None

    def _handle_api_error(self, e):
        import json
        try:
            error_details = json.loads(e.content).get('error', {})
            status = error_details.get('code')
            message = error_details.get('message', str(e))
            raise APIError(f"Logging API Error ({status}): {message}", status, error_details)
        except Exception:
            raise APIError(f"Unexpected Logging API Error: {str(e)}")

    def get_logs(self, script_id: str, limit: int = 50) -> Dict[str, Any]:
        """
        Retrieves logs from Google Cloud Logging for the specific script project.
        Requires GOOGLE_CLOUD_PROJECT_ID to be set in .env
        """
        if not self.service:
            raise APIError("GOOGLE_CLOUD_PROJECT_ID is not configured in environment variables.")

        # Filter logs for the specific script ID. 
        # Note: Apps script logs usually have resource.type="app_script_function" 
        # and resource.labels.project_id maps to the GCP project.
        # We try to filter by the scriptId if it's logged in the payload, but standard Apps Script
        # logs the script_id in jsonPayload.scriptId or similar depending on the exact logger used.
        # A common filter for all Apps Script functions in the GCP project:
        filter_str = f'resource.type="app_script_function"'

        body = {
            "resourceNames": [f"projects/{self.project_id}"],
            "filter": filter_str,
            "orderBy": "timestamp desc",
            "pageSize": limit
        }
        
        try:
            return self.service.entries().list(body=body).execute()
        except Exception as e:
            self._handle_api_error(e)
