"""Unit tests for TagService"""

import pytest
from fastapi import HTTPException

from app.schemas.tag import TagCreate
from app.services.tag_service import TagService


@pytest.mark.unit
class TestTagService:
    """Test cases for TagService"""

    def test_create_tag(self, db_session):
        """Test creating a tag"""
        service = TagService(db_session)
        tag_data = TagCreate(name="new-tag", color="#FF5733")

        tag = service.create(tag_data)

        assert tag.id is not None
        assert tag.name == "new-tag"
        assert tag.color == "#FF5733"

    def test_create_tag_duplicate_name(self, db_session, test_tag):
        """Test creating tag with duplicate name fails"""
        service = TagService(db_session)
        tag_data = TagCreate(name=test_tag.name, color="#000000")

        with pytest.raises(HTTPException) as exc_info:
            service.create(tag_data)

        assert exc_info.value.status_code == 400
        assert "already exists" in str(exc_info.value.detail)

    def test_create_tag_default_color(self, db_session):
        """Test creating tag with default color"""
        service = TagService(db_session)
        tag_data = TagCreate(name="default-color")

        tag = service.create(tag_data)

        assert tag.color == "#6B7280"

    def test_get_tag_by_id(self, db_session, test_tag):
        """Test getting tag by ID"""
        service = TagService(db_session)

        tag = service.get_by_id(test_tag.id)

        assert tag.id == test_tag.id
        assert tag.name == test_tag.name

    def test_get_tag_by_id_not_found(self, db_session):
        """Test getting non-existent tag raises exception"""
        service = TagService(db_session)

        with pytest.raises(HTTPException) as exc_info:
            service.get_by_id(99999)

        assert exc_info.value.status_code == 404

    def test_get_all_tags(self, db_session, test_tag):
        """Test getting all tags"""
        service = TagService(db_session)

        tags = service.get_all()

        assert len(tags) >= 1
        assert test_tag.id in [t.id for t in tags]

    def test_delete_tag(self, db_session, test_tag):
        """Test deleting a tag"""
        service = TagService(db_session)

        service.delete(test_tag.id)

        with pytest.raises(HTTPException):
            service.get_by_id(test_tag.id)
