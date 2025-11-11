"""
Database Configuration
Sets up SQLAlchemy engine and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL - defaults to SQLite for easy local development
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pyarena.db")

# For PostgreSQL in production, use:
# DATABASE_URL = "postgresql://user:password@localhost/pyarena"

# Create engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency function to get database session.
    Use this in route dependencies: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
