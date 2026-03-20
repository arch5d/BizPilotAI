"""
BizPilotAI - Database connection and session management.
Async MongoDB connection using Motor driver.
"""
from motor.motor_asyncio import AsyncClient, AsyncDatabase
from contextlib import asynccontextmanager

from config import MONGODB_URL, MONGODB_DB_NAME

# Global MongoDB client and database instances
_client: AsyncClient = None
_database: AsyncDatabase = None


async def connect_to_mongo():
    """Initialize MongoDB connection."""
    global _client, _database
    _client = AsyncClient(MONGODB_URL)
    _database = _client[MONGODB_DB_NAME]
    
    # Create indexes for better performance
    await create_indexes()
    
    print(f"Connected to MongoDB: {MONGODB_DB_NAME}")


async def disconnect_from_mongo():
    """Close MongoDB connection."""
    global _client
    if _client:
        _client.close()
        print("Disconnected from MongoDB")


async def create_indexes():
    """Create database indexes for performance."""
    # Create index for business_id in reports collection
    await _database["reports"].create_index("business_id")
    
    # Create index for created_at in reports collection
    await _database["reports"].create_index("created_at")
    
    # Create index for created_at in businesses collection
    await _database["businesses"].create_index("created_at")


def get_database() -> AsyncDatabase:
    """Get the current database instance."""
    if _database is None:
        raise RuntimeError("Database not connected. Call connect_to_mongo() first.")
    return _database


@asynccontextmanager
async def get_db_context():
    """Context manager for database operations."""
    try:
        yield get_database()
    except Exception as e:
        print(f"Database error: {e}")
        raise
