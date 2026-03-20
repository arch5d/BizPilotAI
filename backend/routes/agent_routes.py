"""
Agent execution endpoints.
"""
from fastapi import APIRouter, HTTPException, status

from services.report_service import run_agent


router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("/run/{agent_name}")
async def run_agent_endpoint(agent_name: str, business_id: str):
    try:
        report = await run_agent(agent_name, business_id)
        return {
            "success": True,
            "report_id": str(report.id),
            "agent": report.agent_name,
            "message": "Report generated successfully",
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        # generic for Gemini or db errors
        raise HTTPException(status_code=500, detail=str(e))
