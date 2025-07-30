# endpoints.py - FastAPI route handlers for Memory Hub MCP Server

import hashlib
import time
import uuid
import re
import json
from typing import List, Set
# Removed FastAPI dependencies for stdio-only MCP server
import httpx

# Simple exception class to replace FastAPI ValidationError
class ValidationError(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)
from qdrant_client.http import models

from .config import QDRANT_COLLECTION_NAME, ENABLE_GEMMA_SUMMARIZATION
from .models import (
    MemoryItemIn, MemorySearchRequest, RetrievedChunk, 
    SearchResponse, AddMemoryResponse, ListIdsResponse
)
from .services import qdrant_client, get_embedding, synthesize_search_results, get_chat_completions_endpoint
from .chunking import create_semantic_chunker
from .utils.dependencies import get_http_client

# Import handler functions
from .handlers.memory_handlers import add_memory as add_memory_handler, search_memories as search_memories_handler
from .handlers.list_handlers import list_app_ids as list_app_ids_handler, list_project_ids as list_project_ids_handler, list_ticket_ids as list_ticket_ids_handler
from .handlers.health_handlers import health_check as health_check_handler

# Initialize semantic chunker
try:
    semantic_chunker = create_semantic_chunker(chunk_size=90)
except Exception as e:
    print(f"ERROR: Failed to initialize semantic chunker: {e}")
    raise ValidationError(status_code=500, detail="Failed to initialize semantic chunker")


async def expand_query_with_keywords(query_text: str, metadata_filters: dict, client: httpx.AsyncClient) -> str:
    """
    Expand search query by finding related keywords from existing chunks in the same context.
    This helps find semantically related content even if different terminology is used.
    """
    try:
        # Quick search to find related keywords from the same app/project context
        if not metadata_filters:
            return query_text  # Can't expand without context
        
        # Create a simplified filter for context matching
        context_filter = models.Filter(
            must=[models.FieldCondition(key=k, match=models.MatchValue(value=v)) 
                  for k, v in metadata_filters.items()]
        )
        
        # Get a small sample of chunks from the same context
        sample_results = qdrant_client.search(
            collection_name=QDRANT_COLLECTION_NAME,
            query_vector=await get_embedding(query_text, client),
            query_filter=context_filter,
            limit=5,  # Small sample
            with_payload=True,
            with_vectors=False
        )
        
        # Extract keywords from top matching chunks
        related_keywords = set()
        for hit in sample_results:
             keywords = hit.payload.get("keywords", [])
             related_keywords.update(keywords)
        
        # Add relevant keywords to query (limit to avoid query bloat)
        if related_keywords:
            keyword_addition = " ".join(list(related_keywords)[:3])
            expanded = f"{query_text} {keyword_addition}"
            return expanded
        
        return query_text
    
    except Exception as e:
        print(f"WARN: Query expansion failed: {e}")
        return query_text  # Fallback to original query

def calculate_keyword_enhanced_score(vector_score: float, query_text: str, keywords: List[str]) -> float:
    """
    Enhance vector similarity score with keyword relevance matching.
    This provides hybrid search combining semantic and lexical matching.
    """
    # Start with the vector similarity score
    enhanced_score = vector_score
    
    # Convert query and keywords to lowercase for matching
    query_lower = query_text.lower()
    all_keywords = [kw.lower() for kw in keywords]
    
    # Keyword matching bonuses
    exact_matches = sum(1 for keyword in all_keywords if keyword in query_lower)
    partial_matches = sum(1 for keyword in all_keywords 
                         if any(word in keyword or keyword in word 
                               for word in query_lower.split()))
    
    # Calculate keyword bonus (up to 20% boost)
    if exact_matches > 0:
        keyword_boost = min(0.15, exact_matches * 0.05)  # 5% per exact match, max 15%
    elif partial_matches > 0:
        keyword_boost = min(0.10, partial_matches * 0.02)  # 2% per partial match, max 10%
    else:
        keyword_boost = 0
    
    # Apply keyword boost
    enhanced_score = min(1.0, vector_score + keyword_boost)
    
    return enhanced_score

async def generate_chunk_keywords(chunk_text: str, client: httpx.AsyncClient) -> List[str]:
    """
    Generate chunk-specific keywords using Gemma LLM.
    
    This provides precise keyword extraction by understanding the semantic content 
    of each chunk and identifying the most searchable terms.
    """
    try:
        # Truncate chunk text if too long to prevent context overflow
        max_chunk_length = 2000  # Conservative limit for keyword extraction
        if len(chunk_text) > max_chunk_length:
            chunk_text = chunk_text[:max_chunk_length] + "..."
            print(f"WARN: Truncated chunk text for keyword extraction ({max_chunk_length} chars)")

        prompt = f"""Analyze this text chunk and extract 3-5 specific, relevant keywords that would help someone find this content in a search.

Text chunk:
{chunk_text}

Requirements:
- Return ONLY a JSON array of keywords, nothing else
- Focus on technical terms, proper nouns, and key concepts  
- Avoid generic words like "the", "and", "system"
- Keep keywords short and specific (1-2 words ideal)
- Examples: ["bedrock", "api", "dealership", "recommendations", "inventory"]

Keywords:"""

        # Make request to Gemma with timeout and proper error handling
        try:
            response = await client.post(
                f"{get_chat_completions_endpoint()}",
                json={
                    "model": "gemma-3-4b",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.1,
                    "max_tokens": 100
                },
                timeout=15.0  # Explicit timeout for keyword extraction
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"].strip()
                
                # Try to parse JSON array from response
                try:
                    keywords = json.loads(content)
                    if isinstance(keywords, list) and len(keywords) <= 5:
                        # Clean and validate keywords
                        cleaned_keywords = [kw.lower().strip() for kw in keywords if isinstance(kw, str) and len(kw) > 2]
                        return cleaned_keywords[:5]
                except json.JSONDecodeError:
                    # Fallback: extract keywords from content if JSON parsing fails
                    keywords = re.findall(r'"([^"]+)"', content)
                    if keywords:
                        return [kw.lower().strip() for kw in keywords[:5]]
            else:
                print(f"WARN: Gemma keyword extraction HTTP error: {response.status_code}")
        
        except httpx.TimeoutException:
            print(f"WARN: Gemma keyword extraction timed out")
        except httpx.HTTPStatusError as e:
            print(f"WARN: Gemma keyword extraction HTTP error: {e}")
        except Exception as e:
            print(f"WARN: Gemma keyword extraction request failed: {e}")
        
        print(f"WARN: Gemma keyword extraction failed, returning empty keywords")
        return []
        
    except Exception as e:
        print(f"ERROR: Gemma keyword extraction failed: {e}")
        return []

# --- Memory Management Endpoints ---

async def add_memory(memory_item: MemoryItemIn, client: httpx.AsyncClient : httpx.AsyncClient):
    """
    Adds memory content. Chunks content, gets embeddings, and stores in Qdrant.
    Supports flexible hierarchy: app_id (required), project_id (optional), ticket_id (optional).
    """
    return await add_memory_handler(memory_item, client)

async def search_memories(search_request: MemorySearchRequest, client: httpx.AsyncClient : httpx.AsyncClient):
    """
    Searches memories in Qdrant with keyword-enhanced querying, then uses LM Studio to synthesize results.
    """
    return await search_memories_handler(search_request, client)

# --- ID Listing Endpoints ---

async def list_app_ids():
    """
    Lists all unique app_ids found in the Memory Hub.
    """
    return await list_app_ids_handler()

async def list_project_ids():
    """
    Lists all unique project_ids found in the Memory Hub.
    """
    return await list_project_ids_handler()

async def list_ticket_ids():
    """
    Lists all unique ticket_ids found in the Memory Hub.
    """
    return await list_ticket_ids_handler()

# --- System Endpoints ---

async def health_check():
    """Health check endpoint."""
    return await health_check_handler() 