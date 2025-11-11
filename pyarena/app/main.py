"""
PyArena Main Application
This is the heart of the Guild Management System that evolves through 13 missions.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import users, auth, analytics, external

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="PyArena: Guild Management System",
    description="A gamified Python learning environment through progressive missions",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(auth.router, prefix="/api/auth", tags=["authentication"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
app.include_router(external.router, prefix="/api/external", tags=["external"])


@app.get("/")
async def root():
    """Root endpoint - Welcome to PyArena"""
    return {
        "message": "Welcome to PyArena: The Python Learning Arena",
        "version": "0.1.0",
        "docs": "/docs",
        "missions": 13,
        "status": "The Guild awaits your journey"
    }


@app.get("/ping")
async def ping():
    """Health check endpoint"""
    return {"message": "The Guild is alive", "status": "operational"}


@app.get("/missions")
async def list_missions():
    """List all available missions in PyArena"""
    missions = [
        {"id": 1, "name": "The First Flame", "focus": "FastAPI Basics"},
        {"id": 2, "name": "Records of Apprentices", "focus": "SQLAlchemy & CRUD"},
        {"id": 3, "name": "Seal of the Keeper", "focus": "JWT Authentication"},
        {"id": 4, "name": "External Scrolls", "focus": "API Integration"},
        {"id": 5, "name": "Parallel Prophecies", "focus": "Async Programming"},
        {"id": 6, "name": "The Guild Archives", "focus": "Data Analysis"},
        {"id": 7, "name": "Echo of Time", "focus": "Redis Caching"},
        {"id": 8, "name": "Circle of Truth", "focus": "Testing & CI"},
        {"id": 9, "name": "The Forge", "focus": "Packaging"},
        {"id": 10, "name": "Ascension", "focus": "Docker Deployment"},
        {"id": 11, "name": "The Whispering Stream", "focus": "WebSockets"},
        {"id": 12, "name": "The Mirror Gateway", "focus": "GraphQL"},
        {"id": 13, "name": "The Sky Forge", "focus": "Cloud Deployment"},
    ]
    return {"missions": missions, "total": len(missions)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
