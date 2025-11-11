# 🔐 Mission 3: Seal of the Keeper

**Status**: Core
**Difficulty**: Intermediate
**Focus**: JWT Authentication & Authorization

---

## 🎯 Mission Objective

Protect the Guild's secrets! Implement JWT (JSON Web Token) based authentication to secure your API endpoints and control access based on user roles.

---

## 📚 What You'll Learn

- JWT token generation and validation
- Password hashing with bcrypt
- OAuth2 with Password flow
- Protected routes with dependencies
- Role-based access control (RBAC)
- Security best practices

---

## ✅ Tasks

### 1. Understand the Authentication Flow

Examine `app/utils/auth_utils.py`:
- Password hashing functions
- JWT token creation
- Token validation
- User authentication

### 2. Test Authentication Endpoints

```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "keeper", "email": "keeper@guild.com", "password": "secret123", "full_name": "The Keeper"}'

# Login to get token
curl -X POST http://localhost:8000/api/auth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=keeper&password=secret123"

# Use the token
TOKEN="<your-token-here>"
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/users/me
```

### 3. Implement Token Refresh

Add token refresh functionality to `app/routers/auth.py`:

```python
@router.post("/refresh", response_model=Token)
async def refresh_access_token(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    TODO: Implement token refresh
    - Verify current token is valid
    - Generate new access token
    - Optional: Implement refresh token rotation
    - Return new token
    """
    # Your code here
    pass
```

### 4. Add Admin-Only Endpoints

Create protected admin endpoints:

```python
from app.utils.auth_utils import get_current_admin_user

@router.delete("/admin/users/{user_id}")
async def admin_delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """
    TODO: Admin-only user deletion
    - Verify admin privileges (already done by dependency)
    - Prevent deleting self
    - Soft delete instead of hard delete
    - Log the action
    """
    # Your code here
    pass
```

### 5. Implement Password Reset

Add password reset functionality:

```python
@router.post("/password/reset-request")
async def request_password_reset(email: str, db: Session = Depends(get_db)):
    """
    TODO: Request password reset
    - Verify email exists
    - Generate reset token (short-lived)
    - In production: Send email with reset link
    - For now: Return the token for testing
    """
    # Your code here
    pass


@router.post("/password/reset-confirm")
async def confirm_password_reset(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """
    TODO: Complete password reset
    - Validate reset token
    - Verify token hasn't expired
    - Update user password
    - Invalidate the reset token
    """
    # Your code here
    pass
```

---

## 🧪 Testing Your Solution

```bash
# Create admin user (for testing)
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "email": "admin@pyarena.dev", "password": "admin123", "full_name": "Admin User"}'

# Test protected endpoint without token (should fail)
curl http://localhost:8000/api/users/me

# Test with valid token (should succeed)
curl -H "Authorization: Bearer $TOKEN" http://localhost:8000/api/users/me

# Test token refresh
curl -X POST http://localhost:8000/api/auth/refresh \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📖 Key Concepts

### Password Hashing
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash password
hashed = pwd_context.hash("mypassword")

# Verify password
is_valid = pwd_context.verify("mypassword", hashed)
```

### JWT Creation
```python
from jose import jwt
from datetime import datetime, timedelta

payload = {"sub": username, "exp": datetime.utcnow() + timedelta(minutes=30)}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

### Protected Routes
```python
from fastapi import Depends
from app.utils.auth_utils import get_current_user

@router.get("/protected")
async def protected_route(current_user: User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}"}
```

---

## 🎓 Resources

- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [OAuth2 with Password and Bearer](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [JWT.io - Introduction](https://jwt.io/introduction)
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

---

## 🔒 Security Best Practices

1. **Never store passwords in plain text** - Always hash with bcrypt
2. **Use environment variables** for SECRET_KEY
3. **Set appropriate token expiration** - Balance security vs UX
4. **Implement rate limiting** - Prevent brute force attacks
5. **Use HTTPS in production** - Protect tokens in transit
6. **Validate all inputs** - Prevent injection attacks
7. **Implement token blacklisting** - Allow logout to work properly

---

## ✨ Completion Criteria

- [ ] Successfully registered and logged in users
- [ ] JWT tokens generated and validated
- [ ] Protected endpoints require valid tokens
- [ ] Admin-only endpoints enforce role checks
- [ ] Token refresh mechanism implemented
- [ ] Password reset flow working
- [ ] Tested authentication with different user roles

---

## 🐛 Common Issues

**Issue**: `Could not validate credentials`
**Solution**: Check that the token is correctly formatted and not expired.

**Issue**: `401 Unauthorized` on protected routes
**Solution**: Ensure you're sending the token in the `Authorization: Bearer <token>` header.

---

## ⏭️ Next Mission

Seal acquired! Proceed to **Mission 4: External Scrolls** to learn how to integrate with external APIs using httpx.

*"Only those who bear the Seal may enter the inner chambers..."*
