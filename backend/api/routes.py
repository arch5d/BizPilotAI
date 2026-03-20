"""
BizPilot AI - API route definitions.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.db import get_db
from database.models import Report, Business
from schemas.report_schema import ReportResponse, AgentRunResponse
from schemas.business_schema import BusinessCreate, BusinessResponse
from orchestrator.orchestrator import run_agent

router = APIRouter()


@router.get("/health")
def health_check():
    """Health check endpoint for monitoring and load balancers."""
    return {"status": "healthy", "service": "BizPilot AI"}


@router.post("/business/create", response_model=BusinessResponse)
def create_business(data: BusinessCreate, db: Session = Depends(get_db)):
    """Create a new business profile."""
    business = Business(
        name=data.name,
        industry=data.industry,
        website=data.website,
        description=data.description,
        goals=data.goals,
    )
    db.add(business)
    db.commit()
    db.refresh(business)
    return business


@router.get("/business", response_model=list[BusinessResponse])
def get_businesses(db: Session = Depends(get_db)):
    """Return all business profiles, newest first."""
    businesses = db.query(Business).order_by(Business.created_at.desc()).all()
    return businesses

@router.delete("/business/{business_id}")
def delete_business(business_id: int, db: Session = Depends(get_db)):
    business = db.query(Business).filter(Business.id == business_id).first()

    if not business:
        raise HTTPException(status_code=404, detail="Business not found")

    # Delete related reports first
    db.query(Report).filter(Report.business_id == business_id).delete()

    db.delete(business)
    db.commit()

    return {"success": True, "message": "Business and related reports deleted"}

@router.post("/agents/run/marketing", response_model=AgentRunResponse)
def run_marketing_agent(
    db: Session = Depends(get_db),
    business_id: int | None = Query(None, description="Optional business profile ID for personalized report"),
):
    """
    Run the Marketing Trend Agent.
    Optionally pass business_id to use that profile for personalized report.
    """
    success, report_id, message = run_agent("marketing", db, business_id=business_id)
    if not success:
        raise HTTPException(status_code=500, detail=message)
    return AgentRunResponse(
        success=True,
        message=message,
        report_id=report_id,
    )


@router.get("/reports", response_model=list[ReportResponse])
def get_reports(db: Session = Depends(get_db)):
    """Return all reports from the database, newest first."""
    reports = db.query(Report).order_by(Report.created_at.desc()).all()
    return reports


@router.post("/run-agents")
async def run_agents(payload: dict):
    """
    Run all simple BizPilot agents (currently FinanceAgent).

    Expects a JSON object with at least `revenue` and `expenses` keys.
    """
    from services.agent_runner import AgentRunner

    runner = AgentRunner()
    results = await runner.run_all(payload)
    return {"success": True, "results": results}

@router.delete("/reports/{report_id}")
def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.id == report_id).first()

    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    db.delete(report)
    db.commit()

    return {"success": True, "message": "Report deleted"}