"""Comment schemas"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CommentBase(BaseModel):
    """Base comment schema"""

    content: str = Field(..., min_length=1)


class CommentCreate(CommentBase):
    """Schema for creating a comment"""

    issue_id: int


class CommentUpdate(BaseModel):
    """Schema for updating a comment"""

    content: str = Field(..., min_length=1)


class Comment(CommentBase):
    """Schema for comment response"""

    id: int
    issue_id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
