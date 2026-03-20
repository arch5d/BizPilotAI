"""
Agent orchestration service - selects and runs the appropriate agent.
"""
from typing import Dict

from report_service import run_agent


async def execute_agent(agent_name: str, business_id: str) -> Dict[str, str]:
    """Run an agent and return summary result."""
    report = await run_agent(agent_name, business_id)
    return {
        "report_id": str(report.id),
        "agent": report.agent_name,
        "message": "Report generated successfully",
    }
