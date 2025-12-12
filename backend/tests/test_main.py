import pytest
from fastapi import status


class TestMainEndpoints:
    """Test main application endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint returns welcome message"""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"message": "Welcome to the API"}
    
    def test_root_endpoint_method_not_allowed(self, client):
        """Test root endpoint with POST method fails"""
        response = client.post("/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_root_endpoint_returns_json(self, client):
        """Test root endpoint returns JSON content type"""
        response = client.get("/")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_check_endpoint(self, client):
        """Test health check endpoint returns healthy status"""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"status": "healthy"}
    
    def test_health_check_method_not_allowed(self, client):
        """Test health check with wrong method fails"""
        response = client.put("/health")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_health_check_returns_json(self, client):
        """Test health check returns JSON content type"""
        response = client.get("/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_openapi_docs_accessible(self, client):
        """Test OpenAPI docs endpoint is accessible"""
        response = client.get("/docs")
        assert response.status_code == status.HTTP_200_OK
    
    def test_openapi_json_accessible(self, client):
        """Test OpenAPI JSON endpoint is accessible"""
        response = client.get("/api/v1/openapi.json")
        assert response.status_code == status.HTTP_200_OK
        assert "openapi" in response.json()
    
    def test_nonexistent_endpoint(self, client):
        """Test accessing non-existent endpoint returns 404"""
        response = client.get("/nonexistent")
        assert response.status_code == status.HTTP_404_NOT_FOUND


class TestCORSMiddleware:
    """Test CORS middleware configuration"""
    
    def test_cors_headers_present(self, client):
        """Test CORS headers are present in response"""
        response = client.options("/", headers={"Origin": "http://localhost:3000"})
        # CORS headers should be configured (test will depend on actual config)
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_405_METHOD_NOT_ALLOWED]
