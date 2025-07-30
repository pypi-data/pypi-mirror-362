"""
Database connection management for OpenRXN Perovskite Optimizer.

Author: Nik Jois <nikjois@llamasearch.ai>
"""

import os
import logging
from typing import Optional, Any
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import StaticPool
import asyncio

# Set up logging
logger = logging.getLogger(__name__)

# Base class for all database models
Base = declarative_base()

class DatabaseManager:
    """Manages database connections and sessions"""
    
    def __init__(self, database_url: str = "sqlite:///:memory:"):
        """
        Initialize database manager
        
        Args:
            database_url: Database connection URL
        """
        self.database_url = database_url
        self.engine = None
        self.SessionLocal = None
        self._initialized = False
        
    def init_database(self):
        """Initialize database engine and session factory"""
        if self._initialized:
            return
            
        # Create engine with appropriate settings
        if self.database_url.startswith("sqlite"):
            self.engine = create_engine(
                self.database_url,
                connect_args={"check_same_thread": False},
                poolclass=StaticPool,
                echo=False  # Set to True for SQL debugging
            )
        else:
            self.engine = create_engine(
                self.database_url,
                echo=False
            )
        
        # Create session factory
        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )
        
        # Create all tables
        self._create_tables()
        
        self._initialized = True
        logger.info(f"Database initialized with URL: {self.database_url}")
    
    def _create_tables(self):
        """Create all database tables"""
        try:
            # Import models to register them with Base
            from .models import (
                Material, Experiment, OptimizationResult, 
                PropertyMeasurement, SynthesisProtocol
            )
            
            # Create all tables
            Base.metadata.create_all(bind=self.engine)
            logger.info("Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise
    
    def get_session(self) -> Session:
        """Get a new database session"""
        if not self._initialized:
            self.init_database()
            
        if self.SessionLocal is None:
            raise RuntimeError("Database not initialized")
            
        return self.SessionLocal()
    
    def close_session(self, session: Session):
        """Close a database session"""
        if session:
            session.close()
    
    def health_check(self) -> bool:
        """Check database health"""
        try:
            session = self.get_session()
            session.execute(text("SELECT 1"))
            session.close()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False
    
    def reset_database(self):
        """Reset database by dropping and recreating all tables"""
        if not self._initialized:
            self.init_database()
            
        try:
            # Drop all tables
            Base.metadata.drop_all(bind=self.engine)
            logger.info("Dropped all database tables")
            
            # Recreate tables
            self._create_tables()
            logger.info("Database reset completed")
            
        except Exception as e:
            logger.error(f"Error resetting database: {e}")
            raise
    
    def get_engine(self):
        """Get the database engine"""
        if not self._initialized:
            self.init_database()
        return self.engine
    
    def run_migrations(self):
        """Run database migrations using Alembic"""
        try:
            from alembic.config import Config
            from alembic import command
            
            # Get alembic configuration
            alembic_cfg = Config("alembic.ini")
            
            # Set the database URL
            alembic_cfg.set_main_option("sqlalchemy.url", self.database_url)
            
            # Run migrations
            command.upgrade(alembic_cfg, "head")
            logger.info("Database migrations completed successfully")
            
        except ImportError:
            logger.warning("Alembic not available. Running basic table creation instead.")
            self._create_tables()
        except Exception as e:
            logger.error(f"Error running migrations: {e}")
            # Fallback to basic table creation
            self._create_tables()
    
    def get_status(self) -> dict:
        """Get database status information"""
        try:
            status = {
                "initialized": self._initialized,
                "url": self.database_url,
                "health": self.health_check(),
                "tables": []
            }
            
            if self._initialized:
                # Get table information
                from sqlalchemy import inspect
                inspector = inspect(self.engine)
                status["tables"] = inspector.get_table_names()
                
                # Get connection pool info
                pool = self.engine.pool
                status["connection_pool"] = {
                    "size": pool.size(),
                    "checked_in": pool.checkedin(),
                    "checked_out": pool.checkedout(),
                    "overflow": pool.overflow(),
                    "invalid": pool.invalid()
                }
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting database status: {e}")
            return {
                "initialized": self._initialized,
                "url": self.database_url,
                "health": False,
                "error": str(e)
            }
    
    def close(self):
        """Close database connections"""
        if self.engine:
            self.engine.dispose()
            logger.info("Database connections closed")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


class AsyncDatabaseManager:
    """Async database manager for high-performance operations"""
    
    def __init__(self, database_url: str = "sqlite+aiosqlite:///:memory:"):
        self.database_url = database_url
        self.engine = None
        self.async_session = None
        self._initialized = False
    
    async def init_database(self):
        """Initialize async database"""
        if self._initialized:
            return
        
        try:
            from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
            
            self.engine = create_async_engine(
                self.database_url,
                echo=False
            )
            
            self.async_session = AsyncSession(self.engine)
            self._initialized = True
            
            logger.info(f"Async database initialized with URL: {self.database_url}")
            
        except ImportError:
            logger.warning("Async database features not available. Install asyncpg or aiosqlite.")
            raise
    
    async def get_session(self) -> Any:
        """Get async session"""
        if not self._initialized:
            await self.init_database()
        return self.async_session
    
    async def close(self):
        """Close async database connections"""
        if self.async_session:
            await self.async_session.close()
        if self.engine:
            await self.engine.dispose()


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None

def get_database_manager() -> DatabaseManager:
    """Get global database manager instance"""
    global _db_manager
    if _db_manager is None:
        db_url = os.getenv("DATABASE_URL", "sqlite:///:memory:")
        _db_manager = DatabaseManager(db_url)
    return _db_manager

def get_db_session() -> Session:
    """Get database session (convenience function)"""
    return get_database_manager().get_session()

def close_db_session(session: Session):
    """Close database session (convenience function)"""
    get_database_manager().close_session(session)

# Database session dependency for FastAPI
def get_db():
    """Database session dependency for FastAPI"""
    db = get_db_session()
    try:
        yield db
    finally:
        close_db_session(db)