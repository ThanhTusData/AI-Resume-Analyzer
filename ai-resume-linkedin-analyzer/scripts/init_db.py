import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, inspect
from loguru import logger

from app.config import get_config
from src.database.resume_repository import Base


def init_database():
    """Initialize database with all tables"""
    config = get_config()
    
    logger.info(f"Initializing database: {config.DATABASE_URL}")
    
    try:
        # Create engine
        engine = create_engine(config.DATABASE_URL, echo=config.DEBUG)
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        
        # Verify tables were created
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        logger.info(f"Database initialized successfully!")
        logger.info(f"Created tables: {', '.join(tables)}")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
        return False


if __name__ == "__main__":
    logger.add("logs/init_db.log", rotation="10 MB")
    
    logger.info("=" * 50)
    logger.info("Starting database initialization")
    logger.info("=" * 50)
    
    success = init_database()
    
    if success:
        logger.info("✅ Database initialization completed successfully!")
    else:
        logger.error("❌ Database initialization failed!")
        sys.exit(1)