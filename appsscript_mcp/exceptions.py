class AppsScriptMCPError(Exception):
    """Base exception for Apps Script MCP errors."""
    pass

class AuthenticationError(AppsScriptMCPError):
    """Raised when there is an issue with Google Authentication."""
    pass

class APIError(AppsScriptMCPError):
    """Raised when a Google API call fails."""
    def __init__(self, message, status_code=None, raw_response=None):
        super().__init__(message)
        self.status_code = status_code
        self.raw_response = raw_response

class ProjectNotFoundError(APIError):
    """Raised when a project is not found."""
    pass

class FileOperationError(AppsScriptMCPError):
    """Raised when there's an error manipulating files locally or remotely."""
    pass
