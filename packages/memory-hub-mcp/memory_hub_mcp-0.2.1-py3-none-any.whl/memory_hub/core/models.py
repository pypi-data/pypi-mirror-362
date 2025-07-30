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

class MemoryTypeInfo(BaseModel):
    type_name: str = Field(..., description="The memory type name")
    count: int = Field(..., description="Number of memories with this type")
    latest_version: int = Field(..., description="Highest version number for this type")
    last_updated: str = Field(..., description="ISO timestamp of most recent memory")

class ListMemoryTypesResponse(BaseModel):
    memory_types: List[MemoryTypeInfo] = Field(..., description="List of memory types with metadata")
    total_types: int = Field(..., description="Total number of unique memory types")
    points_scanned: int = Field(..., description="Number of points scanned")

class GetProjectMemoriesRequest(BaseModel):
    app_id: str = Field(..., description="Required - Application identifier")
    project_id: Optional[str] = Field(None, description="Optional - Project identifier to filter by")
    ticket_id: Optional[str] = Field(None, description="Optional - Ticket identifier to filter by")
    limit: int = Field(default=50, description="Maximum number of results to return")
    sort_by: str = Field(default="timestamp", description="Sort field: 'timestamp' or 'score'")

class UpdateMemoryRequest(BaseModel):
    app_id: str = Field(..., description="Required - Application identifier")
    project_id: Optional[str] = Field(None, description="Optional - Project identifier")
    ticket_id: Optional[str] = Field(None, description="Optional - Ticket identifier")
    memory_type: Optional[str] = Field(None, description="Optional - Memory type to identify which memory to update")
    new_content: str = Field(..., description="New content to replace the existing memory")
    metadata_updates: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata fields to update")

class GetRecentMemoriesRequest(BaseModel):
    app_id: Optional[str] = Field(None, description="Optional - Filter by application identifier")
    project_id: Optional[str] = Field(None, description="Optional - Filter by project identifier")
    hours: int = Field(default=24, description="Number of hours to look back (default: 24)")
    limit: int = Field(default=20, description="Maximum number of results to return")
    include_summary: bool = Field(default=True, description="Whether to include AI-generated summary")

class ListMemoryTypesRequest(BaseModel):
    app_id: Optional[str] = Field(None, description="Optional - Filter by application identifier")
    project_id: Optional[str] = Field(None, description="Optional - Filter by project identifier")

class GetMemoryTypeGuideResponse(BaseModel):
    create_new_types: List[str] = Field(..., description="Memory types that should always CREATE new memories")
    update_types: List[str] = Field(..., description="Memory types that should typically be UPDATED")
    guidelines: str = Field(..., description="Guidelines for using memory types") 