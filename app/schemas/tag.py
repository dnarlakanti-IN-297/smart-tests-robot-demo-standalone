"""Tag schemas"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TagBase(BaseModel):
    """Base tag schema"""

    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#6B7280", pattern=r"^#[0-9A-Fa-f]{6}$")


class TagCreate(TagBase):
    """Schema for creating a tag"""

    pass


class Tag(TagBase):
    """Schema for tag response"""

    id: int
    created_at: datetime

    class Config:
        from_attributes = True
