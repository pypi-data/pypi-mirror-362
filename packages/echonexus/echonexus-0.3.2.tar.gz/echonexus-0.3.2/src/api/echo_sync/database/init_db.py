"""
Database initialization script for Echo Sync Protocol.
"""
import logging
from typing import Optional

from sqlalchemy.orm import Session

from .session import init_db, get_db
from .models import EchoNode
from .repositories import EchoNodeRepository

logger = logging.getLogger(__name__)

def init_database() -> None:
    """Initialize the database with required tables and initial data."""
    try:
        # Create all tables
        init_db()
        logger.info("Database tables created successfully")
        
        # Create initial data if needed
        with get_db() as db:
            create_initial_data(db)
            
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
        raise

def create_initial_data(db: Session) -> None:
    """Create initial data in the database."""
    try:
        # Create repository
        node_repo = EchoNodeRepository(db)
        
        # Create default node if it doesn't exist
        default_node = node_repo.get_node("default")
        if not default_node:
            node_repo.create_node(
                node_id="default",
                version="1.0.0",
                metadata={
                    "name": "Default Node",
                    "description": "Default EchoNode for system operations",
                    "type": "system"
                }
            )
            logger.info("Default node created successfully")
            
    except Exception as e:
        logger.error(f"Error creating initial data: {str(e)}")
        raise

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Initialize database
    init_database() 