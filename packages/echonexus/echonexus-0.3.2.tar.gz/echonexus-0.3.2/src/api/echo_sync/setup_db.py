"""
Script to set up the database for Echo Sync Protocol.
"""
import logging
import sys
from pathlib import Path

# Add the parent directory to sys.path
sys.path.append(str(Path(__file__).parent.parent))

from .database.setup import setup_database

logger = logging.getLogger(__name__)

def main() -> None:
    """Main function to set up the database."""
    try:
        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # Set up database
        setup_database()
        
    except Exception as e:
        logger.error(f"Error setting up database: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 