import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from appsscript_mcp.config import settings
from appsscript_mcp.exceptions import AuthenticationError

def get_credentials() -> Credentials:
    """
    Authenticates the user and returns the Google API Credentials.
    Uses OAuth 2.0 Desktop App Flow.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens.
    if os.path.exists(settings.google_token_path):
        try:
            creds = Credentials.from_authorized_user_file(settings.google_token_path, settings.oauth_scopes)
        except Exception as e:
            # If token is corrupted, we will require re-login
            pass

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                raise AuthenticationError(f"Failed to refresh token: {e}")
        else:
            if not os.path.exists(settings.google_credentials_path):
                raise AuthenticationError(
                    f"Credentials file '{settings.google_credentials_path}' not found. "
                    "Please download OAuth 2.0 Client ID credentials (Desktop app type) "
                    "from Google Cloud Console."
                )
            
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    settings.google_credentials_path, settings.oauth_scopes
                )
                creds = flow.run_local_server(port=0)
            except Exception as e:
                raise AuthenticationError(f"OAuth flow failed: {e}")

        # Save the credentials for the next run
        try:
            with open(settings.google_token_path, 'w') as token:
                token.write(creds.to_json())
        except Exception as e:
            # Non-fatal if we can't save the token, but we should probably warn
            pass

    return creds
