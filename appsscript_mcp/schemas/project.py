from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class ProjectCreate(BaseModel):
    title: str = Field(..., description="The title of the new Apps Script project")
    parentId: Optional[str] = Field(None, description="The Drive ID of a parent file that the created script project is bound to (optional)")

class ProjectInfo(BaseModel):
    scriptId: str
    title: str
    createTime: str
    updateTime: str
    creator: Dict[str, Any]
    lastModifyUser: Dict[str, Any]

class DeploymentConfig(BaseModel):
    scriptId: str
    versionNumber: Optional[int] = Field(None, description="The version number to deploy")
    manifestFileName: Optional[str] = Field(None, description="The manifest file name (usually appsscript)")
    description: Optional[str] = Field(None, description="Deployment description")

class VersionCreate(BaseModel):
    description: Optional[str] = Field(None, description="Description for this version")
