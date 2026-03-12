"""Seed database with sample data"""

from app.auth.password import get_password_hash
from app.database import SessionLocal
from app.models.issue import Issue, IssuePriority, IssueStatus, IssueType
from app.models.project import Project, ProjectMember, ProjectRole
from app.models.tag import Tag
from app.models.user import User, UserRole


def seed_data():
    """Seed database with sample data"""
    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(User).first():
            print("Database already contains data. Skipping seed.")
            return

        print("Seeding database with sample data...")

        # Create users
        admin_user = User(
            email="admin@example.com",
            username="admin",
            full_name="Admin User",
            hashed_password=get_password_hash("admin123"),
            role=UserRole.ADMIN.value,
        )
        db.add(admin_user)

        user1 = User(
            email="john@example.com",
            username="john",
            full_name="John Doe",
            hashed_password=get_password_hash("password123"),
            role=UserRole.USER.value,
        )
        db.add(user1)

        user2 = User(
            email="jane@example.com",
            username="jane",
            full_name="Jane Smith",
            hashed_password=get_password_hash("password123"),
            role=UserRole.USER.value,
        )
        db.add(user2)

        db.commit()
        print("✓ Created 3 users")

        # Create tags
        tags = [
            Tag(name="backend", color="#3B82F6"),
            Tag(name="frontend", color="#10B981"),
            Tag(name="ui", color="#8B5CF6"),
            Tag(name="database", color="#F59E0B"),
            Tag(name="urgent", color="#EF4444"),
        ]
        for tag in tags:
            db.add(tag)
        db.commit()
        print("✓ Created 5 tags")

        # Create projects
        project1 = Project(
            name="Issue Tracker",
            key="IT",
            description="Main issue tracking system",
        )
        db.add(project1)

        project2 = Project(
            name="Web Dashboard",
            key="WD",
            description="Admin dashboard for analytics",
        )
        db.add(project2)

        db.commit()
        print("✓ Created 2 projects")

        # Add project members
        members = [
            ProjectMember(project_id=project1.id, user_id=admin_user.id, role=ProjectRole.OWNER.value),
            ProjectMember(project_id=project1.id, user_id=user1.id, role=ProjectRole.MEMBER.value),
            ProjectMember(project_id=project1.id, user_id=user2.id, role=ProjectRole.MEMBER.value),
            ProjectMember(project_id=project2.id, user_id=admin_user.id, role=ProjectRole.OWNER.value),
            ProjectMember(project_id=project2.id, user_id=user2.id, role=ProjectRole.MEMBER.value),
        ]
        for member in members:
            db.add(member)
        db.commit()
        print("✓ Added project members")

        # Create issues for Project 1
        issues = [
            Issue(
                title="Setup authentication system",
                description="Implement JWT authentication with login and registration",
                status=IssueStatus.RESOLVED.value,
                type=IssueType.FEATURE.value,
                priority=IssuePriority.HIGH.value,
                project_id=project1.id,
                creator_id=admin_user.id,
                assignee_id=user1.id,
            ),
            Issue(
                title="Fix database connection pool",
                description="Database connections are not being released properly",
                status=IssueStatus.CLOSED.value,
                type=IssueType.BUG.value,
                priority=IssuePriority.CRITICAL.value,
                project_id=project1.id,
                creator_id=user1.id,
                assignee_id=user1.id,
            ),
            Issue(
                title="Add project creation feature",
                description="Users should be able to create and manage projects",
                status=IssueStatus.IN_PROGRESS.value,
                type=IssueType.FEATURE.value,
                priority=IssuePriority.HIGH.value,
                project_id=project1.id,
                creator_id=admin_user.id,
                assignee_id=user2.id,
            ),
            Issue(
                title="Update UI design",
                description="Modernize the user interface with new design system",
                status=IssueStatus.OPEN.value,
                type=IssueType.ENHANCEMENT.value,
                priority=IssuePriority.MEDIUM.value,
                project_id=project1.id,
                creator_id=user2.id,
                assignee_id=user2.id,
            ),
            Issue(
                title="Write API documentation",
                description="Document all API endpoints with examples",
                status=IssueStatus.OPEN.value,
                type=IssueType.TASK.value,
                priority=IssuePriority.LOW.value,
                project_id=project1.id,
                creator_id=admin_user.id,
                assignee_id=None,
            ),
        ]

        for issue in issues:
            db.add(issue)
        db.commit()

        # Add tags to issues
        issues[0].tags = [tags[0]]  # backend
        issues[1].tags = [tags[0], tags[3], tags[4]]  # backend, database, urgent
        issues[2].tags = [tags[0]]  # backend
        issues[3].tags = [tags[1], tags[2]]  # frontend, ui
        issues[4].tags = []

        # Create issues for Project 2
        issues_p2 = [
            Issue(
                title="Create dashboard layout",
                description="Design and implement the main dashboard layout",
                status=IssueStatus.IN_PROGRESS.value,
                type=IssueType.TASK.value,
                priority=IssuePriority.HIGH.value,
                project_id=project2.id,
                creator_id=admin_user.id,
                assignee_id=user2.id,
            ),
            Issue(
                title="Add analytics widgets",
                description="Implement various analytics widgets for the dashboard",
                status=IssueStatus.OPEN.value,
                type=IssueType.FEATURE.value,
                priority=IssuePriority.MEDIUM.value,
                project_id=project2.id,
                creator_id=admin_user.id,
                assignee_id=None,
            ),
        ]

        for issue in issues_p2:
            db.add(issue)
        db.commit()

        issues_p2[0].tags = [tags[1], tags[2]]  # frontend, ui
        issues_p2[1].tags = [tags[1]]  # frontend

        db.commit()
        print(f"✓ Created {len(issues) + len(issues_p2)} issues")

        print("\n✅ Database seeded successfully!")
        print("\nTest accounts:")
        print("  Admin: admin / admin123")
        print("  User 1: john / password123")
        print("  User 2: jane / password123")

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_data()
