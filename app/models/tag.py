"""Tag model"""

from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from app.database import Base

# Association table for many-to-many relationship between issues and tags
issue_tags = Table(
    "issue_tags",
    Base.metadata,
    Column("issue_id", Integer, ForeignKey("issues.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True),
)


class Tag(Base):
    """Tag model"""

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    color = Column(String, default="#6B7280", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    issues = relationship("Issue", secondary=issue_tags, back_populates="tags")

    def __repr__(self):
        return f"<Tag(id={self.id}, name={self.name})>"
