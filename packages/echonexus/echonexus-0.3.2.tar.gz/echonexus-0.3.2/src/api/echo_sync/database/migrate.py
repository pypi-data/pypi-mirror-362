"""
Database migration script for Echo Sync Protocol.
"""
import logging
import os
import sys
from pathlib import Path

from alembic import command
from alembic.config import Config

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent.parent))

logger = logging.getLogger(__name__)

def run_migrations() -> None:
    """Run database migrations."""
    try:
        # Get the path to the migrations directory
        migrations_dir = Path(__file__).parent / "migrations"
        
        # Create Alembic configuration
        alembic_cfg = Config()
        alembic_cfg.set_main_option("script_location", str(migrations_dir))
        
        # Run the migration
        command.upgrade(alembic_cfg, "head")
        logger.info("Database migrations completed successfully")
        
    except Exception as e:
        logger.error(f"Error running migrations: {str(e)}")
        raise

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Run migrations
    run_migrations() 