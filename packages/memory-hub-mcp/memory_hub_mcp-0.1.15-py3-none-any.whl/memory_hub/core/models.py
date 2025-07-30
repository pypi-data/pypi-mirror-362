# models.py - Pydantic models for Memory Hub MCP Server

from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Union, Any

# --- Pydantic Models ---
class MemoryItemIn(BaseModel):
    content: str = Field(..., description="The content to store in memory")
    metadata: Dict[str, Any] = Field(..., description="Metadata with flexible hierarchy: app_id (required), project_id (optional), ticket_id (optional), type, etc.")

class MemorySearchRequest(BaseModel):
    query_text: str = Field(..., description="The query text to search for")
    metadata_filters: Dict[str, str] = Field(default_factory=dict, description="Metadata filters for search")
    keyword_filters: List[str] = Field(default_factory=list, description="List of keywords that results must contain")
    limit: int = Field(default=10, description="Maximum number of results to return")

class RetrievedChunk(BaseModel):
    text_chunk: str
    metadata: Dict[str, Any]
    score: float
    chunk_id: str

class SearchResponse(BaseModel):
    synthesized_summary: Optional[str] = Field(default=None, description="AI-generated summary of results")
    retrieved_chunks: List[RetrievedChunk]
    total_results: int

class AddMemoryResponse(BaseModel):
    message: str
    chunks_stored: int
    original_content_hash: str

# --- New Introspection Models ---
class ListIdsResponse(BaseModel):
    ids: List[str] = Field(..., description="List of unique identifiers found")
    total_count: int = Field(..., description="Total number of unique identifiers")
    points_scanned: int = Field(..., description="Number of points scanned to extract IDs") 