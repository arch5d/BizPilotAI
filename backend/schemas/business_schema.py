"""
BizPilot AI - Pydantic schemas for Business profile.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class BusinessCreate(BaseModel):
    """Schema for creating/updating a business profile."""
    name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    goals: Optional[str] = None


class BusinessResponse(BaseModel):
    """Schema for business API response."""
    id: int
    name: str
    industry: Optional[str] = None
    website: Optional[str] = None
    description: Optional[str] = None
    goals: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
