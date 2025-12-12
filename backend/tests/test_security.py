import pytest
from datetime import datetime, timedelta, UTC
from jose import jwt
from backend.app.core.config import settings
from backend.app.auth.security import (
    create_access_token,
    create_refresh_token,
    verify_password,
    get_password_hash
)


class TestCreateAccessToken:
    """Test create_access_token function"""
    
    def test_create_access_token_with_default_expiry(self):
        """Test creating access token with default expiration"""
        data = {"sub": "123"}
        token = create_access_token(data)
        
        # Decode and verify token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "123"
        assert "exp" in payload
        
        # Verify expiration is approximately correct (within 1 minute tolerance)
        expected_exp = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        actual_exp = datetime.fromtimestamp(payload["exp"], tz=UTC)
        assert abs((expected_exp - actual_exp).total_seconds()) < 60
    
    def test_create_access_token_with_custom_expiry(self):
        """Test creating access token with custom expiration delta"""
        data = {"sub": "456"}
        custom_delta = timedelta(minutes=60)
        token = create_access_token(data, expires_delta=custom_delta)
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "456"
        
        # Verify custom expiration
        expected_exp = datetime.now(UTC) + custom_delta
        actual_exp = datetime.fromtimestamp(payload["exp"], tz=UTC)
        assert abs((expected_exp - actual_exp).total_seconds()) < 60
    
    def test_create_access_token_with_empty_data(self):
        """Test creating access token with empty data dictionary"""
        token = create_access_token({})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert "exp" in payload
    
    def test_create_access_token_with_invalid_data_type(self):
        """Test creating access token with non-dict data raises error"""
        with pytest.raises(AttributeError):
            create_access_token("not a dict")
    
    def test_create_access_token_with_none_data(self):
        """Test creating access token with None data raises error"""
        with pytest.raises(AttributeError):
            create_access_token(None)


class TestCreateRefreshToken:
    """Test create_refresh_token function"""
    
    def test_create_refresh_token_success(self):
        """Test creating refresh token successfully"""
        data = {"sub": "789"}
        token = create_refresh_token(data)
        
        # Decode and verify token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "789"
        assert "exp" in payload
        
        # Verify expiration is approximately correct (within 1 minute tolerance)
        expected_exp = datetime.now(UTC) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        actual_exp = datetime.fromtimestamp(payload["exp"], tz=UTC)
        assert abs((expected_exp - actual_exp).total_seconds()) < 120
    
    def test_create_refresh_token_with_multiple_fields(self):
        """Test creating refresh token with multiple data fields"""
        data = {"sub": "999", "role": "admin", "email": "test@example.com"}
        token = create_refresh_token(data)
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert payload["sub"] == "999"
        assert payload["role"] == "admin"
        assert payload["email"] == "test@example.com"
    
    def test_create_refresh_token_with_empty_data(self):
        """Test creating refresh token with empty data"""
        token = create_refresh_token({})
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        assert "exp" in payload
    
    def test_create_refresh_token_with_invalid_data_type(self):
        """Test creating refresh token with non-dict data raises error"""
        with pytest.raises(AttributeError):
            create_refresh_token([1, 2, 3])
    
    def test_create_refresh_token_with_none_data(self):
        """Test creating refresh token with None data raises error"""
        with pytest.raises(AttributeError):
            create_refresh_token(None)


class TestVerifyPassword:
    """Test verify_password function"""
    
    def test_verify_password_correct(self):
        """Test verifying correct password"""
        plain_password = "MySecurePassword123!"
        hashed_password = get_password_hash(plain_password)
        
        assert verify_password(plain_password, hashed_password) is True
    
    def test_verify_password_incorrect(self):
        """Test verifying incorrect password returns False"""
        plain_password = "MySecurePassword123!"
        wrong_password = "WrongPassword456!"
        hashed_password = get_password_hash(plain_password)
        
        assert verify_password(wrong_password, hashed_password) is False
    
    def test_verify_password_empty_string(self):
        """Test verifying empty password returns False"""
        plain_password = "MySecurePassword123!"
        hashed_password = get_password_hash(plain_password)
        
        assert verify_password("", hashed_password) is False
    
    def test_verify_password_case_sensitive(self):
        """Test password verification is case sensitive"""
        plain_password = "MyPassword"
        hashed_password = get_password_hash(plain_password)
        
        assert verify_password("mypassword", hashed_password) is False
    
    def test_verify_password_with_special_characters(self):
        """Test verifying password with special characters"""
        plain_password = "P@ssw0rd!#$%^&*()"
        hashed_password = get_password_hash(plain_password)
        
        assert verify_password(plain_password, hashed_password) is True
    
    def test_verify_password_whitespace_matters(self):
        """Test that whitespace in password matters"""
        plain_password = "MyPassword"
        hashed_password = get_password_hash(plain_password)
        
        assert verify_password("MyPassword ", hashed_password) is False
        assert verify_password(" MyPassword", hashed_password) is False


class TestGetPasswordHash:
    """Test get_password_hash function"""
    
    def test_get_password_hash_creates_hash(self):
        """Test password hashing creates a hash string"""
        password = "TestPassword123!"
        hashed = get_password_hash(password)
        
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password
    
    def test_get_password_hash_different_hashes(self):
        """Test same password produces different hashes (salt)"""
        password = "TestPassword123!"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Bcrypt uses random salt, so hashes should be different
        assert hash1 != hash2
        # But both should verify against the original password
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
    
    def test_get_password_hash_empty_password(self):
        """Test hashing empty password"""
        hashed = get_password_hash("")
        assert isinstance(hashed, str)
        assert len(hashed) > 0
    
    def test_get_password_hash_long_password(self):
        """Test hashing very long password"""
        long_password = "a" * 1000
        hashed = get_password_hash(long_password)
        assert verify_password(long_password, hashed) is True
    
    def test_get_password_hash_unicode_characters(self):
        """Test hashing password with unicode characters"""
        unicode_password = "密码🔒Test123"
        hashed = get_password_hash(unicode_password)
        assert verify_password(unicode_password, hashed) is True
    
    def test_get_password_hash_special_characters(self):
        """Test hashing password with special characters"""
        special_password = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        hashed = get_password_hash(special_password)
        assert verify_password(special_password, hashed) is True
