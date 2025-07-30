"""
Database session management for Echo Sync Protocol.
"""
from contextlib import contextmanager
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

from ..config import settings

# Create SQLAlchemy engine
engine = create_engine(
    settings.database.connection_string,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    echo=settings.database.echo,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()

@contextmanager
def get_db() -> Generator[Session, None, None]:
    """
    Context manager for database sessions.
    
    Usage:
        with get_db() as db:
            # Use db session
            pass
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db() -> None:
    """Initialize the database by creating all tables."""
    Base.metadata.create_all(bind=engine)

def get_db_session() -> Session:
    """
    Get a database session.
    
    Note: This should be used with FastAPI's dependency injection system.
    The session will be automatically closed after the request is complete.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 