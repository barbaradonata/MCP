from mcp.server.fastmcp import FastMCP
from typing import Optional, List, Dict, Any
from appsscript_mcp.services.apps_script import AppsScriptService
from appsscript_mcp.services.drive import DriveService
from appsscript_mcp.services.logging import LoggingService
from appsscript_mcp.schemas.project import ProjectCreate
from appsscript_mcp.schemas.file import ProjectFiles

# Initialize FastMCP Server
mcp = FastMCP("Google Apps Script Manager")

# Lazy load services to avoid auth prompts if tools are not used
def get_apps_script_service():
    return AppsScriptService()

def get_drive_service():
    return DriveService()

def get_logging_service():
    return LoggingService()

@mcp.tool()
def create_project(title: str, parent_id: Optional[str] = None) -> Dict[str, Any]:
    """Creates a new Google Apps Script project."""
    service = get_apps_script_service()
    req = ProjectCreate(title=title, parentId=parent_id)
    return service.create_project(req)

@mcp.tool()
def list_projects() -> Dict[str, Any]:
    """Lists Google Apps Script projects from Google Drive."""
    service = get_drive_service()
    return service.list_projects()

@mcp.tool()
def get_project_info(script_id: str) -> Dict[str, Any]:
    """Gets details of a specific Apps Script project."""
    service = get_apps_script_service()
    return service.get_project(script_id)

@mcp.tool()
def get_project_files(script_id: str) -> Dict[str, Any]:
    """Gets all files (.gs, .html, appsscript.json) from a project."""
    service = get_apps_script_service()
    return service.get_project_files(script_id)

@mcp.tool()
def update_project_files(script_id: str, files_data: dict) -> Dict[str, Any]:
    """
    Updates, creates, or deletes files in the project. 
    Note: This completely replaces all existing files in the project.
    Provide the full dictionary representing ProjectFiles.
    """
    service = get_apps_script_service()
    # Validate with Pydantic
    files = ProjectFiles(**files_data)
    return service.update_project_files(script_id, files)

@mcp.tool()
def run_script_function(script_id: str, function_name: str, parameters: List[Any], dev_mode: bool = False) -> Dict[str, Any]:
    """
    Runs a specific function via the API Executable.
    The script must be deployed as an API Executable.
    """
    service = get_apps_script_service()
    return service.run_function(script_id, function_name, parameters, dev_mode)

@mcp.tool()
def create_version(script_id: str, description: Optional[str] = None) -> Dict[str, Any]:
    """Creates a new immutable version of the project."""
    service = get_apps_script_service()
    return service.create_version(script_id, description)

@mcp.tool()
def list_deployments(script_id: str) -> Dict[str, Any]:
    """Lists the deployments of a project."""
    service = get_apps_script_service()
    return service.list_deployments(script_id)

@mcp.tool()
def create_deployment(script_id: str, version_number: int, description: Optional[str] = None) -> Dict[str, Any]:
    """Creates a new deployment (Web App or API Executable) for a specific version."""
    service = get_apps_script_service()
    return service.create_deployment(script_id, version_number, description)

@mcp.tool()
def manage_permissions(script_id: str, email: str, role: str) -> Dict[str, Any]:
    """
    Adds permissions to the project. 
    Role can be 'reader', 'commenter', or 'writer'.
    """
    service = get_drive_service()
    return service.share_project(script_id, email, role)

@mcp.tool()
def get_logs(script_id: str, limit: int = 50) -> Dict[str, Any]:
    """
    Queries execution logs using Google Cloud Logging.
    Requires GOOGLE_CLOUD_PROJECT_ID in the .env file.
    """
    service = get_logging_service()
    return service.get_logs(script_id, limit)

if __name__ == "__main__":
    # Start the server using stdio transport
    mcp.run()
