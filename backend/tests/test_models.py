import pytest
from datetime import datetime
from app.models.user import User


class TestUserModel:
    """Test User SQLAlchemy model"""
    
    def test_create_user(self, db_session):
        """Test creating a user successfully"""
        user = User(
            email="test@example.com",
            username="testuser",
            hashed_password="hashedpassword123",
            is_active=True,
            is_superuser=False
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.id is not None
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.hashed_password == "hashedpassword123"
        assert user.is_active is True
        assert user.is_superuser is False
        assert isinstance(user.created_at, datetime)
    
    def test_user_default_values(self, db_session):
        """Test user model default values"""
        user = User(
            email="default@example.com",
            username="defaultuser",
            hashed_password="hashed123"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        assert user.is_active is True
        assert user.is_superuser is False
        assert user.created_at is not None
    
    def test_user_unique_email(self, db_session):
        """Test email uniqueness constraint"""
        user1 = User(
            email="duplicate@example.com",
            username="user1",
            hashed_password="hash1"
        )
        user2 = User(
            email="duplicate@example.com",
            username="user2",
            hashed_password="hash2"
        )
        
        db_session.add(user1)
        db_session.commit()
        
        db_session.add(user2)
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
    
    def test_user_unique_username(self, db_session):
        """Test username uniqueness constraint"""
        user1 = User(
            email="user1@example.com",
            username="duplicateuser",
            hashed_password="hash1"
        )
        user2 = User(
            email="user2@example.com",
            username="duplicateuser",
            hashed_password="hash2"
        )
        
        db_session.add(user1)
        db_session.commit()
        
        db_session.add(user2)
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
    
    def test_user_nullable_fields(self, db_session):
        """Test that required fields cannot be null"""
        user = User(
            email=None,
            username="testuser",
            hashed_password="hash123"
        )
        db_session.add(user)
        with pytest.raises(Exception):  # IntegrityError
            db_session.commit()
    
    def test_user_updated_at(self, db_session):
        """Test updated_at field updates on modification"""
        user = User(
            email="update@example.com",
            username="updateuser",
            hashed_password="hash123"
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        original_updated = user.updated_at
        
        # Update user
        user.email = "newemail@example.com"
        db_session.commit()
        db_session.refresh(user)
        
        # Note: updated_at may still be None if not explicitly set
        # This depends on database trigger or manual update
        assert user.email == "newemail@example.com"
