"""
BizPilot AI - Base agent class for all agents.
Provides reusable interface and built-in OpenAI support.
"""

import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except Exception:
    OPENAI_AVAILABLE = False


class BaseAgent(ABC):
    """
    Abstract base class for BizPilot AI agents.
    Includes built-in AI generation helper.
    """

    name: str = "base_agent"
    description: str = "Base agent - override in subclass"

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client: Optional["OpenAI"] = None

        if OPENAI_AVAILABLE and self.api_key:
            self.client = OpenAI(api_key=self.api_key)

    @abstractmethod
    def run(self, **kwargs: Any) -> str:
        """Execute the agent and return report content."""
        pass

    def generate_ai_report(self, prompt: str) -> str:
        """
        Generate report using OpenAI if available.
        Falls back to simulated response if not configured.
        """

        if not self.client:
            return (
                "# Simulated Report\n\n"
                "OpenAI API key not configured.\n"
                "Add OPENAI_API_KEY in backend/.env to enable real AI reports.\n\n"
                f"Prompt preview:\n{prompt[:300]}"
            )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a senior business analyst generating professional reports.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=0.7,
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"AI generation failed: {str(e)}"

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
        }


class AsyncBaseAgent(ABC):
    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    async def run(self, data: dict) -> dict:
        raise NotImplementedError