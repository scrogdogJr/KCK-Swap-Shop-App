import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas.user import UserCreate, UserUpdate, User, UserInDB
from app.schemas.token import Token, TokenPayload


class TestUserSchemas:
    """Test User Pydantic schemas"""
    
    def test_user_create_valid(self):
        """Test creating valid UserCreate schema"""
        user_data = {
            "email": "test@example.com",
            "username": "testuser",
            "password": "password123"
        }
        user = UserCreate(**user_data)
        
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.password == "password123"
        assert user.is_active is True
        assert user.is_superuser is False
    
    def test_user_create_invalid_email(self):
        """Test UserCreate with invalid email format"""
        user_data = {
            "email": "invalid-email",
            "username": "testuser",
            "password": "password123"
        }
        with pytest.raises(ValidationError):
            UserCreate(**user_data)
    
    def test_user_create_missing_required_fields(self):
        """Test UserCreate missing required fields"""
        with pytest.raises(ValidationError):
            UserCreate(username="testuser")
    
    def test_user_update_all_optional(self):
        """Test UserUpdate with all fields optional"""
        user_update = UserUpdate()
        assert user_update.email is None
        assert user_update.username is None
        assert user_update.password is None
    
    def test_user_update_partial(self):
        """Test UserUpdate with partial data"""
        user_update = UserUpdate(email="newemail@example.com")
        assert user_update.email == "newemail@example.com"
        assert user_update.username is None
    
    def test_user_update_invalid_email(self):
        """Test UserUpdate with invalid email"""
        with pytest.raises(ValidationError):
            UserUpdate(email="not-an-email")
    
    def test_user_schema_from_orm(self):
        """Test User schema from ORM model"""
        user_data = {
            "id": 1,
            "email": "test@example.com",
            "username": "testuser",
            "is_active": True,
            "is_superuser": False,
            "created_at": datetime.now(),
            "updated_at": None
        }
        user = User(**user_data)
        
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.username == "testuser"
    
    def test_user_in_db_with_hashed_password(self):
        """Test UserInDB includes hashed_password"""
        user_data = {
            "id": 1,
            "email": "test@example.com",
            "username": "testuser",
            "hashed_password": "hashedpassword123",
            "is_active": True,
            "is_superuser": False,
            "created_at": datetime.now(),
            "updated_at": None
        }
        user = UserInDB(**user_data)
        
        assert user.hashed_password == "hashedpassword123"
    
    def test_user_in_db_missing_hashed_password(self):
        """Test UserInDB requires hashed_password"""
        user_data = {
            "id": 1,
            "email": "test@example.com",
            "username": "testuser",
            "is_active": True,
            "is_superuser": False,
            "created_at": datetime.now()
        }
        with pytest.raises(ValidationError):
            UserInDB(**user_data)
    
    def test_user_create_with_superuser_flag(self):
        """Test creating UserCreate with superuser flag"""
        user_data = {
            "email": "admin@example.com",
            "username": "admin",
            "password": "adminpass",
            "is_superuser": True
        }
        user = UserCreate(**user_data)
        assert user.is_superuser is True


class TestTokenSchemas:
    """Test Token Pydantic schemas"""
    
    def test_token_schema_valid(self):
        """Test creating valid Token schema"""
        token_data = {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9refresh",
            "token_type": "bearer"
        }
        token = Token(**token_data)
        
        assert token.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
        assert token.refresh_token == "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9refresh"
        assert token.token_type == "bearer"
    
    def test_token_schema_default_type(self):
        """Test Token schema has default token_type"""
        token_data = {
            "access_token": "access123",
            "refresh_token": "refresh456"
        }
        token = Token(**token_data)
        assert token.token_type == "bearer"
    
    def test_token_schema_missing_required_fields(self):
        """Test Token schema requires access and refresh tokens"""
        with pytest.raises(ValidationError):
            Token(access_token="access123")
    
    def test_token_payload_optional_sub(self):
        """Test TokenPayload with optional sub field"""
        payload = TokenPayload()
        assert payload.sub is None
    
    def test_token_payload_with_sub(self):
        """Test TokenPayload with sub field"""
        payload = TokenPayload(sub=123)
        assert payload.sub == 123
    
    def test_token_payload_invalid_sub_type(self):
        """Test TokenPayload with invalid sub type"""
        with pytest.raises(ValidationError):
            TokenPayload(sub="not an integer")
