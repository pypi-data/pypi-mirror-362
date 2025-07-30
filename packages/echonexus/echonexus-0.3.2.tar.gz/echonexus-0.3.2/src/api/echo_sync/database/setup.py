"""
Database setup script for Echo Sync Protocol.
"""
import logging
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

from .init_db import init_database
from .migrate import run_migrations

logger = logging.getLogger(__name__)

def setup_database() -> None:
    """Set up the database by running migrations and initializing data."""
    try:
        # Run migrations
        logger.info("Running database migrations...")
        run_migrations()
        
        # Initialize database
        logger.info("Initializing database...")
        init_database()
        
        logger.info("Database setup completed successfully")
        
    except Exception as e:
        logger.error(f"Error setting up database: {str(e)}")
        raise

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Set up database
    setup_database() 