import pytest
from unittest.mock import Mock, patch
from fastapi import HTTPException, status
from app.schemas.user import User
from backend.app.auth.dependencies import (
    require_user,
    get_current_active_user,
    get_current_active_superuser
)


class TestGetCurrentUser:
    """Test get_current_user dependency"""
    
    def test_get_current_user_not_implemented(self, db_session):
        """Test get_current_user raises not implemented"""
        with pytest.raises(HTTPException) as exc_info:
            require_user(db=db_session, token="fake_token")
        
        assert exc_info.value.status_code == status.HTTP_501_NOT_IMPLEMENTED
        assert "not implemented" in exc_info.value.detail.lower()
    
    def test_get_current_user_with_empty_token(self, db_session):
        """Test get_current_user with empty token"""
        with pytest.raises(HTTPException) as exc_info:
            require_user(db=db_session, token="")
        
        assert exc_info.value.status_code == status.HTTP_501_NOT_IMPLEMENTED
    
    def test_get_current_user_with_none_token(self, db_session):
        """Test get_current_user with None token"""
        with pytest.raises(HTTPException) as exc_info:
            require_user(db=db_session, token=None)
        
        assert exc_info.value.status_code == status.HTTP_501_NOT_IMPLEMENTED
    
    def test_get_current_user_with_invalid_token_format(self, db_session):
        """Test get_current_user with malformed token"""
        with pytest.raises(HTTPException) as exc_info:
            require_user(db=db_session, token="invalid.token.format")
        
        assert exc_info.value.status_code == status.HTTP_501_NOT_IMPLEMENTED
    
    def test_get_current_user_with_long_token(self, db_session):
        """Test get_current_user with very long token string"""
        long_token = "a" * 10000
        with pytest.raises(HTTPException) as exc_info:
            require_user(db=db_session, token=long_token)
        
        assert exc_info.value.status_code == status.HTTP_501_NOT_IMPLEMENTED
    
    def test_get_current_user_with_special_characters(self, db_session):
        """Test get_current_user with special characters in token"""
        special_token = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
        with pytest.raises(HTTPException) as exc_info:
            require_user(db=db_session, token=special_token)
        
        assert exc_info.value.status_code == status.HTTP_501_NOT_IMPLEMENTED


class TestGetCurrentActiveUser:
    """Test get_current_active_user dependency"""
    
    def test_get_current_active_user_with_active_user(self):
        """Test get_current_active_user returns active user"""
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        
        result = get_current_active_user(current_user=mock_user)
        assert result == mock_user
    
    def test_get_current_active_user_with_inactive_user(self):
        """Test get_current_active_user raises error for inactive user"""
        mock_user = Mock(spec=User)
        mock_user.is_active = False
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user(current_user=mock_user)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
        assert "inactive" in exc_info.value.detail.lower()
    
    def test_get_current_active_user_with_none_is_active(self):
        """Test get_current_active_user with None is_active value"""
        mock_user = Mock(spec=User)
        mock_user.is_active = None
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_user(current_user=mock_user)
        
        assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_get_current_active_user_preserves_user_data(self):
        """Test get_current_active_user preserves all user data"""
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        mock_user.id = 123
        mock_user.email = "test@example.com"
        
        result = get_current_active_user(current_user=mock_user)
        assert result.id == 123
        assert result.email == "test@example.com"
    
    def test_get_current_active_user_multiple_calls(self):
        """Test get_current_active_user can be called multiple times"""
        mock_user = Mock(spec=User)
        mock_user.is_active = True
        
        result1 = get_current_active_user(current_user=mock_user)
        result2 = get_current_active_user(current_user=mock_user)
        
        assert result1 == mock_user
        assert result2 == mock_user
    
    def test_get_current_active_user_with_string_is_active(self):
        """Test get_current_active_user with string 'False' (truthy)"""
        mock_user = Mock(spec=User)
        mock_user.is_active = "False"  # String is truthy
        
        # Should pass because "False" string is truthy in Python
        result = get_current_active_user(current_user=mock_user)
        assert result == mock_user


class TestGetCurrentActiveSuperuser:
    """Test get_current_active_superuser dependency"""
    
    def test_get_current_active_superuser_with_superuser(self):
        """Test get_current_active_superuser returns superuser"""
        mock_user = Mock(spec=User)
        mock_user.is_superuser = True
        
        result = get_current_active_superuser(current_user=mock_user)
        assert result == mock_user
    
    def test_get_current_active_superuser_with_regular_user(self):
        """Test get_current_active_superuser raises error for regular user"""
        mock_user = Mock(spec=User)
        mock_user.is_superuser = False
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_superuser(current_user=mock_user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
        assert "privilege" in exc_info.value.detail.lower()
    
    def test_get_current_active_superuser_with_none_is_superuser(self):
        """Test get_current_active_superuser with None is_superuser"""
        mock_user = Mock(spec=User)
        mock_user.is_superuser = None
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_superuser(current_user=mock_user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
    
    def test_get_current_active_superuser_preserves_user_data(self):
        """Test get_current_active_superuser preserves user data"""
        mock_user = Mock(spec=User)
        mock_user.is_superuser = True
        mock_user.id = 1
        mock_user.email = "admin@example.com"
        
        result = get_current_active_superuser(current_user=mock_user)
        assert result.id == 1
        assert result.email == "admin@example.com"
    
    def test_get_current_active_superuser_multiple_calls(self):
        """Test get_current_active_superuser can be called multiple times"""
        mock_user = Mock(spec=User)
        mock_user.is_superuser = True
        
        result1 = get_current_active_superuser(current_user=mock_user)
        result2 = get_current_active_superuser(current_user=mock_user)
        
        assert result1 == mock_user
        assert result2 == mock_user
    
    def test_get_current_active_superuser_with_zero_is_superuser(self):
        """Test get_current_active_superuser with zero (falsy) is_superuser"""
        mock_user = Mock(spec=User)
        mock_user.is_superuser = 0
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_active_superuser(current_user=mock_user)
        
        assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
