"""
BizPilotAI - Centralized Gemini API client.
Handles all interactions with Google Gemini API.
"""
import asyncio
from typing import Optional
import google.generativeai as genai

from config import GEMINI_API_KEY, GEMINI_MODEL, REQUEST_TIMEOUT


class AIClient:
    """Centralized AI client for Gemini API interactions."""
    
    def __init__(self):
        """Initialize the AI client with Gemini API."""
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = GEMINI_MODEL
        self._client = genai.GenerativeModel(self.model)
    
    async def generate_report(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a report using Gemini API.
        
        Args:
            prompt: The prompt to send to Gemini
            temperature: Controls randomness (0-2)
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text response from Gemini
            
        Raises:
            ValueError: If prompt is empty
            RuntimeError: If API call fails
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        try:
            # Run the API call in a thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            response = await asyncio.wait_for(
                loop.run_in_executor(
                    None,
                    self._call_gemini,
                    prompt,
                    temperature,
                    max_tokens
                ),
                timeout=REQUEST_TIMEOUT
            )
            return response
        except asyncio.TimeoutError:
            raise RuntimeError(f"Gemini API request timed out after {REQUEST_TIMEOUT}s")
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")
    
    def _call_gemini(
        self,
        prompt: str,
        temperature: float,
        max_tokens: Optional[int]
    ) -> str:
        """
        Synchronous wrapper for Gemini API call.
        
        Args:
            prompt: The prompt to send
            temperature: Temperature setting
            max_tokens: Maximum tokens
            
        Returns:
            Generated text
        """
        generation_config = {
            "temperature": temperature,
        }
        
        if max_tokens:
            generation_config["max_output_tokens"] = max_tokens
        
        response = self._client.generate_content(
            prompt,
            generation_config=genai.types.GenerationConfig(
                **generation_config
            )
        )
        
        if not response.text:
            raise RuntimeError("Empty response from Gemini API")
        
        return response.text


# Global AI client instance
_ai_client: Optional[AIClient] = None


def get_ai_client() -> AIClient:
    """Get or create the global AI client instance."""
    global _ai_client
    if _ai_client is None:
        _ai_client = AIClient()
    return _ai_client


async def initialize_ai():
    """Initialize the AI client (called during app startup)."""
    get_ai_client()
    print("AI Client initialized successfully")


async def shutdown_ai():
    """Shutdown the AI client (called during app shutdown)."""
    global _ai_client
    _ai_client = None
    print("AI Client shutdown")
