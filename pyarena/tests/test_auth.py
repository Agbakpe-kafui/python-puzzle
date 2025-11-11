"""
Test Authentication Endpoints
Mission 3: Seal of the Keeper
"""


def test_register_user(client):
    """Test user registration"""
    user_data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "securepass123",
        "full_name": "New User"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 201

    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]


def test_login_success(client, sample_user_data):
    """Test successful login"""
    # Register user
    client.post("/api/auth/register", json=sample_user_data)

    # Login
    login_data = {
        "username": sample_user_data["username"],
        "password": sample_user_data["password"]
    }

    response = client.post(
        "/api/auth/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, sample_user_data):
    """Test login with incorrect password"""
    # Register user
    client.post("/api/auth/register", json=sample_user_data)

    # Try login with wrong password
    login_data = {
        "username": sample_user_data["username"],
        "password": "wrongpassword"
    }

    response = client.post(
        "/api/auth/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """Test login with non-existent user"""
    login_data = {
        "username": "nonexistent",
        "password": "password"
    }

    response = client.post(
        "/api/auth/token",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 401


def test_protected_endpoint_without_token(client):
    """Test accessing protected endpoint without token"""
    response = client.get("/api/users/me")
    assert response.status_code == 401


def test_protected_endpoint_with_token(client, auth_headers):
    """Test accessing protected endpoint with valid token"""
    response = client.get("/api/users/me", headers=auth_headers)
    assert response.status_code == 200

    data = response.json()
    assert "username" in data
    assert "email" in data


def test_protected_endpoint_invalid_token(client):
    """Test accessing protected endpoint with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/users/me", headers=headers)
    assert response.status_code == 401
