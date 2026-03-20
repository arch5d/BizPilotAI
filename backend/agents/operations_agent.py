"""
BizPilotAI - Operations Agent
Generates comprehensive operations improvement reports.
"""
from typing import Dict, Any

from agents.base_agent import BaseAgent
from core.prompt_builder import PromptBuilder


class OperationsAgent(BaseAgent):
    """Operations strategy agent using Gemini API."""
    
    def __init__(self):
        super().__init__("operations")
    
    def get_agent_name(self) -> str:
        return "operations"
    
    async def generate_report(self, business: Dict[str, Any]) -> str:
        prompt = PromptBuilder.get_prompt_for_agent("operations", business)
        report = await self._call_gemini(prompt, temperature=0.7)
        return report
