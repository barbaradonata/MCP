import os
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    google_credentials_path: str = Field(default="credentials.json", description="Path to the OAuth credentials.json file")
    google_token_path: str = Field(default="token.json", description="Path to save the user OAuth token")
    google_cloud_project_id: Optional[str] = Field(default=None, description="Google Cloud Project ID for logging API")
    oauth_scopes: List[str] = Field(
        default=[
            "https://www.googleapis.com/auth/script.projects",
            "https://www.googleapis.com/auth/script.deployments",
            "https://www.googleapis.com/auth/drive",
            "https://www.googleapis.com/auth/logging.read",
        ],
        description="OAuth scopes required for the application"
    )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("oauth_scopes", mode="before")
    def parse_scopes(cls, v):
        if isinstance(v, str):
            if not v.strip():
                return [
                    "https://www.googleapis.com/auth/script.projects",
                    "https://www.googleapis.com/auth/script.deployments",
                    "https://www.googleapis.com/auth/drive",
                    "https://www.googleapis.com/auth/logging.read",
                ]
            return [scope.strip() for scope in v.split(",")]
        return v

settings = Settings()
