"""Issue model"""

from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class IssueStatus(str, Enum):
    """Issue status enumeration"""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


class IssueType(str, Enum):
    """Issue type enumeration"""

    BUG = "bug"
    FEATURE = "feature"
    TASK = "task"
    ENHANCEMENT = "enhancement"


class IssuePriority(str, Enum):
    """Issue priority enumeration"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Issue(Base):
    """Issue model"""

    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text)
    status = Column(String, default=IssueStatus.OPEN.value, nullable=False, index=True)
    type = Column(String, default=IssueType.TASK.value, nullable=False, index=True)
    priority = Column(String, default=IssuePriority.MEDIUM.value, nullable=False, index=True)

    # Foreign keys
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    assignee_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    project = relationship("Project", back_populates="issues")
    creator = relationship("User", foreign_keys=[creator_id], back_populates="created_issues")
    assignee = relationship("User", foreign_keys=[assignee_id], back_populates="assigned_issues")
    comments = relationship("Comment", back_populates="issue", cascade="all, delete-orphan")
    tags = relationship("Tag", secondary="issue_tags", back_populates="issues")

    def __repr__(self):
        return f"<Issue(id={self.id}, title={self.title}, status={self.status})>"
