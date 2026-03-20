"""
BizPilotAI - Sales Agent
Generates comprehensive sales strategy reports.
"""
from typing import Dict, Any

from agents.base_agent import BaseAgent
from core.prompt_builder import PromptBuilder


class SalesAgent(BaseAgent):
    """Sales strategy agent using Gemini API."""
    
    def __init__(self):
        super().__init__("sales")
    
    def get_agent_name(self) -> str:
        return "sales"
    
    async def generate_report(self, business: Dict[str, Any]) -> str:
        prompt = PromptBuilder.get_prompt_for_agent("sales", business)
        report = await self._call_gemini(prompt, temperature=0.7)
        return report
