"""
Test User Endpoints
Mission 2: Records of Apprentices
"""

import pytest


def test_create_user(client, sample_user_data):
    """Test user creation"""
    response = client.post("/api/users/", json=sample_user_data)
    assert response.status_code == 201

    data = response.json()
    assert data["username"] == sample_user_data["username"]
    assert data["email"] == sample_user_data["email"]
    assert "id" in data
    assert "hashed_password" not in data  # Should not expose password
    assert data["guild_rank"] == "Apprentice"
    assert data["experience_points"] == 0


def test_create_duplicate_user(client, sample_user_data):
    """Test that duplicate users are rejected"""
    # Create first user
    client.post("/api/users/", json=sample_user_data)

    # Try to create duplicate
    response = client.post("/api/users/", json=sample_user_data)
    assert response.status_code == 400


def test_get_users(client, sample_user_data):
    """Test getting list of users"""
    # Create a user
    client.post("/api/users/", json=sample_user_data)

    # Get users
    response = client.get("/api/users/")
    assert response.status_code == 200

    users = response.json()
    assert isinstance(users, list)
    assert len(users) >= 1


def test_get_user_by_id(client, create_test_user):
    """Test getting specific user"""
    user_id = create_test_user["id"]

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200

    data = response.json()
    assert data["id"] == user_id
    assert data["username"] == create_test_user["username"]


def test_get_nonexistent_user(client):
    """Test 404 for non-existent user"""
    response = client.get("/api/users/999999")
    assert response.status_code == 404


def test_update_user(client, create_test_user, auth_headers):
    """Test updating user information"""
    user_id = create_test_user["id"]

    update_data = {
        "full_name": "Updated Name",
        "email": "updated@example.com"
    }

    response = client.put(
        f"/api/users/{user_id}",
        json=update_data,
        headers=auth_headers
    )
    assert response.status_code == 200

    data = response.json()
    assert data["full_name"] == update_data["full_name"]


def test_complete_mission(client, create_test_user, auth_headers):
    """Test mission completion"""
    user_id = create_test_user["id"]

    response = client.post(
        f"/api/users/{user_id}/missions/1/complete?score=100",
        headers=auth_headers
    )
    assert response.status_code == 200

    data = response.json()
    assert "experience_earned" in data
    assert "guild_rank" in data
    assert data["experience_earned"] == 10  # 100/10


@pytest.mark.parametrize("username,email,password,expected_status", [
    ("validuser", "valid@email.com", "password123", 201),
    ("ab", "valid@email.com", "password123", 422),  # Username too short
    ("validuser", "invalid-email", "password123", 422),  # Invalid email
    ("validuser", "valid@email.com", "short", 422),  # Password too short
])
def test_user_validation(client, username, email, password, expected_status):
    """Test input validation for user creation"""
    response = client.post(
        "/api/users/",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )
    assert response.status_code == expected_status
