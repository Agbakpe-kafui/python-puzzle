# 🧪 Mission 8: Circle of Truth

**Status**: Core
**Difficulty**: Intermediate
**Focus**: Testing with pytest & CI/CD

---

## 🎯 Mission Objective

Ensure your Guild stands on solid ground! Master automated testing with pytest, write comprehensive test suites, and set up continuous integration to catch bugs before they reach production.

---

## 📚 What You'll Learn

- pytest fundamentals
- Unit testing FastAPI endpoints
- Test fixtures and parametrization
- Mocking and test databases
- Code coverage analysis
- CI/CD with GitHub Actions
- Test-driven development (TDD)

---

## ✅ Tasks

### 1. Explore Existing Tests

Check out `tests/` directory:

```bash
# Run tests
cd pyarena
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_users.py

# Run with verbose output
poetry run pytest -v
```

### 2. Write Tests for User Endpoints

Create comprehensive user endpoint tests in `tests/test_users.py`:

```python
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.models import User

client = TestClient(app)

@pytest.fixture
def test_db():
    """
    TODO: Create test database fixture
    - Create tables before tests
    - Clean up after tests
    - Yield database session
    """
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_user(test_db):
    """
    TODO: Test user creation
    - Send POST request to /api/users/
    - Assert status code 201
    - Assert response contains user data
    - Assert user is in database
    """
    response = client.post(
        "/api/users/",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_create_duplicate_user(test_db):
    """
    TODO: Test duplicate user handling
    - Create a user
    - Try to create same user again
    - Assert 400 error
    """
    pass


def test_get_users(test_db):
    """
    TODO: Test getting user list
    - Create several test users
    - GET /api/users/
    - Assert all users returned
    """
    pass


def test_get_user_by_id(test_db):
    """
    TODO: Test getting specific user
    - Create test user
    - GET /api/users/{id}
    - Assert correct user returned
    """
    pass


def test_get_nonexistent_user(test_db):
    """
    TODO: Test 404 error
    - GET /api/users/999999
    - Assert 404 status
    """
    pass
```

### 3. Write Authentication Tests

Create `tests/test_auth.py`:

```python
def test_user_registration():
    """
    TODO: Test registration endpoint
    - POST to /api/auth/register
    - Assert user created
    - Assert password is hashed
    """
    pass


def test_user_login():
    """
    TODO: Test login flow
    - Create user
    - Login with correct credentials
    - Assert token returned
    - Verify token format (JWT)
    """
    pass


def test_login_wrong_password():
    """
    TODO: Test failed login
    - Create user
    - Login with wrong password
    - Assert 401 error
    """
    pass


def test_protected_endpoint_without_token():
    """
    TODO: Test authentication requirement
    - Call protected endpoint without token
    - Assert 401 error
    """
    pass


def test_protected_endpoint_with_token():
    """
    TODO: Test authenticated access
    - Create user and get token
    - Call protected endpoint with token
    - Assert success
    """
    pass
```

### 4. Test External API Integration

Create `tests/test_external.py`:

```python
import pytest
from unittest.mock import patch, AsyncMock

@pytest.mark.asyncio
async def test_fetch_external_api():
    """
    TODO: Test external API fetching
    - Mock httpx client
    - Test successful response
    - Assert data parsed correctly
    """
    with patch('httpx.AsyncClient.get') as mock_get:
        mock_get.return_value = AsyncMock(
            status_code=200,
            json=lambda: {"data": "test"}
        )
        # Test your endpoint
        pass


@pytest.mark.asyncio
async def test_fetch_external_api_timeout():
    """
    TODO: Test timeout handling
    - Mock httpx to raise TimeoutException
    - Assert 408 error returned
    """
    pass


@pytest.mark.asyncio
async def test_fetch_multiple_apis_parallel():
    """
    TODO: Test parallel fetching
    - Mock multiple API calls
    - Verify all called concurrently
    - Assert results aggregated correctly
    """
    pass
```

### 5. Implement Parametrized Tests

Use pytest parametrization for multiple test cases:

```python
@pytest.mark.parametrize("username,email,password,expected_status", [
    ("validuser", "valid@email.com", "password123", 201),
    ("ab", "valid@email.com", "password123", 422),  # Username too short
    ("validuser", "invalid-email", "password123", 422),  # Invalid email
    ("validuser", "valid@email.com", "short", 422),  # Password too short
])
def test_user_creation_validation(username, email, password, expected_status):
    """
    TODO: Test input validation
    - Try various invalid inputs
    - Assert appropriate error codes
    """
    response = client.post(
        "/api/users/",
        json={
            "username": username,
            "email": email,
            "password": password
        }
    )
    assert response.status_code == expected_status
```

### 6. Set Up GitHub Actions CI

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]

jobs:
  test:
    runs-on: ubuntu-latest

    services:
      redis:
        image: redis:alpine
        options: >-
          --health-cmd "redis-cli ping"
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 6379:6379

    steps:
    - uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'

    - name: Install Poetry
      run: |
        curl -sSL https://install.python-poetry.org | python3 -
        echo "$HOME/.local/bin" >> $GITHUB_PATH

    - name: Install dependencies
      run: |
        poetry install

    - name: Run tests
      run: |
        poetry run pytest --cov=app --cov-report=xml

    - name: Upload coverage
      uses: codecov/codecov-action@v3
      with:
        file: ./coverage.xml
```

### 7. Add Test Coverage Requirements

Create `pytest.ini`:

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_functions = test_*
addopts =
    --cov=app
    --cov-report=html
    --cov-report=term-missing
    --cov-fail-under=80
```

---

## 🧪 Testing Your Solution

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Open coverage report
open htmlcov/index.html

# Run specific test
poetry run pytest tests/test_users.py::test_create_user

# Run tests matching pattern
poetry run pytest -k "test_user"

# Show print statements
poetry run pytest -s

# Stop on first failure
poetry run pytest -x
```

---

## 📖 Key Concepts

### Basic Test Structure
```python
def test_something():
    # Arrange - set up test data
    user_data = {"username": "test"}

    # Act - perform the action
    result = create_user(user_data)

    # Assert - verify the result
    assert result is not None
    assert result.username == "test"
```

### Fixtures
```python
@pytest.fixture
def sample_user():
    """Reusable test data"""
    return User(username="test", email="test@example.com")

def test_with_fixture(sample_user):
    assert sample_user.username == "test"
```

### Mocking
```python
from unittest.mock import patch, MagicMock

def test_with_mock():
    with patch('app.utils.external_api') as mock_api:
        mock_api.return_value = {"data": "test"}
        result = my_function()
        assert result == {"data": "test"}
        mock_api.assert_called_once()
```

---

## 🎓 Resources

- [pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [unittest.mock Guide](https://docs.python.org/3/library/unittest.mock.html)
- [Test-Driven Development](https://testdriven.io/blog/modern-tdd/)

---

## 🎯 Testing Best Practices

1. **Write tests first** (TDD) - Define behavior before implementation
2. **Test one thing** - Each test should verify one specific behavior
3. **Use descriptive names** - `test_user_creation_fails_with_duplicate_email`
4. **Keep tests fast** - Mock external dependencies
5. **Test edge cases** - Empty inputs, null values, boundary conditions
6. **Maintain test isolation** - Tests shouldn't depend on each other
7. **Aim for high coverage** - Target 80%+ but focus on critical paths

---

## ✨ Completion Criteria

- [ ] Created comprehensive test suite
- [ ] Tests for all major endpoints (users, auth, analytics)
- [ ] Mocked external dependencies
- [ ] Parametrized tests for validation
- [ ] Code coverage > 80%
- [ ] Set up CI/CD with GitHub Actions
- [ ] All tests passing
- [ ] Coverage report generated

---

## 🐛 Common Issues

**Issue**: `fixture 'db' not found`
**Solution**: Define fixtures in `conftest.py` or import them properly.

**Issue**: Tests fail with database errors
**Solution**: Use separate test database or mock database operations.

**Issue**: Async tests not running
**Solution**: Install `pytest-asyncio` and mark tests with `@pytest.mark.asyncio`.

---

## ⏭️ Next Mission

Tests are solid! Progress to **Mission 9: The Forge** to learn packaging and distribution with Poetry.

*"Truth is forged in the fires of rigorous testing..."*
