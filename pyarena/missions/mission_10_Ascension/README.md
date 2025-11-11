# 🚀 Mission 10: Ascension

**Status**: Advanced
**Difficulty**: Intermediate-Advanced
**Focus**: Docker & Containerization

---

## 🎯 Mission Objective

Ascend to the clouds! Package your entire application stack into Docker containers for consistent deployment across any environment. Master Docker, Docker Compose, and container orchestration basics.

---

## 📚 What You'll Learn

- Docker fundamentals
- Writing Dockerfiles
- Multi-stage builds
- Docker Compose
- Container networking
- Volume management
- Environment configuration
- Production best practices

---

## ✅ Tasks

### 1. Understand the Dockerfile

Examine `Dockerfile` in the project root:

```dockerfile
# Multi-stage build for smaller final image

FROM python:3.11-slim as builder

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Install dependencies (no dev dependencies)
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Copy installed dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

# Create non-root user
RUN useradd -m -u 1000 pyarena && chown -R pyarena:pyarena /app
USER pyarena

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD python -c "import requests; requests.get('http://localhost:8000/ping')"

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Create Docker Compose Configuration

Examine `docker-compose.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: pyarena_web
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://pyarena:password@db:5432/pyarena
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - SECRET_KEY=${SECRET_KEY:-change-me-in-production}
    depends_on:
      db:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./app:/app/app  # For development
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  db:
    image: postgres:15-alpine
    container_name: pyarena_db
    environment:
      - POSTGRES_USER=pyarena
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=pyarena
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U pyarena"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    container_name: pyarena_redis
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 5

  # Optional: Redis Commander (GUI for Redis)
  redis-commander:
    image: rediscommander/redis-commander:latest
    container_name: pyarena_redis_ui
    environment:
      - REDIS_HOSTS=local:redis:6379
    ports:
      - "8081:8081"
    depends_on:
      - redis

volumes:
  postgres_data:
  redis_data:
```

### 3. Build and Run with Docker

```bash
# Build the image
docker build -t pyarena:latest .

# Run container
docker run -p 8000:8000 pyarena:latest

# Or use Docker Compose (recommended)
docker-compose up -d

# View logs
docker-compose logs -f web

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

### 4. Create Production Dockerfile

Create `Dockerfile.prod`:

```dockerfile
FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

FROM python:3.11-slim

WORKDIR /app

# Install only runtime dependencies
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application
COPY app ./app

# Security: non-root user
RUN useradd -m -u 1000 pyarena && chown -R pyarena:pyarena /app
USER pyarena

EXPOSE 8000

# Production server (gunicorn with uvicorn workers)
CMD ["gunicorn", "app.main:app", \
     "--workers", "4", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--access-logfile", "-", \
     "--error-logfile", "-"]
```

### 5. Add Environment Configuration

Create `.env.example`:

```bash
# Database
DATABASE_URL=postgresql://pyarena:password@db:5432/pyarena

# Redis
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=

# Security
SECRET_KEY=your-super-secret-key-change-this
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Application
DEBUG=False
ALLOWED_HOSTS=*

# External APIs (optional)
GITHUB_TOKEN=
WEATHER_API_KEY=
```

### 6. Create Makefile for Common Commands

Create `Makefile`:

```makefile
.PHONY: build up down logs test shell db-migrate

build:
	docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

test:
	docker-compose exec web pytest

shell:
	docker-compose exec web /bin/bash

db-migrate:
	docker-compose exec web alembic upgrade head

db-shell:
	docker-compose exec db psql -U pyarena -d pyarena

redis-cli:
	docker-compose exec redis redis-cli

clean:
	docker-compose down -v
	docker system prune -f
```

Usage:

```bash
make build  # Build images
make up     # Start services
make logs   # View logs
make test   # Run tests
make down   # Stop services
```

### 7. Optimize Docker Image Size

Implement optimization techniques:

```dockerfile
# Use alpine for smaller size
FROM python:3.11-alpine

# Multi-stage build
FROM python:3.11-slim as builder
# ... build stage ...
FROM python:3.11-slim
# ... only copy what's needed ...

# Minimize layers
RUN apt-get update && apt-get install -y \
    package1 \
    package2 \
    && rm -rf /var/lib/apt/lists/*

# .dockerignore file
TODO: Create .dockerignore:
__pycache__
*.pyc
*.pyo
*.pyd
.Python
.git
.pytest_cache
.coverage
htmlcov/
dist/
build/
*.egg-info/
.env
.venv
```

### 8. Add Docker Health Checks

Implement comprehensive health checking:

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import httpx; httpx.get('http://localhost:8000/ping').raise_for_status()"
```

And add health endpoint in `app/main.py`:

```python
@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    TODO: Comprehensive health check
    - Check database connection
    - Check Redis connection
    - Check disk space
    - Return detailed status
    """
    health_status = {
        "status": "healthy",
        "checks": {
            "database": "unknown",
            "redis": "unknown",
            "disk": "unknown"
        }
    }

    # Check database
    try:
        db.execute("SELECT 1")
        health_status["checks"]["database"] = "healthy"
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = f"unhealthy: {str(e)}"

    # Check Redis
    try:
        from app.utils.cache_utils import get_redis_client
        client = get_redis_client()
        if client:
            client.ping()
            health_status["checks"]["redis"] = "healthy"
        else:
            health_status["checks"]["redis"] = "unavailable"
    except Exception as e:
        health_status["checks"]["redis"] = f"unhealthy: {str(e)}"

    return health_status
```

---

## 🧪 Testing Your Solution

```bash
# Build and start
docker-compose up --build

# Check services are running
docker-compose ps

# Test the API
curl http://localhost:8000/ping
curl http://localhost:8000/health

# Check logs
docker-compose logs web

# Inspect containers
docker inspect pyarena_web

# Check resource usage
docker stats

# Clean up
docker-compose down -v
```

---

## 📖 Key Concepts

### Dockerfile Instructions
```dockerfile
FROM python:3.11          # Base image
WORKDIR /app             # Set working directory
COPY . .                 # Copy files
RUN pip install poetry   # Execute command
EXPOSE 8000              # Document port
CMD ["python", "app.py"] # Default command
```

### Docker Compose
```yaml
services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
```

---

## 🎓 Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [FastAPI in Containers](https://fastapi.tiangolo.com/deployment/docker/)

---

## ✨ Completion Criteria

- [ ] Created optimized Dockerfile
- [ ] Set up Docker Compose with all services
- [ ] Containerized web app, database, and Redis
- [ ] Implemented health checks
- [ ] Created production Dockerfile
- [ ] Added .dockerignore
- [ ] Created Makefile for convenience
- [ ] Successfully deployed stack locally

---

## 🐛 Common Issues

**Issue**: `Cannot connect to Docker daemon`
**Solution**: Ensure Docker is running

**Issue**: Port already in use
**Solution**: Change port mapping or stop conflicting service

**Issue**: Database connection refused
**Solution**: Ensure services are healthy: `docker-compose ps`

---

## ⏭️ Next Mission

Containerized! Advance to **Mission 11: The Whispering Stream** to add real-time features with WebSockets.

*"Ascension is achieved when your creation can run anywhere..."*
