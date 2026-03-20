"""
Report-related endpoints.
"""
from typing import List
from fastapi import APIRouter, HTTPException, status

from services.report_service import (
    list_reports,
    list_reports_for_business,
    delete_report,
)
from database.models import Report


router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("", response_model=List[Report])
async def list_reports_endpoint():
    try:
        return await list_reports()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/business/{business_id}", response_model=List[Report])
async def list_reports_for_business_endpoint(business_id: str):
    try:
        return await list_reports_for_business(business_id)
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{report_id}")
async def delete_report_endpoint(report_id: str):
    try:
        await delete_report(report_id)
        return {"success": True}
    except ValueError as ve:
        raise HTTPException(status_code=404, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
