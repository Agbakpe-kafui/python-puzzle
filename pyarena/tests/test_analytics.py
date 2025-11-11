"""
Test Analytics Endpoints
Mission 6: The Guild Archives
"""


def test_get_user_statistics(client, create_test_user):
    """Test user statistics endpoint"""
    response = client.get("/api/analytics/users/stats")
    assert response.status_code == 200

    data = response.json()
    assert "total_users" in data
    assert "active_users" in data
    assert "total_missions_completed" in data
    assert "average_experience" in data
    assert data["total_users"] >= 1


def test_get_mission_statistics(client):
    """Test mission statistics endpoint"""
    response = client.get("/api/analytics/missions/stats")
    assert response.status_code == 200

    data = response.json()
    assert "missions" in data
    assert isinstance(data["missions"], list)


def test_get_leaderboard(client, create_test_user):
    """Test leaderboard endpoint"""
    response = client.get("/api/analytics/leaderboard?limit=10")
    assert response.status_code == 200

    data = response.json()
    assert "leaderboard" in data
    assert isinstance(data["leaderboard"], list)

    if len(data["leaderboard"]) > 0:
        entry = data["leaderboard"][0]
        assert "rank" in entry
        assert "username" in entry
        assert "experience_points" in entry


def test_get_user_performance(client, create_test_user, auth_headers):
    """Test user performance analytics"""
    user_id = create_test_user["id"]

    response = client.get(
        f"/api/analytics/users/{user_id}/performance",
        headers=auth_headers
    )
    assert response.status_code == 200

    data = response.json()
    assert data["user_id"] == user_id
    assert "missions_attempted" in data
    assert "missions_completed" in data
    assert "completion_rate" in data
