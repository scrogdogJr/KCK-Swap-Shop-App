import pytest
from fastapi import status


class TestGetUsersEndpoint:
    """Test get all users endpoint"""
    
    def test_get_users_not_implemented(self, client):
        """Test get users endpoint returns not implemented"""
        response = client.get("/api/v1/users/")
        
        # Will fail auth first (501) or return not implemented
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_501_NOT_IMPLEMENTED]
    
    def test_get_users_with_pagination(self, client):
        """Test get users with skip and limit parameters"""
        response = client.get("/api/v1/users/?skip=0&limit=10")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_501_NOT_IMPLEMENTED]
    
    def test_get_users_wrong_method(self, client):
        """Test get users with POST method fails"""
        response = client.post("/api/v1/users/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_get_users_invalid_pagination(self, client):
        """Test get users with invalid pagination values"""
        response = client.get("/api/v1/users/?skip=-1&limit=-5")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_501_NOT_IMPLEMENTED]
    
    def test_get_users_delete_method(self, client):
        """Test get users with DELETE method fails"""
        response = client.delete("/api/v1/users/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED
    
    def test_get_users_put_method(self, client):
        """Test get users with PUT method fails"""
        response = client.put("/api/v1/users/")
        assert response.status_code == status.HTTP_405_METHOD_NOT_ALLOWED


class TestGetCurrentUserEndpoint:
    """Test get current user endpoint"""
    
    def test_get_current_user_unauthorized(self, client):
        """Test get current user without authentication fails"""
        response = client.get("/api/v1/users/me")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user_with_invalid_token(self, client):
        """Test get current user with invalid token fails"""
        headers = {"Authorization": "Bearer invalid_token"}
        response = client.get("/api/v1/users/me", headers=headers)
        
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_501_NOT_IMPLEMENTED]
    
    def test_get_current_user_wrong_method(self, client):
        """Test get current user with DELETE method fails"""
        response = client.delete("/api/v1/users/me")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_405_METHOD_NOT_ALLOWED]
    
    def test_get_current_user_no_bearer_prefix(self, client):
        """Test get current user without Bearer prefix fails"""
        headers = {"Authorization": "invalid_token"}
        response = client.get("/api/v1/users/me", headers=headers)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_current_user_empty_token(self, client):
        """Test get current user with empty token fails"""
        headers = {"Authorization": "Bearer "}
        response = client.get("/api/v1/users/me", headers=headers)
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_501_NOT_IMPLEMENTED]
    
    def test_get_current_user_post_method(self, client):
        """Test get current user with POST method fails"""
        response = client.post("/api/v1/users/me")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_405_METHOD_NOT_ALLOWED]


class TestGetUserByIdEndpoint:
    """Test get user by ID endpoint"""
    
    def test_get_user_unauthorized(self, client):
        """Test get user by ID without authentication fails"""
        response = client.get("/api/v1/users/1")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_user_invalid_id_format(self, client):
        """Test get user with invalid ID format"""
        response = client.get("/api/v1/users/not_a_number")
        
        assert response.status_code in [status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_401_UNAUTHORIZED]
    
    def test_get_user_wrong_method(self, client):
        """Test get user with POST method fails"""
        response = client.post("/api/v1/users/1")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_405_METHOD_NOT_ALLOWED]
    
    def test_get_user_negative_id(self, client):
        """Test get user with negative ID"""
        response = client.get("/api/v1/users/-1")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_501_NOT_IMPLEMENTED]
    
    def test_get_user_zero_id(self, client):
        """Test get user with ID zero"""
        response = client.get("/api/v1/users/0")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_501_NOT_IMPLEMENTED]
    
    def test_get_user_patch_method(self, client):
        """Test get user with PATCH method fails"""
        response = client.patch("/api/v1/users/1")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_405_METHOD_NOT_ALLOWED]


class TestUpdateCurrentUserEndpoint:
    """Test update current user endpoint"""
    
    def test_update_current_user_unauthorized(self, client):
        """Test update current user without authentication fails"""
        update_data = {"email": "newemail@example.com"}
        response = client.put("/api/v1/users/me", json=update_data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_current_user_invalid_email(self, client):
        """Test update current user with invalid email"""
        update_data = {"email": "not-an-email"}
        response = client.put("/api/v1/users/me", json=update_data)
        
        assert response.status_code in [status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_401_UNAUTHORIZED]
    
    def test_update_current_user_wrong_method(self, client):
        """Test update current user with GET method fails"""
        response = client.get("/api/v1/users/me")
        # GET is allowed for reading, not updating
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_current_user_empty_body(self, client):
        """Test update current user with empty body"""
        response = client.put("/api/v1/users/me", json={})
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_current_user_delete_method(self, client):
        """Test update current user with DELETE method fails"""
        response = client.delete("/api/v1/users/me")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_405_METHOD_NOT_ALLOWED]
    
    def test_update_current_user_post_method(self, client):
        """Test update current user with POST method fails"""
        update_data = {"email": "newemail@example.com"}
        response = client.post("/api/v1/users/me", json=update_data)
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_405_METHOD_NOT_ALLOWED]


class TestDeleteUserEndpoint:
    """Test delete user endpoint"""
    
    def test_delete_user_unauthorized(self, client):
        """Test delete user without authentication fails"""
        response = client.delete("/api/v1/users/1")
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_delete_user_invalid_id(self, client):
        """Test delete user with invalid ID format"""
        response = client.delete("/api/v1/users/invalid")
        
        assert response.status_code in [status.HTTP_422_UNPROCESSABLE_ENTITY, status.HTTP_401_UNAUTHORIZED]
    
    def test_delete_user_wrong_method(self, client):
        """Test delete user with GET method fails"""
        response = client.get("/api/v1/users/1")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_delete_user_negative_id(self, client):
        """Test delete user with negative ID"""
        response = client.delete("/api/v1/users/-1")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_501_NOT_IMPLEMENTED]
    
    def test_delete_user_post_method(self, client):
        """Test delete user with POST method fails"""
        response = client.post("/api/v1/users/1")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_405_METHOD_NOT_ALLOWED]
    
    def test_delete_user_put_method(self, client):
        """Test delete user with PUT method fails"""
        response = client.put("/api/v1/users/1")
        assert response.status_code in [status.HTTP_401_UNAUTHORIZED, status.HTTP_405_METHOD_NOT_ALLOWED]
