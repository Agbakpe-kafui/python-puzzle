"""
Pytest Configuration and Fixtures
Shared test utilities and fixtures for all tests
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Use in-memory SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """
    Create a fresh database for each test.
    This ensures test isolation.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """
    FastAPI test client with test database
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing"""
    return {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User"
    }


@pytest.fixture
def create_test_user(client, sample_user_data):
    """
    Create a test user and return the response
    """
    response = client.post("/api/users/", json=sample_user_data)
    return response.json()


@pytest.fixture
def get_auth_token(client, sample_user_data):
    """
    Create a user and get authentication token
    """
    # Create user
    client.post("/api/users/", json=sample_user_data)

    # Login to get token
    login_data = {
        "username": sample_user_data["username"],
        "password": sample_user_data["password"]
    }
    response = client.post(
        "/api/auth/token",
        data=login_data,  # OAuth2 uses form data
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    token = response.json()["access_token"]
    return token


@pytest.fixture
def auth_headers(get_auth_token):
    """
    Get authorization headers with valid token
    """
    return {"Authorization": f"Bearer {get_auth_token}"}
