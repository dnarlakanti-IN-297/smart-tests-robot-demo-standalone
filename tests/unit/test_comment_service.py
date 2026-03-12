"""Unit tests for CommentService"""

import pytest
from fastapi import HTTPException

from app.schemas.comment import CommentCreate, CommentUpdate
from app.services.comment_service import CommentService


@pytest.mark.unit
class TestCommentService:
    """Test cases for CommentService"""

    def test_create_comment(self, db_session, test_issue, test_user):
        """Test creating a comment"""
        service = CommentService(db_session)
        comment_data = CommentCreate(content="Test comment", issue_id=test_issue.id)

        comment = service.create(comment_data, test_user)

        assert comment.id is not None
        assert comment.content == "Test comment"
        assert comment.issue_id == test_issue.id
        assert comment.author_id == test_user.id

    def test_create_comment_for_nonexistent_issue(self, db_session, test_user):
        """Test creating comment for non-existent issue fails"""
        service = CommentService(db_session)
        comment_data = CommentCreate(content="Comment", issue_id=99999)

        with pytest.raises(HTTPException) as exc_info:
            service.create(comment_data, test_user)

        assert exc_info.value.status_code == 404

    def test_get_comment_by_id(self, db_session, test_issue, test_user):
        """Test getting comment by ID"""
        service = CommentService(db_session)

        # Create comment
        comment_data = CommentCreate(content="Test comment", issue_id=test_issue.id)
        created_comment = service.create(comment_data, test_user)

        # Get comment
        comment = service.get_by_id(created_comment.id)

        assert comment.id == created_comment.id
        assert comment.content == "Test comment"

    def test_get_comment_by_id_not_found(self, db_session):
        """Test getting non-existent comment raises exception"""
        service = CommentService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.get_by_id(99999)

        assert exc_info.value.status_code == 404

    def test_get_comments_by_issue(self, db_session, test_issue, test_user):
        """Test getting comments for an issue"""
        service = CommentService(db_session)

        # Create multiple comments
        for i in range(3):
            comment_data = CommentCreate(content=f"Comment {i}", issue_id=test_issue.id)
            service.create(comment_data, test_user)

        # Get comments
        comments = service.get_by_issue(test_issue.id)

        assert len(comments) == 3
        assert all(c.issue_id == test_issue.id for c in comments)

    def test_update_comment(self, db_session, test_issue, test_user):
        """Test updating a comment"""
        service = CommentService(db_session)

        # Create comment
        comment_data = CommentCreate(content="Original", issue_id=test_issue.id)
        comment = service.create(comment_data, test_user)

        # Update comment
        update_data = CommentUpdate(content="Updated content")
        updated_comment = service.update(comment.id, update_data, test_user)

        assert updated_comment.content == "Updated content"

    def test_update_comment_by_non_author(self, db_session, test_issue, test_user, test_user2):
        """Test updating comment by non-author fails"""
        service = CommentService(db_session)

        # Create comment as user1
        comment_data = CommentCreate(content="User1 comment", issue_id=test_issue.id)
        comment = service.create(comment_data, test_user)

        # Try to update as user2
        update_data = CommentUpdate(content="Hacked content")

        with pytest.raises(HTTPException) as exc_info:
            service.update(comment.id, update_data, test_user2)

        assert exc_info.value.status_code == 403

    def test_delete_comment(self, db_session, test_issue, test_user):
        """Test deleting a comment"""
        service = CommentService(db_session)

        # Create comment
        comment_data = CommentCreate(content="To delete", issue_id=test_issue.id)
        comment = service.create(comment_data, test_user)

        # Delete comment
        service.delete(comment.id, test_user)

        # Verify deletion
        with pytest.raises(HTTPException):
            service.get_by_id(comment.id)

    def test_delete_comment_by_non_author(self, db_session, test_issue, test_user, test_user2):
        """Test deleting comment by non-author fails"""
        service = CommentService(db_session)

        # Create comment as user1
        comment_data = CommentCreate(content="User1 comment", issue_id=test_issue.id)
        comment = service.create(comment_data, test_user)

        # Try to delete as user2
        with pytest.raises(HTTPException) as exc_info:
            service.delete(comment.id, test_user2)

        assert exc_info.value.status_code == 403
