"""
BizPilotAI - Strategy Agent
Generates high-level strategic reports for CEOs.
"""
from typing import Dict, Any

from agents.base_agent import BaseAgent
from core.prompt_builder import PromptBuilder


class StrategyAgent(BaseAgent):
    """Strategy agent using Gemini API."""
    
    def __init__(self):
        super().__init__("strategy")
    
    def get_agent_name(self) -> str:
        return "strategy"
    
    async def generate_report(self, business: Dict[str, Any]) -> str:
        prompt = PromptBuilder.get_prompt_for_agent("strategy", business)
        report = await self._call_gemini(prompt, temperature=0.7)
        return report
