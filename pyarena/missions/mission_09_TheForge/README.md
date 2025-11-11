# ⚙️ Mission 9: The Forge

**Status**: Advanced
**Difficulty**: Intermediate
**Focus**: Packaging & Distribution with Poetry

---

## 🎯 Mission Objective

Forge your creation into a distributable artifact! Learn to package Python applications with Poetry, manage dependencies, version your releases, and prepare for distribution.

---

## 📚 What You'll Learn

- Poetry project management
- Dependency management and lock files
- Semantic versioning
- Package metadata
- Building distributions
- Publishing to PyPI (optional)
- Entry points and CLI tools

---

## ✅ Tasks

### 1. Understand Your Poetry Configuration

Examine `pyproject.toml`:
- Project metadata
- Dependencies and dev dependencies
- Build system configuration
- Tool configurations (pytest, black, ruff)

### 2. Manage Dependencies

Practice dependency management:

```bash
# Add a new dependency
poetry add requests

# Add a dev dependency
poetry add --group dev black

# Update dependencies
poetry update

# Show dependency tree
poetry show --tree

# Export requirements.txt (for compatibility)
poetry export -f requirements.txt --output requirements.txt
```

### 3. Version Your Application

Update version in `pyproject.toml`:

```toml
[tool.poetry]
name = "pyarena"
version = "1.0.0"  # Update this
```

Or use Poetry commands:

```bash
# Bump patch version (0.1.0 -> 0.1.1)
poetry version patch

# Bump minor version (0.1.1 -> 0.2.0)
poetry version minor

# Bump major version (0.2.0 -> 1.0.0)
poetry version major

# Set specific version
poetry version 1.0.0
```

### 4. Add CLI Entry Points

Create a CLI tool for PyArena management:

Create `app/cli.py`:

```python
"""
PyArena CLI Tool
TODO: Create command-line interface for managing PyArena
"""

import typer
from app.database import SessionLocal, engine
from app.models import User, Base
from app.utils.auth_utils import get_password_hash

app = typer.Typer()


@app.command()
def init_db():
    """Initialize the database"""
    typer.echo("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    typer.echo("✓ Database initialized!")


@app.command()
def create_admin(
    username: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(..., prompt=True, hide_input=True)
):
    """
    TODO: Create an admin user via CLI
    - Prompt for username, email, password
    - Hash password
    - Create user with admin privileges
    - Save to database
    """
    db = SessionLocal()
    try:
        admin = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password),
            is_admin=True,
            guild_rank="Master"
        )
        db.add(admin)
        db.commit()
        typer.echo(f"✓ Admin user '{username}' created successfully!")
    except Exception as e:
        typer.echo(f"✗ Error: {e}", err=True)
    finally:
        db.close()


@app.command()
def list_users():
    """
    TODO: List all users
    - Query database
    - Display in table format
    - Show username, email, rank, missions completed
    """
    pass


@app.command()
def stats():
    """
    TODO: Show guild statistics
    - Total users
    - Total missions completed
    - Average experience
    - Top users
    """
    pass


if __name__ == "__main__":
    app()
```

Add entry point to `pyproject.toml`:

```toml
[tool.poetry.scripts]
pyarena = "app.cli:app"
```

Test CLI:

```bash
# After adding entry point, reinstall
poetry install

# Use CLI
poetry run pyarena init-db
poetry run pyarena create-admin
poetry run pyarena stats
```

### 5. Build Distribution Packages

Build your package:

```bash
# Build both wheel and sdist
poetry build

# Output:
# - dist/pyarena-0.1.0-py3-none-any.whl
# - dist/pyarena-0.1.0.tar.gz

# Inspect built package
tar -tzf dist/pyarena-0.1.0.tar.gz

# Install your package locally
pip install dist/pyarena-0.1.0-py3-none-any.whl
```

### 6. Create Package Documentation

Add detailed package information to `pyproject.toml`:

```toml
[tool.poetry]
name = "pyarena"
version = "1.0.0"
description = "A gamified Python learning environment through progressive missions"
authors = ["Your Name <you@example.com>"]
license = "MIT"
readme = "README.md"
homepage = "https://github.com/yourusername/pyarena"
repository = "https://github.com/yourusername/pyarena"
documentation = "https://pyarena.readthedocs.io"
keywords = ["learning", "fastapi", "python", "education", "gamification"]
classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Framework :: FastAPI",
    "Topic :: Education",
]

[tool.poetry.urls]
"Bug Tracker" = "https://github.com/yourusername/pyarena/issues"
```

### 7. (Optional) Publish to Test PyPI

```bash
# Configure test PyPI
poetry config repositories.testpypi https://test.pypi.org/legacy/

# Get API token from https://test.pypi.org/manage/account/token/
poetry config pypi-token.testpypi your-api-token

# Build and publish
poetry build
poetry publish -r testpypi

# Test installation
pip install --index-url https://test.pypi.org/simple/ pyarena
```

### 8. Create Installation Script

Create `scripts/install.sh`:

```bash
#!/bin/bash
# PyArena Installation Script

echo "🔥 Installing PyArena..."

# Check Python version
python_version=$(python3 --version 2>&1 | grep -Po '(?<=Python )(.+)')
required_version="3.9"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then
    echo "❌ Python 3.9+ required. You have $python_version"
    exit 1
fi

# Install Poetry if not present
if ! command -v poetry &> /dev/null; then
    echo "📦 Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
fi

# Install dependencies
echo "📥 Installing dependencies..."
poetry install

# Initialize database
echo "🗄️  Initializing database..."
poetry run pyarena init-db

# Create .env file if not exists
if [ ! -f .env ]; then
    echo "⚙️  Creating .env file..."
    cat > .env << EOF
DATABASE_URL=sqlite:///./pyarena.db
SECRET_KEY=$(openssl rand -hex 32)
REDIS_HOST=localhost
REDIS_PORT=6379
EOF
fi

echo "✅ Installation complete!"
echo "🚀 Start the server with: poetry run uvicorn app.main:app --reload"
```

---

## 🧪 Testing Your Solution

```bash
# Verify package builds
poetry build

# Check package contents
tar -tzf dist/pyarena-*.tar.gz | head -20

# Install in editable mode
pip install -e .

# Test CLI
pyarena --help
pyarena init-db
pyarena stats

# Uninstall
pip uninstall pyarena
```

---

## 📖 Key Concepts

### Semantic Versioning
```
MAJOR.MINOR.PATCH
1.0.0

MAJOR: Breaking changes
MINOR: New features (backward compatible)
PATCH: Bug fixes
```

### Poetry Lock File
- `poetry.lock` - Exact versions of all dependencies
- Commit to git for reproducible builds
- Update with `poetry update`

### Entry Points
```toml
[tool.poetry.scripts]
my-command = "module.file:function"
```

---

## 🎓 Resources

- [Poetry Documentation](https://python-poetry.org/docs/)
- [Semantic Versioning](https://semver.org/)
- [Python Packaging Guide](https://packaging.python.org/)
- [PyPI Publishing Tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/)

---

## ✨ Completion Criteria

- [ ] Updated project metadata in pyproject.toml
- [ ] Managed dependencies with Poetry
- [ ] Implemented semantic versioning
- [ ] Created CLI tool with entry points
- [ ] Built distribution packages (wheel + sdist)
- [ ] Created installation script
- [ ] (Optional) Published to Test PyPI
- [ ] Package successfully installs and runs

---

## 🐛 Common Issues

**Issue**: `poetry: command not found`
**Solution**: Add Poetry to PATH or use full path `~/.local/bin/poetry`

**Issue**: Dependency conflicts
**Solution**: Use `poetry update` or specify compatible versions

**Issue**: Entry points not working
**Solution**: Reinstall after adding entry points: `poetry install`

---

## ⏭️ Next Mission

Package forged! Advance to **Mission 10: Ascension** to containerize your application with Docker.

*"True craftsmanship means your creation can be shared with the world..."*
