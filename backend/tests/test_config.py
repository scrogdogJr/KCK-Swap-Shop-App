import pytest
from pydantic import ValidationError
from backend.app.core.config import Settings


class TestSettings:
    """Test Settings configuration"""
    
    def test_settings_initialization(self, monkeypatch):
        """Test settings initialization with environment variables"""
        # Set required environment variables
        monkeypatch.setenv("POSTGRES_SERVER", "localhost")
        monkeypatch.setenv("POSTGRES_USER", "testuser")
        monkeypatch.setenv("POSTGRES_PASSWORD", "testpass")
        monkeypatch.setenv("POSTGRES_DB", "testdb")
        monkeypatch.setenv("SECRET_KEY", "test_secret_key_12345")
        
        settings = Settings()
        
        assert settings.POSTGRES_SERVER == "localhost"
        assert settings.POSTGRES_USER == "testuser"
        assert settings.POSTGRES_PASSWORD == "testpass"
        assert settings.POSTGRES_DB == "testdb"
        assert settings.SECRET_KEY == "test_secret_key_12345"
    
    def test_settings_default_values(self, monkeypatch):
        """Test settings default values"""
        monkeypatch.setenv("POSTGRES_SERVER", "localhost")
        monkeypatch.setenv("POSTGRES_USER", "testuser")
        monkeypatch.setenv("POSTGRES_PASSWORD", "testpass")
        monkeypatch.setenv("POSTGRES_DB", "testdb")
        monkeypatch.setenv("SECRET_KEY", "test_secret_key")
        
        settings = Settings()
        
        assert settings.PROJECT_NAME == "FastAPI App"
        assert settings.API_V1_STR == "/api/v1"
        assert settings.POSTGRES_PORT == "5432"
        assert settings.ALGORITHM == "HS256"
        assert settings.ACCESS_TOKEN_EXPIRE_MINUTES == 30
        assert settings.REFRESH_TOKEN_EXPIRE_DAYS == 7
    
    def test_database_url_property(self, monkeypatch):
        """Test DATABASE_URL property construction"""
        monkeypatch.setenv("POSTGRES_SERVER", "localhost")
        monkeypatch.setenv("POSTGRES_USER", "myuser")
        monkeypatch.setenv("POSTGRES_PASSWORD", "mypass")
        monkeypatch.setenv("POSTGRES_DB", "mydb")
        monkeypatch.setenv("POSTGRES_PORT", "5432")
        monkeypatch.setenv("SECRET_KEY", "test_key")
        
        settings = Settings()
        expected_url = "postgresql://myuser:mypass@localhost:5432/mydb"
        assert settings.DATABASE_URL == expected_url
    
    def test_settings_missing_required_field(self, monkeypatch):
        """Test settings raises error when required field is missing"""
        monkeypatch.delenv("POSTGRES_SERVER", raising=False)
        monkeypatch.delenv("POSTGRES_USER", raising=False)
        monkeypatch.delenv("POSTGRES_PASSWORD", raising=False)
        monkeypatch.delenv("POSTGRES_DB", raising=False)
        monkeypatch.delenv("SECRET_KEY", raising=False)
        
        with pytest.raises(ValidationError):
            Settings()
    
    def test_settings_custom_port(self, monkeypatch):
        """Test settings with custom port"""
        monkeypatch.setenv("POSTGRES_SERVER", "localhost")
        monkeypatch.setenv("POSTGRES_USER", "testuser")
        monkeypatch.setenv("POSTGRES_PASSWORD", "testpass")
        monkeypatch.setenv("POSTGRES_DB", "testdb")
        monkeypatch.setenv("POSTGRES_PORT", "5433")
        monkeypatch.setenv("SECRET_KEY", "test_key")
        
        settings = Settings()
        assert settings.POSTGRES_PORT == "5433"
        assert "5433" in settings.DATABASE_URL
    
    def test_cors_origins_default_empty(self, monkeypatch):
        """Test CORS origins defaults to empty list"""
        monkeypatch.setenv("POSTGRES_SERVER", "localhost")
        monkeypatch.setenv("POSTGRES_USER", "testuser")
        monkeypatch.setenv("POSTGRES_PASSWORD", "testpass")
        monkeypatch.setenv("POSTGRES_DB", "testdb")
        monkeypatch.setenv("SECRET_KEY", "test_key")
        
        settings = Settings()
        assert settings.BACKEND_CORS_ORIGINS == []
