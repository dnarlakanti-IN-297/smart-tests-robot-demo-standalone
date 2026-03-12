"""Initialize database tables"""

from app.database import Base, engine
from app.models import Comment, Issue, Project, ProjectMember, Tag, User, issue_tags

def init_db():
    """Create all database tables"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")


if __name__ == "__main__":
    init_db()
