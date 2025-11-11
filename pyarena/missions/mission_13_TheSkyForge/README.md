# ☁️ Mission 13: The Sky Forge

**Status**: Final
**Difficulty**: Advanced
**Focus**: Cloud Deployment & Production

---

## 🎯 Mission Objective

Ascend to the clouds! Deploy your Guild Management System to production, implement CI/CD, configure monitoring, and ensure your application can scale to serve thousands of guild members.

---

## 📚 What You'll Learn

- Cloud platform deployment (Render, Fly.io, Railway)
- Production configuration
- Environment management
- CI/CD pipelines
- Database migrations in production
- Monitoring and logging
- SSL/TLS certificates
- Scaling strategies

---

## ✅ Tasks

### 1. Prepare for Production

Create production checklist:

**Security**:
- [ ] Change SECRET_KEY
- [ ] Set strong database passwords
- [ ] Enable HTTPS only
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Disable debug mode
- [ ] Remove test/demo accounts

**Performance**:
- [ ] Enable caching
- [ ] Configure database connection pooling
- [ ] Set up CDN for static files
- [ ] Optimize database indexes
- [ ] Enable gzip compression

**Monitoring**:
- [ ] Set up error tracking (Sentry)
- [ ] Configure logging
- [ ] Set up uptime monitoring
- [ ] Add performance monitoring
- [ ] Configure alerts

### 2. Deploy to Render

Create `render.yaml`:

```yaml
services:
  # Web Service
  - type: web
    name: pyarena-web
    env: python
    region: oregon
    plan: free
    buildCommand: "pip install poetry && poetry install --no-dev"
    startCommand: "poetry run gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:$PORT"
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
      - key: DATABASE_URL
        fromDatabase:
          name: pyarena-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          name: pyarena-redis
          type: redis
          property: connectionString
      - key: SECRET_KEY
        generateValue: true
      - key: ENVIRONMENT
        value: production

  # PostgreSQL Database
databases:
  - name: pyarena-db
    databaseName: pyarena
    user: pyarena
    plan: free

  # Redis
  - name: pyarena-redis
    plan: free
```

Deploy:

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Deploy
render deploy
```

### 3. Deploy to Fly.io

Create `fly.toml`:

```toml
app = "pyarena"
primary_region = "sjc"

[build]
  builder = "paketobuildpacks/builder:base"
  buildpacks = ["gcr.io/paketo-buildpacks/python"]

[env]
  PORT = "8000"
  ENVIRONMENT = "production"

[http_service]
  internal_port = 8000
  force_https = true
  auto_stop_machines = true
  auto_start_machines = true
  min_machines_running = 0

  [http_service.concurrency]
    type = "connections"
    hard_limit = 25
    soft_limit = 20

[[services]]
  protocol = "tcp"
  internal_port = 8000

  [[services.ports]]
    port = 80
    handlers = ["http"]
    force_https = true

  [[services.ports]]
    port = 443
    handlers = ["tls", "http"]

  [services.concurrency]
    type = "connections"
    hard_limit = 25
    soft_limit = 20

  [[services.tcp_checks]]
    interval = "15s"
    timeout = "2s"
    grace_period = "5s"
    restart_limit = 0

[mounts]
  source = "data"
  destination = "/data"
```

Deploy:

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
fly auth login

# Launch app
fly launch

# Create PostgreSQL
fly postgres create --name pyarena-db

# Attach database
fly postgres attach --app pyarena pyarena-db

# Create Redis
fly redis create --name pyarena-redis

# Set secrets
fly secrets set SECRET_KEY=$(openssl rand -hex 32)

# Deploy
fly deploy

# Open app
fly open
```

### 4. Set Up CI/CD Pipeline

Enhance `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Production

on:
  push:
    branches: [ main ]
  release:
    types: [ published ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install

      - name: Run tests
        run: poetry run pytest

      - name: Check code quality
        run: |
          poetry run black --check app
          poetry run ruff check app

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
      - uses: actions/checkout@v3

      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
        run: |
          curl -X POST \
            https://api.render.com/deploy/srv-xxxxx \
            -H "Authorization: Bearer $RENDER_API_KEY"

      # Or deploy to Fly.io
      - name: Deploy to Fly.io
        uses: superfly/flyctl-actions/setup-flyctl@master
      - run: flyctl deploy --remote-only
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
```

### 5. Configure Production Database

Run migrations in production:

```bash
# For Render
render run alembic upgrade head

# For Fly.io
fly ssh console
>>> alembic upgrade head

# Create initial admin user
fly ssh console
>>> poetry run pyarena create-admin
```

### 6. Set Up Monitoring

Add Sentry for error tracking:

```bash
poetry add sentry-sdk
```

Update `app/main.py`:

```python
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[FastApiIntegration()],
    environment=os.getenv("ENVIRONMENT", "development"),
    traces_sample_rate=1.0,
)
```

Add logging:

```python
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        RotatingFileHandler('pyarena.log', maxBytes=10000000, backupCount=5),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### 7. Configure Production Environment

Create `.env.production`:

```bash
# Application
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<generate-with-openssl-rand-hex-32>

# Database
DATABASE_URL=postgresql://user:pass@host:5432/pyarena

# Redis
REDIS_HOST=your-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=<redis-password>

# CORS
ALLOWED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Monitoring
SENTRY_DSN=https://xxx@xxx.ingest.sentry.io/xxx

# External APIs
GITHUB_TOKEN=<optional>
WEATHER_API_KEY=<optional>
```

### 8. Performance Optimization

Add production server config:

```python
# Use Gunicorn with Uvicorn workers
CMD = [
    "gunicorn",
    "app.main:app",
    "--workers", "4",
    "--worker-class", "uvicorn.workers.UvicornWorker",
    "--bind", "0.0.0.0:8000",
    "--access-logfile", "-",
    "--error-logfile", "-",
    "--log-level", "info",
    "--timeout", "120",
    "--graceful-timeout", "30"
]
```

### 9. Set Up Domain and SSL

```bash
# For Fly.io
fly certs add yourdomain.com

# For Render
# Configure custom domain in dashboard
# SSL is automatic with Let's Encrypt
```

### 10. Create Health Checks and Monitoring

Add comprehensive health endpoint:

```python
@app.get("/health/detailed")
async def detailed_health(db: Session = Depends(get_db)):
    """
    Detailed health check for monitoring
    """
    health = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "checks": {}
    }

    # Database
    try:
        db.execute("SELECT 1")
        health["checks"]["database"] = {"status": "up"}
    except Exception as e:
        health["status"] = "unhealthy"
        health["checks"]["database"] = {"status": "down", "error": str(e)}

    # Redis
    try:
        from app.utils.cache_utils import get_redis_client
        client = get_redis_client()
        if client:
            client.ping()
            health["checks"]["redis"] = {"status": "up"}
    except Exception as e:
        health["checks"]["redis"] = {"status": "down", "error": str(e)}

    # Disk space
    import shutil
    total, used, free = shutil.disk_usage("/")
    health["checks"]["disk"] = {
        "total_gb": round(total / (2**30), 2),
        "used_gb": round(used / (2**30), 2),
        "free_gb": round(free / (2**30), 2),
        "percent_used": round((used / total) * 100, 2)
    }

    return health
```

---

## 🧪 Testing Your Deployment

```bash
# Test production endpoint
curl https://your-app.fly.dev/ping
curl https://your-app.fly.dev/health/detailed

# Load testing
hey -n 1000 -c 10 https://your-app.fly.dev/

# Check logs
fly logs

# Monitor metrics
fly dashboard
```

---

## 📖 Deployment Platforms Comparison

| Platform | Free Tier | Database | Auto-SSL | Price |
|----------|-----------|----------|----------|-------|
| **Render** | ✅ | PostgreSQL | ✅ | $0-$7/mo |
| **Fly.io** | ✅ | Postgres | ✅ | $0-$10/mo |
| **Railway** | ✅ | PostgreSQL | ✅ | $0-$5/mo |
| **Heroku** | ❌ | PostgreSQL | ✅ | $7+/mo |

---

## 🎓 Resources

- [Render Docs](https://render.com/docs)
- [Fly.io Docs](https://fly.io/docs/)
- [Railway Docs](https://docs.railway.app/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [The Twelve-Factor App](https://12factor.net/)

---

## ✨ Completion Criteria

- [ ] Deployed to cloud platform
- [ ] Database running in production
- [ ] Redis cache configured
- [ ] SSL/HTTPS enabled
- [ ] Custom domain (optional)
- [ ] CI/CD pipeline working
- [ ] Monitoring and logging configured
- [ ] Production environment variables set
- [ ] Health checks passing
- [ ] Load tested
- [ ] Backup strategy in place

---

## 🎉 Congratulations, Guildmaster!

You've completed all 13 missions of PyArena! You've built a production-ready FastAPI application from scratch, mastering:

✅ **Foundations**: FastAPI, SQLAlchemy, Pydantic
✅ **Security**: JWT Authentication, Authorization
✅ **Integration**: External APIs, Async Programming
✅ **Data**: pandas, Analytics, Caching
✅ **Quality**: Testing, CI/CD
✅ **Distribution**: Packaging, Docker
✅ **Advanced**: WebSockets, GraphQL
✅ **Production**: Cloud Deployment, Monitoring

**Your Next Steps**:
1. Build your own projects with these skills
2. Contribute to open source FastAPI projects
3. Explore advanced topics (microservices, Kubernetes)
4. Share your knowledge with others

*"The true master is one who never stops learning..."*

---

## 🏆 Final Challenge

Create a new mission! Fork PyArena and add:
- Mission 14: Your choice!
- New technology integration
- Advanced feature
- Share with the community

**The Guild is yours now. Lead it well.**
