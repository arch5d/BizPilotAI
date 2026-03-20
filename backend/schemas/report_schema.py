"""
BizPilot AI - Pydantic schemas for API validation.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReportCreate(BaseModel):
    """Schema for creating a report."""
    agent_name: str
    content: str


class ReportResponse(BaseModel):
    """Schema for report API response."""
    id: int
    agent_name: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class AgentRunResponse(BaseModel):
    """Schema for agent run API response."""
    success: bool
    message: str
    report_id: Optional[int] = None
