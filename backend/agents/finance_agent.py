"""
BizPilotAI - Finance Agent
Generates comprehensive financial reports.
"""
from typing import Dict, Any

from agents.base_agent import BaseAgent
from core.prompt_builder import PromptBuilder


class FinanceAgent(BaseAgent):
    """Finance strategy agent using Gemini API."""
    
    def __init__(self):
        super().__init__("finance")
    
    def get_agent_name(self) -> str:
        return "finance"
    
    async def generate_report(self, business: Dict[str, Any]) -> str:
        prompt = PromptBuilder.get_prompt_for_agent("finance", business)
        report = await self._call_gemini(prompt, temperature=0.7)
        return report

