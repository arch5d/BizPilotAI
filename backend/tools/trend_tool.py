"""
BizPilot AI - Trend analysis tool.
Simulates business and AI trend data for the Marketing Agent.
ChromaDB-ready: can be extended to use vector search for real trend data.
"""
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class TrendToolInput(BaseModel):
    """Input schema for TrendTool - extensible for future parameters."""
    query: str = Field(default="", description="Optional query to focus trend analysis")


class TrendTool(BaseTool):
    """
    Tool that provides simulated business and AI trend data.
    Returns structured trend insights for agent analysis.
    """
    name: str = "get_trend_data"
    description: str = (
        "Retrieves current business and AI market trends. "
        "Use this to analyze and summarize trends for reports."
    )
    args_schema: Type[BaseModel] = TrendToolInput

    def _run(self, query: str = "") -> str:
        """
        Returns simulated trend data. In production, this could query
        ChromaDB, external APIs, or real data sources.
        """
        trends = [
            "AI automation rising - 67% of enterprises increasing AI adoption in 2024",
            "SaaS growth increasing - Cloud software market projected to reach $700B by 2025",
            "Marketing AI adoption - 80% of marketers plan to use AI for content creation",
            "Personalization demand - Hyper-personalization drives 40% higher conversion",
            "Video marketing surge - Short-form video engagement up 2.5x year-over-year",
            "Sustainability focus - 73% of consumers prefer eco-friendly brands",
            "Remote work tools - Collaboration software market growing 12% annually",
            "Data privacy regulations - GDPR-style laws expanding globally",
        ]
        return "\n".join(trends)
