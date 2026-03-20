"""
BizPilotAI - Pydantic models for request/response validation.
Database models represent MongoDB documents.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class BusinessBase(BaseModel):
    """Base business model with common fields."""
    name: str = Field(..., min_length=1, max_length=200)
    industry: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    website: Optional[str] = Field(None, max_length=500)
    goals: Optional[str] = None


class BusinessCreate(BusinessBase):
    """Model for creating a new business."""
    pass


class BusinessUpdate(BaseModel):
    """Model for updating business information."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    industry: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    website: Optional[str] = Field(None, max_length=500)
    goals: Optional[str] = None


class Business(BusinessBase):
    """Business model with database fields."""
    id: str = Field(..., alias="_id")
    created_at: datetime

    class Config:
        populate_by_name = True


class ReportBase(BaseModel):
    """Base report model with common fields."""
    agent_name: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)


class ReportCreate(ReportBase):
    """Model for creating a new report."""
    business_id: str = Field(..., alias="_id")


class Report(ReportBase):
    """Report model with database fields."""
    id: str = Field(..., alias="_id")
    business_id: str
    created_at: datetime

    class Config:
        populate_by_name = True
