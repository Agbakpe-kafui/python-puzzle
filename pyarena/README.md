# 🧠 PyArena: The Python Learning Arena

Welcome to **PyArena**, a gamified, hands-on Python learning environment inspired by HackTheBox — but for developers who want to master **Python libraries, frameworks, and APIs** by *building* and *breaking* real things.

Every level (called a **Mission**) expands one single evolving application — your own codebase — while teaching you the tools and principles used by professional Python developers.

By the end, you'll have a **production-ready FastAPI app** and a deep understanding of Python's ecosystem.

---

## 🎯 What You'll Build

You will create the **API Guild Management System**, a single FastAPI application that grows with every mission:

- REST APIs
- Databases & ORMs
- Authentication
- Async & concurrency
- Data analytics
- Caching
- Testing
- Packaging & Deployment

All in one unified project called **PyArena**.

---

## 🧱 Tech Stack

| Category | Tool |
|-----------|------|
| Web Framework | **FastAPI** |
| ORM & DB | **SQLAlchemy** + **SQLite / Postgres** |
| HTTP Clients | **httpx**, **aiohttp** |
| Auth | **JWT / OAuth2** |
| Data Tools | **pandas**, **numpy** |
| Caching | **Redis** |
| Testing | **pytest** |
| Dependency Mgmt | **Poetry** |
| Deployment | **Docker**, **Docker Compose** |

---

## ⚙️ Setup Guide

### 1️⃣ Clone the project

```bash
git clone https://github.com/Agbakpe-kafui/python-puzzle.git
cd pyarena
```

### 2️⃣ Install dependencies

Using Poetry (recommended):

```bash
# Install Poetry if you haven't
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

Or using pip:

```bash
pip install -r requirements.txt
```

### 3️⃣ Set up environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your settings
# For development, defaults should work fine
```

### 4️⃣ Run the server

```bash
# With Poetry
poetry run uvicorn app.main:app --reload

# Or with Python directly
python -m uvicorn app.main:app --reload
```

Visit [http://localhost:8000](http://localhost:8000)

**Test it works:**
```bash
curl http://localhost:8000/ping
# Should return: {"message":"The Guild is alive","status":"operational"}
```

### 5️⃣ Explore the API

- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Missions List**: http://localhost:8000/missions

### 6️⃣ Run with Docker (Optional)

```bash
docker-compose up --build
```

Includes PostgreSQL, Redis, and web UI tools!

---

## 🧭 Learning Roadmap — The 13 Missions of PyArena

### 🕯️ Mission 1 — The First Flame

Set up your FastAPI app.

> **Skills**: FastAPI basics, app structure, JSON responses.
>
> **Location**: `missions/mission_01_FirstFlame/`

### 📜 Mission 2 — Records of Apprentices

Build your first SQLAlchemy models and CRUD endpoints.

> **Skills**: ORM, Pydantic models, migrations.
>
> **Location**: `missions/mission_02_RecordsOfApprentices/`

### 🔐 Mission 3 — Seal of the Keeper

Add JWT-based authentication.

> **Skills**: OAuth2, JWT, secure routes.
>
> **Location**: `missions/mission_03_SealOfTheKeeper/`

### 🌐 Mission 4 — External Scrolls

Consume external APIs with httpx.

> **Skills**: API calls, env vars, response parsing.
>
> **Location**: `missions/mission_04_ExternalScrolls/`

### ⚡ Mission 5 — Parallel Prophecies

Add async calls with asyncio.

> **Skills**: async/await, performance tuning.
>
> **Location**: `missions/mission_05_ParallelProphecies/`

### 📊 Mission 6 — The Guild Archives

Analyze data using pandas & numpy.

> **Skills**: dataframes, analytics endpoints.
>
> **Location**: `missions/mission_06_TheGuildArchives/`

### 🌀 Mission 7 — Echo of Time

Implement Redis caching.

> **Skills**: cache optimization, background tasks.
>
> **Location**: `missions/mission_07_EchoOfTime/`

### 🧪 Mission 8 — Circle of Truth

Add automated testing and CI.

> **Skills**: pytest, GitHub Actions.
>
> **Location**: `missions/mission_08_CircleOfTruth/`

### ⚙️ Mission 9 — The Forge

Package your app with Poetry.

> **Skills**: versioning, metadata.
>
> **Location**: `missions/mission_09_TheForge/`

### 🚀 Mission 10 — Ascension

Dockerize your full app.

> **Skills**: Docker, Compose, deployment setup.
>
> **Location**: `missions/mission_10_Ascension/`

### 🌊 Mission 11 — The Whispering Stream

Add WebSockets for real-time updates.

> **Skills**: WebSocket endpoints, async streams.
>
> **Location**: `missions/mission_11_TheWhisperingStream/`

### 🪞 Mission 12 — The Mirror Gateway

Add GraphQL API layer.

> **Skills**: Strawberry / Graphene, schema design.
>
> **Location**: `missions/mission_12_TheMirrorGateway/`

### ☁️ Mission 13 — The Sky Forge

Deploy your app to cloud platforms.

> **Skills**: CI/CD, environment secrets, Render or Fly.io.
>
> **Location**: `missions/mission_13_TheSkyForge/`

---

## 📚 How to Learn Inside PyArena

1. **Start at Mission 1** and read each mission's README
2. **Complete each TODO** in the code
3. **Run `pytest`** to confirm success
4. **Explore mission solutions** afterward
5. **Take notes** on what you learn per mission

---

## 🧪 Running Tests

```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test file
poetry run pytest tests/test_users.py

# Run tests in verbose mode
poetry run pytest -v
```

---

## 🚀 Quick Start Commands

```bash
# Development
poetry run uvicorn app.main:app --reload

# Testing
poetry run pytest

# Docker
docker-compose up

# Format code
poetry run black app/

# Lint
poetry run ruff check app/

# Type checking
poetry run mypy app/
```

---

## 📖 Project Structure

```
pyarena/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── routers/             # API route handlers
│   │   ├── users.py
│   │   ├── auth.py
│   │   ├── analytics.py
│   │   └── external.py
│   └── utils/               # Utility functions
│       ├── auth_utils.py
│       └── cache_utils.py
├── missions/                # 13 learning missions
│   ├── mission_01_FirstFlame/
│   ├── mission_02_RecordsOfApprentices/
│   └── ...
├── tests/                   # Test suite
│   ├── conftest.py
│   ├── test_main.py
│   ├── test_users.py
│   ├── test_auth.py
│   └── test_analytics.py
├── pyproject.toml          # Poetry configuration
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Multi-container setup
└── README.md               # This file
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Add new missions** - Create Mission 14+
2. **Improve existing missions** - Better explanations, examples
3. **Fix bugs** - Submit issues or pull requests
4. **Share your solutions** - Help others learn
5. **Improve documentation** - Clarify instructions

### How to Contribute

```bash
# Fork the repository
git clone https://github.com/yourusername/pyarena.git
cd pyarena

# Create a new branch
git checkout -b feature/your-feature-name

# Make your changes and commit
git add .
git commit -m "Add: your feature description"

# Push and create a Pull Request
git push origin feature/your-feature-name
```

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🌟 Acknowledgments

- Inspired by **HackTheBox** and gamified learning platforms
- Built with **FastAPI** by Sebastián Ramírez
- Uses amazing Python libraries: SQLAlchemy, Pydantic, pytest, and more
- Community contributions and feedback

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/pyarena/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/pyarena/discussions)
- **Documentation**: Check individual mission READMEs in `missions/` folder

---

## 🏁 Final Words

> *"The true Guildmaster is forged not by reading docs — but by building."*

Welcome to **PyArena**. Your journey begins now.

**Ready to start?** Head to [`missions/mission_01_FirstFlame/README.md`](missions/mission_01_FirstFlame/README.md)

---

## 📊 Project Status

- ✅ **13 Complete Missions**
- ✅ **Production-Ready Code**
- ✅ **Comprehensive Tests**
- ✅ **Docker Support**
- ✅ **Full Documentation**

**Current Version**: 0.1.0

**Compatibility**: Python 3.9+

---

**Happy Learning! May your code be bug-free and your APIs blazing fast.** ⚡
