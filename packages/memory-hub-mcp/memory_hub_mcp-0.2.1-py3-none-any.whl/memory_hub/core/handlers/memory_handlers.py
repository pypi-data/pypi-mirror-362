# handlers/memory_handlers.py - Memory-related endpoint handlers

import hashlib
import time
import uuid
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any
# Removed FastAPI dependencies for stdio-only MCP server
import httpx

# Simple exception class to replace FastAPI ValidationError
class ValidationError(Exception):
    def __init__(self, detail: str, status_code: int = 400):
        self.detail = detail
        self.status_code = status_code
        super().__init__(detail)
from qdrant_client.http import models
from collections import defaultdict

from ..config import (
    QDRANT_COLLECTION_NAME, ENABLE_GEMMA_SUMMARIZATION, SEARCH_RESULT_MULTIPLIER,
    MAX_SEARCH_RESULTS, MAX_SUMMARIZATION_CHUNKS
)
from ..models import (
    MemoryItemIn, MemorySearchRequest, RetrievedChunk, 
    SearchResponse, AddMemoryResponse, GetProjectMemoriesRequest,
    UpdateMemoryRequest, GetRecentMemoriesRequest
)
from ..services import get_embedding, synthesize_search_results, AppConfig
from ..chunking import create_semantic_chunker
from ..utils.dependencies import get_http_client
from ..utils.search_utils import (
    expand_query_with_keywords, calculate_keyword_enhanced_score,
    generate_chunk_keywords
)

# Initialize semantic chunker
try:
    semantic_chunker = create_semantic_chunker(chunk_size=90)
except Exception as e:
    print(f"ERROR: Failed to initialize semantic chunker: {e}")
    raise ValidationError(status_code=500, detail="Failed to initialize semantic chunker")

def safe_int_conversion(value, default=1):
    """
    Safely convert version field to integer, handling string floats like "1.0".
    
    Args:
        value: The value to convert (could be int, float, string)
        default: Default value if conversion fails
        
    Returns:
        int: The converted integer value
    """
    if value is None:
        return default
    
    try:
        # Handle string values that might be "1.0"
        if isinstance(value, str):
            # Convert string to float first, then to int
            return int(float(value))
        # Handle numeric values
        elif isinstance(value, (int, float)):
            return int(value)
        else:
            print(f"WARN: Unexpected version type {type(value)}: {value}, using default {default}")
            return default
    except (ValueError, TypeError) as e:
        print(f"WARN: Failed to convert version '{value}' to int: {e}, using default {default}")
        return default

async def add_memory(memory_item: MemoryItemIn, config: AppConfig):
    """
    Adds memory content. Chunks content, gets embeddings, and stores in Qdrant.
    Supports flexible hierarchy: app_id (required), project_id (optional), ticket_id (optional).
    """
    try:
        # Validate that app_id is provided
        if not memory_item.metadata.get("app_id"):
            raise ValidationError(status_code=400, detail="app_id is required in metadata")
        
        # Normalize metadata types to prevent future conversion issues
        normalized_metadata = dict(memory_item.metadata)
        
        # Ensure version is stored as integer
        if 'version' in normalized_metadata:
            normalized_metadata['version'] = safe_int_conversion(normalized_metadata['version'])
        else:
            # Default version if not provided
            normalized_metadata['version'] = 1
        
        # Ensure timestamp_iso is provided if not present
        if "timestamp_iso" not in normalized_metadata:
            from datetime import datetime, timedelta
            normalized_metadata["timestamp_iso"] = datetime.utcnow().isoformat() + "Z"
        
        app_id = normalized_metadata.get('app_id', 'N/A')
        project_id = normalized_metadata.get('project_id', None)
        ticket_id = normalized_metadata.get('ticket_id', None)
        
        # Determine hierarchy level for logging
        if ticket_id:
            level = "ticket-level"
            context = f"app: {app_id}, project: {project_id}, ticket: {ticket_id}"
        elif project_id:
            level = "project-level"
            context = f"app: {app_id}, project: {project_id}"
        else:
            level = "app-level"
            context = f"app: {app_id}"
        
        print(f"INFO: Received /add_memory for {level} context ({context})")

        try:
            chunks = semantic_chunker(memory_item.content)  # Using actual semchunk
        except Exception as e:
            print(f"ERROR: Failed to chunk content for {level} context ({context}): {e}")
            raise ValidationError(status_code=500, detail=f"Content chunking failed: {str(e)}")

        if not chunks:
            print(f"WARN: No chunks generated for {level} context ({context}). Content: '{memory_item.content[:100]}'")
            # This might happen if content is very short or only whitespace
            if not memory_item.content.strip():
                raise ValidationError(status_code=400, detail="Content is empty or only whitespace.")
            # If content is not empty but semchunk didn't chunk, store the original content as a single chunk
            chunks = [memory_item.content.strip()]

        points_to_upsert = []
        original_content_hash = hashlib.sha256(memory_item.content.encode()).hexdigest()

        for i, chunk_text in enumerate(chunks):
            if not chunk_text: # Skip empty chunks
                continue
            try:
                embedding = await get_embedding(chunk_text, config.http_client, config)
                
                # Generate chunk-specific keywords using Gemma
                chunk_keywords = await generate_chunk_keywords(chunk_text, config)
                
                chunk_metadata = normalized_metadata.copy() # Start with normalized metadata
                chunk_metadata["original_content_hash"] = original_content_hash
                chunk_metadata["chunk_index"] = i
                chunk_metadata["total_chunks"] = len(chunks)
                chunk_metadata["keywords"] = chunk_keywords  # Use chunk keywords as primary keywords
                # Add the actual chunk text to the payload for Qdrant, so we can retrieve it.
                # Qdrant payload can be any JSON-serializable dict.
                payload = {"text_chunk": chunk_text, **chunk_metadata} 

                points_to_upsert.append(models.PointStruct(
                    id=str(uuid.uuid4()), # Generate unique ID for each chunk point
                    vector=embedding,
                    payload=payload
                ))
            except Exception as e:
                print(f"ERROR: Failed to process chunk {i} for {level} context ({context}): {e}")
                # Decide on error strategy: skip chunk, fail all? For now, skip faulty chunks.

        if not points_to_upsert:
            print(f"ERROR: No valid points generated for upsertion for {level} context ({context})")
            raise ValidationError(status_code=500, detail="No data could be prepared for storage after chunking/embedding.")

        try:
            config.qdrant_client.upsert(
                collection_name=QDRANT_COLLECTION_NAME,
                points=points_to_upsert,
                wait=True # Wait for operation to complete
            )
            print(f"INFO: Successfully upserted {len(points_to_upsert)} points for {level} context ({context})")
            return AddMemoryResponse(
                message=f"Memory added. {len(points_to_upsert)} chunks stored.",
                chunks_stored=len(points_to_upsert),
                original_content_hash=original_content_hash
            )
        except Exception as e:
            print(f"ERROR: Failed to upsert points to Qdrant for {level} context ({context}): {e}")
            raise ValidationError(status_code=500, detail=f"Storage in Qdrant failed: {str(e)}")

    except Exception as e:
        print(f"ERROR: Failed to add memory: {e}")
        raise ValidationError(status_code=500, detail=f"Failed to add memory: {str(e)}")

async def search_memories(search_request: MemorySearchRequest, config: AppConfig):
    """
    Searches memories in Qdrant with keyword-enhanced querying, then uses LM Studio to synthesize results.
    """
    try:
        # Validate input
        if not search_request.query_text or not search_request.query_text.strip():
            raise ValidationError(
                status_code=400, 
                detail="query_text is required and cannot be empty"
            )

        filters_str = f", filters: {search_request.metadata_filters}" if search_request.metadata_filters else ""
        keyword_str = f", keyword_filters: {search_request.keyword_filters}" if search_request.keyword_filters else ""
        print(f"INFO: Received /search_memories for query: '{search_request.query_text[:50]}...'{filters_str}{keyword_str}")
        
        # Step 1: Expand query with relevant keywords for better semantic matching
        try:
            expanded_query = await expand_query_with_keywords(search_request.query_text, search_request.metadata_filters, config)
            print(f"INFO: Expanded query: '{expanded_query[:100]}...'")
        except Exception as e:
            print(f"WARN: Query expansion failed: {e}")
            expanded_query = search_request.query_text
        
        try:
            query_embedding = await get_embedding(expanded_query, config.http_client, config)
        except Exception as e:
            print(f"ERROR: Failed to get embedding for search query: {e}")
            raise ValidationError(status_code=500, detail=f"Query embedding failed: {str(e)}")

        # Qdrant metadata filtering:
        # Build the filter condition based on provided metadata_filters
        qdrant_filter = None
        if search_request.metadata_filters:
            must_conditions = []
            for key, value in search_request.metadata_filters.items():
                must_conditions.append(models.FieldCondition(key=f"{key}", match=models.MatchValue(value=value))) # Exact match
                # For more complex filtering (e.g., "keywords CONTAINS X"), Qdrant has other Match types
            if must_conditions:
                qdrant_filter = models.Filter(must=must_conditions)
        
        try:
            # Step 2: Get more results initially for keyword-based re-ranking
            search_limit = min(search_request.limit * SEARCH_RESULT_MULTIPLIER, MAX_SEARCH_RESULTS)
            search_results = config.qdrant_client.search(
                collection_name=QDRANT_COLLECTION_NAME,
                query_vector=query_embedding,
                query_filter=qdrant_filter,
                limit=search_limit,
                with_payload=True, # Crucial: get the metadata and text_chunk back
                with_vectors=False # Usually don't need vectors in response
            )
        except Exception as e:
            print(f"ERROR: Qdrant search failed: {e}")
            raise ValidationError(status_code=500, detail=f"Qdrant search failed: {str(e)}")

        retrieved_chunks_for_response: List[RetrievedChunk] = []
        for hit in search_results:
            # The actual text chunk is in the payload, along with all original metadata
            chunk_content = hit.payload.get("text_chunk", "")
            metadata_from_payload = {k: v for k, v in hit.payload.items() if k != "text_chunk"}
            
            # Step 3: Calculate keyword-enhanced score
            enhanced_score = calculate_keyword_enhanced_score(
                hit.score, 
                search_request.query_text, 
                metadata_from_payload.get("keywords", [])
            )
            
            retrieved_chunks_for_response.append(RetrievedChunk(
                chunk_id=str(hit.id), # Qdrant point ID
                text_chunk=chunk_content,
                metadata=metadata_from_payload,
                score=enhanced_score  # Use enhanced score instead of raw vector score
            ))
        
        # Step 4: Apply keyword filtering if specified
        if search_request.keyword_filters:
            filtered_chunks = []
            for chunk in retrieved_chunks_for_response:
                keywords = chunk.metadata.get("keywords", [])
                all_chunk_keywords = [kw.lower() for kw in keywords]
                
                # Check if chunk contains at least one of the required keywords
                required_keywords = [kw.lower() for kw in search_request.keyword_filters]
                if any(req_kw in all_chunk_keywords for req_kw in required_keywords):
                    filtered_chunks.append(chunk)
            
            retrieved_chunks_for_response = filtered_chunks
            print(f"INFO: Keyword filtering reduced results from {len(search_results)} to {len(retrieved_chunks_for_response)}")
        
        # Step 4.5: Version-aware deduplication - prefer highest version within each logical memory group
        memory_groups = defaultdict(list)
        for chunk in retrieved_chunks_for_response:
            # Create a key that uniquely identifies a logical memory
            app_id = chunk.metadata.get('app_id', '')
            project_id = chunk.metadata.get('project_id', '') or 'none'  # Handle None values
            ticket_id = chunk.metadata.get('ticket_id', '') or 'none'
            memory_type = chunk.metadata.get('type', '') or 'none'
            
            memory_key = f"{app_id}|{project_id}|{ticket_id}|{memory_type}"
            memory_groups[memory_key].append(chunk)
        
        # Within each group, prefer chunks from the highest version
        version_filtered_chunks = []
        for memory_key, chunks_in_group in memory_groups.items():
            if len(chunks_in_group) == 1:
                # No versioning conflict, keep the chunk
                version_filtered_chunks.extend(chunks_in_group)
            else:
                # Find the highest version in this group
                max_version = max(safe_int_conversion(chunk.metadata.get('version', 1)) for chunk in chunks_in_group)
                highest_version_chunks = [chunk for chunk in chunks_in_group 
                                        if safe_int_conversion(chunk.metadata.get('version', 1)) == max_version]
                version_filtered_chunks.extend(highest_version_chunks)
                
                print(f"INFO: Version deduplication for {memory_key}: {len(chunks_in_group)} chunks reduced to {len(highest_version_chunks)} (version {max_version})")
        
        retrieved_chunks_for_response = version_filtered_chunks
        
        # Step 5: Re-rank by enhanced scores and limit to requested amount
        retrieved_chunks_for_response.sort(key=lambda x: x.score, reverse=True)
        retrieved_chunks_for_response = retrieved_chunks_for_response[:search_request.limit]

        if not retrieved_chunks_for_response:
            print("INFO: No chunks found matching the search criteria.")
            return SearchResponse(retrieved_chunks=[], total_results=0)

        # --- New Enhancement: Synthesize search results (configurable) ---
        synthesized_summary = None
        if ENABLE_GEMMA_SUMMARIZATION and search_request.query_text:
            try:
                # Use the http_client from the config object
                summary = await synthesize_search_results(search_request.query_text, retrieved_chunks_for_response, config.http_client, config)
                if summary:
                    print("INFO: LM Studio summary generated successfully.")
                    synthesized_summary = summary
                else:
                    print("WARN: LM Studio summarization returned no content.")
            except Exception as e:
                print(f"WARN: Search result summarization failed: {e}. Returning raw chunks.")
                # Proceed to return raw chunks if summarization fails
        else:
            print(f"INFO: Gemma summarization disabled via ENABLE_GEMMA_SUMMARIZATION=false")

        if synthesized_summary:
            return SearchResponse(
                synthesized_summary=synthesized_summary,
                retrieved_chunks=retrieved_chunks_for_response, # Still return chunks for reference or if summary is brief
                total_results=len(retrieved_chunks_for_response)
            )
        else:
            return SearchResponse(
                retrieved_chunks=retrieved_chunks_for_response,
                total_results=len(retrieved_chunks_for_response)
            )

    except ValidationError:
        # Re-raise ValidationErrors as-is
        raise
    except Exception as e:
        print(f"ERROR: Unexpected error in search_memories: {e}")
        raise ValidationError(
            status_code=500, 
            detail=f"Internal server error during search: {str(e)}"
        )

async def get_project_memories(request: GetProjectMemoriesRequest, config: AppConfig):
    """
    Retrieves all memories for a specific app_id/project_id/ticket_id combination without requiring a search query.
    This is designed for agents to pull all context from a specific project without guessing search terms.
    """
    try:
        # Validate input
        if not request.app_id:
            raise ValidationError(
                status_code=400, 
                detail="app_id is required"
            )

        # Build filter based on hierarchy
        filter_desc = f"app_id: {request.app_id}"
        must_conditions = [
            models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id))
        ]
        
        if request.project_id:
            filter_desc += f", project_id: {request.project_id}"
            must_conditions.append(
                models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id))
            )
        
        if request.ticket_id:
            filter_desc += f", ticket_id: {request.ticket_id}"
            must_conditions.append(
                models.FieldCondition(key="ticket_id", match=models.MatchValue(value=request.ticket_id))
            )
        
        print(f"INFO: Retrieving all memories for {filter_desc}")
        
        qdrant_filter = models.Filter(must=must_conditions)
        
        try:
            # Scroll through all matching points
            all_points = []
            offset = None
            batch_size = 100
            
            while True:
                result = config.qdrant_client.scroll(
                    collection_name=QDRANT_COLLECTION_NAME,
                    scroll_filter=qdrant_filter,
                    limit=batch_size,
                    offset=offset,
                    with_payload=True,
                    with_vectors=False
                )
                
                points, next_offset = result
                all_points.extend(points)
                
                if next_offset is None or len(points) < batch_size:
                    break
                    
                offset = next_offset
            
            print(f"INFO: Found {len(all_points)} total memory chunks for {filter_desc}")
            
        except Exception as e:
            print(f"ERROR: Qdrant scroll failed: {e}")
            raise ValidationError(status_code=500, detail=f"Qdrant retrieval failed: {str(e)}")
        
        # Convert to RetrievedChunk format
        retrieved_chunks: List[RetrievedChunk] = []
        for point in all_points:
            chunk_content = point.payload.get("text_chunk", "")
            metadata_from_payload = {k: v for k, v in point.payload.items() if k != "text_chunk"}
            
            retrieved_chunks.append(RetrievedChunk(
                chunk_id=str(point.id),
                text_chunk=chunk_content,
                metadata=metadata_from_payload,
                score=1.0  # No similarity score needed for direct retrieval
            ))
        
        # Version-aware deduplication - prefer highest version within each logical memory group
        memory_groups = defaultdict(list)
        for chunk in retrieved_chunks:
            # Create a key that uniquely identifies a logical memory
            app_id = chunk.metadata.get('app_id', '')
            project_id = chunk.metadata.get('project_id', '') or 'none'
            ticket_id = chunk.metadata.get('ticket_id', '') or 'none'
            memory_type = chunk.metadata.get('type', '') or 'none'
            
            memory_key = f"{app_id}|{project_id}|{ticket_id}|{memory_type}"
            memory_groups[memory_key].append(chunk)
        
        # Within each group, prefer chunks from the highest version
        version_filtered_chunks = []
        for memory_key, chunks_in_group in memory_groups.items():
            if len(chunks_in_group) == 1:
                version_filtered_chunks.extend(chunks_in_group)
            else:
                # Find the highest version in this group
                max_version = max(safe_int_conversion(chunk.metadata.get('version', 1)) for chunk in chunks_in_group)
                highest_version_chunks = [chunk for chunk in chunks_in_group 
                                        if safe_int_conversion(chunk.metadata.get('version', 1)) == max_version]
                version_filtered_chunks.extend(highest_version_chunks)
                
                print(f"INFO: Version deduplication for {memory_key}: {len(chunks_in_group)} chunks reduced to {len(highest_version_chunks)} (version {max_version})")
        
        retrieved_chunks = version_filtered_chunks
        
        # Sort by timestamp or keep original order
        if request.sort_by == "timestamp" and retrieved_chunks:
            # Sort by timestamp_iso if available
            retrieved_chunks.sort(
                key=lambda x: x.metadata.get('timestamp_iso', ''), 
                reverse=True  # Most recent first
            )
        
        # Apply limit
        retrieved_chunks = retrieved_chunks[:request.limit]
        
        # Optional: Synthesize a summary of all memories
        synthesized_summary = None
        if ENABLE_GEMMA_SUMMARIZATION and retrieved_chunks:
            try:
                # Create a context-aware prompt for summarization
                context_prompt = f"Summarize all memories for {filter_desc}"
                summary = await synthesize_search_results(
                    context_prompt, 
                    retrieved_chunks[:MAX_SUMMARIZATION_CHUNKS], 
                    config.http_client, 
                    config
                )
                if summary:
                    print("INFO: LM Studio summary generated successfully for project memories.")
                    synthesized_summary = summary
            except Exception as e:
                print(f"WARN: Project memories summarization failed: {e}. Returning raw chunks.")
        
        return SearchResponse(
            synthesized_summary=synthesized_summary,
            retrieved_chunks=retrieved_chunks,
            total_results=len(retrieved_chunks)
        )
        
    except ValidationError:
        raise
    except Exception as e:
        print(f"ERROR: Unexpected error in get_project_memories: {e}")
        raise ValidationError(
            status_code=500, 
            detail=f"Internal server error during retrieval: {str(e)}"
        )

async def update_memory(request: UpdateMemoryRequest, config: AppConfig):
    """
    Updates an existing memory by finding it based on app_id/project_id/ticket_id/type combination,
    then replacing its content and incrementing the version.
    """
    try:
        # Validate input
        if not request.app_id:
            raise ValidationError(
                status_code=400, 
                detail="app_id is required"
            )
        
        # Build filter to find the memory to update
        filter_conditions = [
            models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id))
        ]
        
        if request.project_id:
            filter_conditions.append(
                models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id))
            )
        
        if request.ticket_id:
            filter_conditions.append(
                models.FieldCondition(key="ticket_id", match=models.MatchValue(value=request.ticket_id))
            )
            
        if request.memory_type:
            filter_conditions.append(
                models.FieldCondition(key="type", match=models.MatchValue(value=request.memory_type))
            )
        
        qdrant_filter = models.Filter(must=filter_conditions)
        
        # Find existing memory chunks
        existing_points = []
        offset = None
        
        while True:
            result = config.qdrant_client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                scroll_filter=qdrant_filter,
                limit=100,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )
            
            points, next_offset = result
            existing_points.extend(points)
            
            if next_offset is None or len(points) < 100:
                break
            offset = next_offset
        
        if not existing_points:
            raise ValidationError(
                status_code=404,
                detail="No memory found matching the specified criteria"
            )
        
        # Group by original_content_hash to find unique memories
        memory_groups = defaultdict(list)
        for point in existing_points:
            content_hash = point.payload.get("original_content_hash", "unknown")
            memory_groups[content_hash].append(point)
        
        # Find the latest version
        max_version = 0
        for points in memory_groups.values():
            for point in points:
                version = safe_int_conversion(point.payload.get("version", 1))
                max_version = max(max_version, version)
        
        # Prepare new version
        new_version = max_version + 1
        
        # Delete old chunks
        point_ids_to_delete = [point.id for point in existing_points]
        config.qdrant_client.delete(
            collection_name=QDRANT_COLLECTION_NAME,
            points_selector=models.PointIdsList(points=point_ids_to_delete)
        )
        
        # Create new memory with updated content
        new_metadata = {
            "app_id": request.app_id,
            "version": new_version,
            "timestamp_iso": datetime.utcnow().isoformat() + "Z"
        }
        
        # Add optional fields if provided
        if request.project_id:
            new_metadata["project_id"] = request.project_id
        if request.ticket_id:
            new_metadata["ticket_id"] = request.ticket_id
        if request.memory_type:
            new_metadata["type"] = request.memory_type
            
        # Apply any additional metadata updates
        new_metadata.update(request.metadata_updates)
        
        # Create new memory item and add it
        memory_item = MemoryItemIn(
            content=request.new_content,
            metadata=new_metadata
        )
        
        add_result = await add_memory(memory_item, config)
        
        return {
            "message": f"Memory updated successfully to version {new_version}",
            "previous_version": max_version,
            "new_version": new_version,
            "chunks_replaced": len(existing_points),
            "chunks_stored": add_result.chunks_stored,
            "original_content_hash": add_result.original_content_hash
        }
        
    except ValidationError:
        raise
    except Exception as e:
        print(f"ERROR: Unexpected error in update_memory: {e}")
        raise ValidationError(
            status_code=500,
            detail=f"Internal server error during update: {str(e)}"
        )

async def get_recent_memories(request: GetRecentMemoriesRequest, config: AppConfig):
    """
    Retrieves memories from the last N hours, optionally filtered by app_id/project_id.
    Perfect for agents resuming work after a break.
    """
    try:
        # Calculate timestamp cutoff
        cutoff_time = datetime.utcnow() - timedelta(hours=request.hours)
        cutoff_iso = cutoff_time.isoformat() + "Z"
        
        # Build filter conditions
        filter_conditions = []
        
        # Add app_id filter if specified
        if request.app_id:
            filter_conditions.append(
                models.FieldCondition(key="app_id", match=models.MatchValue(value=request.app_id))
            )
        
        # Add project_id filter if specified
        if request.project_id:
            filter_conditions.append(
                models.FieldCondition(key="project_id", match=models.MatchValue(value=request.project_id))
            )
        
        # Note: Qdrant doesn't support direct date range filtering in the same way as other DBs
        # We'll need to fetch all matching records and filter by timestamp in memory
        qdrant_filter = models.Filter(must=filter_conditions) if filter_conditions else None
        
        # Scroll through all matching points
        all_points = []
        offset = None
        batch_size = 100
        
        while True:
            result = config.qdrant_client.scroll(
                collection_name=QDRANT_COLLECTION_NAME,
                scroll_filter=qdrant_filter,
                limit=batch_size,
                offset=offset,
                with_payload=True,
                with_vectors=False
            )
            
            points, next_offset = result
            
            # Filter by timestamp
            for point in points:
                timestamp_iso = point.payload.get("timestamp_iso", "")
                if timestamp_iso and timestamp_iso >= cutoff_iso:
                    all_points.append(point)
            
            if next_offset is None or len(points) < batch_size:
                break
                
            offset = next_offset
        
        print(f"INFO: Found {len(all_points)} recent memory chunks from the last {request.hours} hours")
        
        # Convert to RetrievedChunk format
        retrieved_chunks: List[RetrievedChunk] = []
        for point in all_points:
            chunk_content = point.payload.get("text_chunk", "")
            metadata_from_payload = {k: v for k, v in point.payload.items() if k != "text_chunk"}
            
            retrieved_chunks.append(RetrievedChunk(
                chunk_id=str(point.id),
                text_chunk=chunk_content,
                metadata=metadata_from_payload,
                score=1.0  # No similarity score for time-based retrieval
            ))
        
        # Apply version deduplication
        memory_groups = defaultdict(list)
        for chunk in retrieved_chunks:
            app_id = chunk.metadata.get('app_id', '')
            project_id = chunk.metadata.get('project_id', '') or 'none'
            ticket_id = chunk.metadata.get('ticket_id', '') or 'none'
            memory_type = chunk.metadata.get('type', '') or 'none'
            
            memory_key = f"{app_id}|{project_id}|{ticket_id}|{memory_type}"
            memory_groups[memory_key].append(chunk)
        
        # Keep only highest version per group
        version_filtered_chunks = []
        for memory_key, chunks_in_group in memory_groups.items():
            if len(chunks_in_group) == 1:
                version_filtered_chunks.extend(chunks_in_group)
            else:
                max_version = max(safe_int_conversion(chunk.metadata.get('version', 1)) for chunk in chunks_in_group)
                highest_version_chunks = [chunk for chunk in chunks_in_group 
                                        if safe_int_conversion(chunk.metadata.get('version', 1)) == max_version]
                version_filtered_chunks.extend(highest_version_chunks)
        
        retrieved_chunks = version_filtered_chunks
        
        # Sort by timestamp (most recent first)
        retrieved_chunks.sort(
            key=lambda x: x.metadata.get('timestamp_iso', ''), 
            reverse=True
        )
        
        # Apply limit
        retrieved_chunks = retrieved_chunks[:request.limit]
        
        # Generate summary if requested
        synthesized_summary = None
        if request.include_summary and ENABLE_GEMMA_SUMMARIZATION and retrieved_chunks:
            try:
                context_prompt = f"Summarize the recent activities and updates from the last {request.hours} hours"
                summary = await synthesize_search_results(
                    context_prompt, 
                    retrieved_chunks[:MAX_SUMMARIZATION_CHUNKS], 
                    config.http_client, 
                    config
                )
                if summary:
                    synthesized_summary = summary
            except Exception as e:
                print(f"WARN: Recent memories summarization failed: {e}")
        
        return SearchResponse(
            synthesized_summary=synthesized_summary,
            retrieved_chunks=retrieved_chunks,
            total_results=len(retrieved_chunks)
        )
        
    except Exception as e:
        print(f"ERROR: Unexpected error in get_recent_memories: {e}")
        raise ValidationError(
            status_code=500,
            detail=f"Internal server error during retrieval: {str(e)}"
        ) 