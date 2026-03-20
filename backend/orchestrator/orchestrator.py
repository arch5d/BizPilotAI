"""
BizPilot AI - Agent Orchestrator.
Coordinates agent execution, result handling, and database persistence.
Designed to support multiple agents via agent registry pattern.
Passes business context to agents when business_id is provided.
"""
from typing import Any, Dict, Optional, Type

from sqlalchemy.orm import Session

from agents.base_agent import BaseAgent
from agents.marketing_agent import MarketingTrendAgent
from database.models import Report, Business
from tools.website_scraper_tool import scrape_website_and_store

try:
    from services.chroma_service import get_website_texts_for_business
except ImportError:
    def get_website_texts_for_business(business_id: int, limit: int = 5) -> list:
        return []


# Agent registry - add new agents here for automatic routing
AGENT_REGISTRY: Dict[str, Type[BaseAgent]] = {
    "marketing": MarketingTrendAgent,
}


def get_agent(agent_name: str) -> Optional[BaseAgent]:
    """
    Factory function to get agent instance by name.
    Extensible for adding new agents.
    """
    agent_class = AGENT_REGISTRY.get(agent_name.lower())
    if agent_class:
        return agent_class()
    return None


def _build_business_context(db: Session, business_id: int) -> Optional[Dict[str, Any]]:
    """Load business, scrape website into ChromaDB, return context for agent."""
    business = db.query(Business).filter(Business.id == business_id).first()
    if not business:
        return None
    website_text = ""
    if business.website:
        website_text = scrape_website_and_store(business.website, business.id)
    if not website_text:
        try:
            texts = get_website_texts_for_business(business.id, limit=2)
            website_text = "\n\n".join(texts) if texts else ""
        except Exception:
            pass
    return {
        "name": business.name,
        "industry": business.industry or "",
        "website": business.website or "",
        "description": business.description or "",
        "goals": business.goals or "",
        "website_text": website_text[:15000] if website_text else "",
    }


def run_agent(
    agent_name: str,
    db: Session,
    business_id: Optional[int] = None,
    **kwargs: Any,
) -> tuple[bool, Optional[int], str]:
    """
    Run specified agent, save report to database, return result.
    If business_id is provided, passes business_context to the agent.
    """
    agent = get_agent(agent_name)
    if not agent:
        return False, None, f"Unknown agent: {agent_name}"

    business_context = None
    if business_id:
        business_context = _build_business_context(db, business_id)

    try:
        content = agent.run(business_context=business_context, **kwargs)

        # Save to database
        report = Report(
            agent_name=agent.name,
            content=content,
        )
        db.add(report)
        db.commit()
        db.refresh(report)

        return True, report.id, f"Report generated successfully (ID: {report.id})"
    except Exception as e:
        db.rollback()
        return False, None, str(e)


def list_agents() -> list[Dict[str, str]]:
    """Return metadata for all registered agents."""
    return [
        get_agent(name).get_metadata()
        for name in AGENT_REGISTRY
        if get_agent(name)
    ]
