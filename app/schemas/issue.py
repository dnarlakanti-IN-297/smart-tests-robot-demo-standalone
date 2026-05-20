"""Issue schemas"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class IssueBase(BaseModel):
    """Base issue schema"""

    title: str = Field(..., min_length=20, max_length=200)
    description: Optional[str] = None
    status: str = "open"
    type: str = "task"
    priority: str = "medium"


class IssueCreate(IssueBase):
    """Schema for creating an issue"""

    project_id: int
    assignee_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []


class IssueUpdate(BaseModel):
    """Schema for updating an issue"""

    title: Optional[str] = Field(None, min_length=20, max_length=200)
    description: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None
    priority: Optional[str] = None
    assignee_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class IssueList(BaseModel):
    """Schema for issue list item"""

    id: int
    title: str
    status: str
    type: str
    priority: str
    project_id: int
    creator_id: int
    assignee_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class Issue(IssueList):
    """Schema for detailed issue response"""

    description: Optional[str] = None

    class Config:
        from_attributes = True
