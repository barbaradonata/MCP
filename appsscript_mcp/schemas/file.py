from pydantic import BaseModel, Field
from typing import Literal, Optional, List

# Apps Script Enum for File Types
FileType = Literal["ENUM_TYPE_UNSPECIFIED", "SERVER_JS", "HTML", "JSON"]

class File(BaseModel):
    name: str = Field(..., description="The name of the file without extension")
    type: FileType = Field(..., description="The type of the file (SERVER_JS, HTML, JSON)")
    source: str = Field(..., description="The content of the file")

class ProjectFiles(BaseModel):
    files: List[File] = Field(..., description="List of all files in the project")
