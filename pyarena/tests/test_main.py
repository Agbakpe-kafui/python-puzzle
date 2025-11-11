"""
Test Main Application Endpoints
"""

def test_read_root(client):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data
    assert data["missions"] == 13


def test_ping(client):
    """Test health check endpoint"""
    response = client.get("/ping")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "The Guild is alive"
    assert data["status"] == "operational"


def test_list_missions(client):
    """Test missions list endpoint"""
    response = client.get("/missions")
    assert response.status_code == 200
    data = response.json()
    assert "missions" in data
    assert data["total"] == 13
    assert len(data["missions"]) == 13

    # Check first mission
    first_mission = data["missions"][0]
    assert first_mission["id"] == 1
    assert first_mission["name"] == "The First Flame"
    assert first_mission["focus"] == "FastAPI Basics"


def test_docs_available(client):
    """Test that API documentation is available"""
    response = client.get("/docs")
    assert response.status_code == 200


def test_redoc_available(client):
    """Test that ReDoc documentation is available"""
    response = client.get("/redoc")
    assert response.status_code == 200
