"""
BizPilotAI - Marketing Agent
Generates comprehensive marketing strategy reports.
"""
from typing import Dict, Any

from agents.base_agent import BaseAgent
from core.prompt_builder import PromptBuilder


class MarketingAgent(BaseAgent):
    """Marketing strategy agent using Gemini API."""
    
    def __init__(self):
        """Initialize the marketing agent."""
        super().__init__("marketing")
    
    def get_agent_name(self) -> str:
        """Return agent name."""
        return "marketing"
    
    async def generate_report(self, business: Dict[str, Any]) -> str:
        """
        Generate a marketing report for the business.
        
        Args:
            business: Business document from MongoDB
            
        Returns:
            Marketing report as markdown string
        """
        prompt = PromptBuilder.get_prompt_for_agent("marketing", business)
        report = await self._call_gemini(prompt, temperature=0.7)
        return report
