"""
Business-related endpoints.
"""
from typing import List
from fastapi import APIRouter, HTTPException, status

from services.business_service import (
    create_business,
    list_businesses,
    get_business,
    delete_business,
)
from database.models import BusinessCreate, Business


router = APIRouter(prefix="/business", tags=["business"])


@router.post("", response_model=Business, status_code=status.HTTP_201_CREATED)
async def create_business_endpoint(business: BusinessCreate):
    try:
        return await create_business(business)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("", response_model=List[Business])
async def list_businesses_endpoint():
    try:
        return await list_businesses()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{business_id}", response_model=Business)
async def get_business_endpoint(business_id: str):
    try:
        return await get_business(business_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{business_id}")
async def delete_business_endpoint(business_id: str):
    try:
        await delete_business(business_id)
        return {"success": True}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
