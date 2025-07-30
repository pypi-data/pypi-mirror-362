"""
MCP Server implementation using stdio transport for ZenCoder compatibility
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.lowlevel import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import (
    Tool, 
    TextContent,
    ImageContent,
    EmbeddedResource,
    CallToolRequest
)

# Import our core functionality
from .core.models import MemoryItemIn, MemorySearchRequest
from .core.handlers.memory_handlers import add_memory as add_memory_handler, search_memories as search_memories_handler
from .core.handlers.list_handlers import (
    list_app_ids as list_app_ids_handler,
    list_project_ids as list_project_ids_handler, 
    list_ticket_ids as list_ticket_ids_handler
)
from .core.handlers.health_handlers import health_check as health_check_handler
from .core.services import startup_event, shutdown_event, AppConfig
from .core.utils.dependencies import get_http_client
import httpx

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MemoryHubMCPServer:
    """Memory Hub MCP Server for stdio transport"""
    
    def __init__(self, config: AppConfig):
        self.server = Server("memory-hub")
        self.config = config
        self._setup_tools()
    
    def _setup_tools(self):
        """Register MCP tools"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available tools"""
            return [
                Tool(
                    name="add_memory",
                    description="Adds memory content. Chunks content, gets embeddings, and stores in Qdrant. Supports flexible hierarchy: app_id (required), project_id (optional), ticket_id (optional).",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "The content to store in memory"
                            },
                            "metadata": {
                                "type": "object",
                                "description": "Metadata with flexible hierarchy: app_id (required), project_id (optional), ticket_id (optional), type, etc.",
                                "properties": {
                                    "app_id": {"type": "string", "description": "Required - Application identifier"},
                                    "project_id": {"type": "string", "description": "Optional - Project identifier"},
                                    "ticket_id": {"type": "string", "description": "Optional - Ticket identifier"}, 
                                    "type": {"type": "string", "description": "Memory type classification"},
                                    "version": {"type": "integer", "description": "Version number", "default": 1}
                                },
                                "required": ["app_id"]
                            }
                        },
                        "required": ["content", "metadata"]
                    }
                ),
                Tool(
                    name="search_memories",
                    description="Searches memories in Qdrant with keyword-enhanced querying, then uses LM Studio to synthesize results.",
                    inputSchema={
                        "type": "object", 
                        "properties": {
                            "query_text": {
                                "type": "string",
                                "description": "The query text to search for"
                            },
                            "metadata_filters": {
                                "type": "object",
                                "description": "Metadata filters for search",
                                "additionalProperties": {"type": "string"},
                                "default": {}
                            },
                            "keyword_filters": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of keywords that results must contain",
                                "default": []
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results to return",
                                "default": 10
                            }
                        },
                        "required": ["query_text"]
                    }
                ),
                Tool(
                    name="list_app_ids",
                    description="Lists all unique app_ids found in the Memory Hub",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                Tool(
                    name="list_project_ids", 
                    description="Lists all unique project_ids found in the Memory Hub",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                Tool(
                    name="list_ticket_ids",
                    description="Lists all unique ticket_ids found in the Memory Hub", 
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                ),
                Tool(
                    name="health_check",
                    description="Health check endpoint to verify server status",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "additionalProperties": False
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent | ImageContent | EmbeddedResource]:
            """Handle tool calls"""
            try:
                if name == "add_memory":
                    # Convert arguments to MemoryItemIn
                    memory_item = MemoryItemIn(
                        content=arguments["content"],
                        metadata=arguments["metadata"]
                    )
                    result = await add_memory_handler(memory_item, self.config)
                    return [TextContent(
                        type="text",
                        text=f"Memory added successfully: {result.message} ({result.chunks_stored} chunks stored)"
                    )]
                
                elif name == "search_memories":
                    # Convert arguments to MemorySearchRequest  
                    search_request = MemorySearchRequest(
                        query_text=arguments["query_text"],
                        metadata_filters=arguments.get("metadata_filters", {}),
                        keyword_filters=arguments.get("keyword_filters", []),
                        limit=arguments.get("limit", 10)
                    )
                    result = await search_memories_handler(search_request, self.config)
                    
                    # Format response
                    if result.synthesized_summary:
                        response_text = f"## Search Results Summary\n\n{result.synthesized_summary}\n\n"
                    else:
                        response_text = f"## Search Results ({result.total_results} found)\n\n"
                    
                    for i, chunk in enumerate(result.retrieved_chunks[:5], 1):
                        response_text += f"### Result {i} (Score: {chunk.score:.3f})\n"
                        response_text += f"**Metadata:** {chunk.metadata}\n\n"
                        response_text += f"{chunk.text_chunk}\n\n---\n\n"
                    
                    return [TextContent(type="text", text=response_text)]
                
                elif name == "list_app_ids":
                    result = await list_app_ids_handler(self.config)
                    return [TextContent(
                        type="text", 
                        text=f"Found {result.total_count} app_ids: {', '.join(result.ids)}"
                    )]
                
                elif name == "list_project_ids":
                    result = await list_project_ids_handler(self.config)
                    return [TextContent(
                        type="text",
                        text=f"Found {result.total_count} project_ids: {', '.join(result.ids)}"
                    )]
                
                elif name == "list_ticket_ids":
                    result = await list_ticket_ids_handler(self.config)
                    return [TextContent(
                        type="text",
                        text=f"Found {result.total_count} ticket_ids: {', '.join(result.ids)}"
                    )]
                
                elif name == "health_check":
                    result = await health_check_handler(self.config)
                    return [TextContent(
                        type="text",
                        text=f"Health check passed: {result['status']}"
                    )]
                
                else:
                    raise ValueError(f"Unknown tool: {name}")
                    
            except Exception as e:
                logger.error(f"Error calling tool {name}: {e}")
                return [TextContent(
                    type="text",
                    text=f"Error executing {name}: {str(e)}"
                )]
    
    async def run(self):
        """Run the MCP server with stdio transport"""
        try:
            # Initialize core services
            await startup_event(self.config)
            logger.info("Memory Hub core services initialized")
            
            # Initialize HTTP client for internal operations
            self.config.http_client = httpx.AsyncClient()
            
            # Import and run stdio server
            from mcp.server.stdio import stdio_server
            
            async with stdio_server() as (read_stream, write_stream):
                logger.info("Memory Hub MCP Server starting with stdio transport")
                await self.server.run(
                    read_stream, 
                    write_stream,
                    InitializationOptions(
                        server_name="memory-hub",
                        server_version="0.1.0",
                        capabilities=self.server.get_capabilities(
                            notification_options=NotificationOptions(),
                            experimental_capabilities={}
                        )
                    )
                )
        except Exception as e:
            logger.error(f"Error running MCP server: {e}")
            raise
        finally:
            await shutdown_event(self.config)
            logger.info("Shutdown complete.")

def create_server(config: AppConfig) -> MemoryHubMCPServer:
    """Create an instance of the Memory Hub MCP Server"""
    return MemoryHubMCPServer(config) 