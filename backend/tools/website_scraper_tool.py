"""
BizPilot AI - Website scraper tool.
Fetches website text and stores it in ChromaDB for use by agents.
"""
import re
from typing import Optional

import requests
from bs4 import BeautifulSoup
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

try:
    from services.chroma_service import add_website_text
except ImportError:
    add_website_text = None


def scrape_url(url: str, max_chars: int = 50000) -> str:
    """Fetch URL and extract visible text."""
    if not url or not url.strip():
        return ""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        headers = {"User-Agent": "BizPilotAI-Scraper/1.0 (Business Analysis)"}
        resp = requests.get(url, timeout=15, headers=headers)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        text = re.sub(r"\n\s*\n", "\n\n", text)
        text = re.sub(r" +", " ", text).strip()
        return text[:max_chars] if len(text) > max_chars else text
    except Exception:
        return ""


def scrape_website_and_store(url: str, business_id: int) -> str:
    """Scrape URL and store in ChromaDB. Returns extracted text."""
    text = scrape_url(url)
    if text and add_website_text is not None:
        try:
            add_website_text(business_id, url, text)
        except Exception:
            pass
    return text


class WebsiteScraperInput(BaseModel):
    """Input schema for WebsiteScraperTool."""
    url: str = Field(description="Full URL to fetch (e.g. https://example.com)")


class WebsiteScraperTool(BaseTool):
    """
    CrewAI tool: fetch website content and return extracted text.
    """
    name: str = "scrape_website"
    description: str = (
        "Fetches a website URL and returns the main text content. "
        "Use this to analyze company websites for context."
    )
    args_schema: type[BaseModel] = WebsiteScraperInput

    def _run(self, url: str) -> str:
        return scrape_url(url)
