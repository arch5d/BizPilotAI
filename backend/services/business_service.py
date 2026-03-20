"""
Business service functions for creating, retrieving, and deleting businesses.
"""
from typing import List
from bson import ObjectId

from database.db import get_database
from database.models import BusinessCreate, Business, BusinessUpdate


db = None


def get_db():
    global db
    if db is None:
        db = get_database()
    return db


async def create_business(business_data: BusinessCreate) -> Business:
    """Create a new business document in MongoDB."""
    database = get_db()
    result = await database["businesses"].insert_one(
        {**business_data.dict()}
    )
    created = await database["businesses"].find_one({"_id": result.inserted_id})
    return Business(**created)


async def list_businesses() -> List[Business]:
    """Return all businesses ordered by creation date desc."""
    database = get_db()
    cursor = database["businesses"].find().sort("created_at", -1)
    docs = await cursor.to_list(length=None)
    return [Business(**doc) for doc in docs]


async def get_business(business_id: str) -> Business:
    """Fetch a single business by id. Raises ValueError if not found."""
    if not ObjectId.is_valid(business_id):
        raise ValueError("Invalid business ID")
    database = get_db()
    doc = await database["businesses"].find_one({"_id": ObjectId(business_id)})
    if not doc:
        raise ValueError("Business not found")
    return Business(**doc)


async def delete_business(business_id: str) -> None:
    """Delete a business and its associated reports."""
    if not ObjectId.is_valid(business_id):
        raise ValueError("Invalid business ID")
    database = get_db()
    res = await database["businesses"].delete_one({"_id": ObjectId(business_id)})
    if res.deleted_count == 0:
        raise ValueError("Business not found")
    # also delete reports tied to business
    await database["reports"].delete_many({"business_id": ObjectId(business_id)})
