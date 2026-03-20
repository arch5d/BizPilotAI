"""
BizPilot AI - ChromaDB service for storing and querying website text.
"""
import hashlib
from typing import Optional

import chromadb
from chromadb.config import Settings

from config import CHROMADB_PATH

# Persistent client; collection name for website content
COLLECTION_NAME = "website_texts"

_client: Optional[chromadb.PersistentClient] = None


def get_chroma_client() -> chromadb.PersistentClient:
    """Get or create persistent ChromaDB client."""
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=CHROMADB_PATH, settings=Settings(anonymized_telemetry=False))
    return _client


def get_website_collection():
    """Get or create the collection for website texts."""
    client = get_chroma_client()
    return client.get_or_create_collection(name=COLLECTION_NAME, metadata={"description": "Scraped website content"})


def _doc_id(business_id: int, url: str) -> str:
    """Generate stable document ID for business + URL."""
    return hashlib.sha256(f"{business_id}:{url}".encode()).hexdigest()[:32]


def add_website_text(business_id: int, url: str, text: str, metadata: Optional[dict] = None) -> None:
    """Store website text in ChromaDB for a business."""
    if not text or not text.strip():
        return
    coll = get_website_collection()
    doc_id = _doc_id(business_id, url)
    meta = {"business_id": business_id, "url": url}
    if metadata:
        meta.update(metadata)
    coll.upsert(
        ids=[doc_id],
        documents=[text[:100_000]],
        metadatas=[meta],
    )


def get_website_texts_for_business(business_id: int, limit: int = 5) -> list[str]:
    """Retrieve stored website texts for a business."""
    coll = get_website_collection()
    try:
        results = coll.get(
            where={"business_id": business_id},
            limit=limit,
            include=["documents"],
        )
        if results and results.get("documents"):
            return results["documents"]
    except Exception:
        pass
    return []
