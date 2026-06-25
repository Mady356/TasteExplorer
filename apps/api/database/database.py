"""Database connection and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
import os
from typing import Generator

from .models import Base

# Database URL from environment
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://tasteexplorer:tasteexplorer@localhost:5432/tasteexplorer"
)

# Create engine
engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool,  # Use NullPool for development
    echo=os.getenv("SQL_ECHO", "false").lower() == "true",
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db() -> Generator:
    """
    Database session dependency for FastAPI.

    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            return db.query(User).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database (create all tables)."""
    Base.metadata.create_all(bind=engine)


def drop_db():
    """Drop all database tables (use with caution!)."""
    Base.metadata.drop_all(bind=engine)
