# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Memory Hub MCP Server is a local memory system for AI agents using the Model Context Protocol (MCP). It provides vector-based storage and retrieval through stdio transport, specifically designed for ZenCoder and other MCP clients.

## Essential Commands

### Development Setup
```bash
# Setup development environment
uv venv
source .venv/bin/activate
uv pip install -e .

# Install with dev dependencies
uv pip install -e ".[dev]"
```

### Running the Server
```bash
# Run with default settings
memory-hub-mcp

# Run with custom configuration
memory-hub-mcp --log-level DEBUG --qdrant-url http://localhost:6333 --lm-studio-url http://localhost:1234/v1

# Run with UVX (recommended for distribution)
uvx memory-hub-mcp
```

### Development and Testing
```bash
# Code formatting and linting
black src/
ruff check src/

# Build distribution
uv build

# Publish to PyPI (requires token)
UV_PUBLISH_TOKEN=<token> uv publish dist/*
```

### Docker Environment
```bash
# Start Qdrant dependency
docker-compose up -d

# Development with hot reload
docker-compose -f docker-compose.dev.yml up
```

## Architecture

### Core Components

1. **MCP Server** (`src/memory_hub/mcp_server.py`): Main server implementation using stdio transport
2. **CLI Interface** (`src/memory_hub/cli.py`): Command-line entry point with argument parsing
3. **Core Services** (`src/memory_hub/core/services.py`): Handles Qdrant client and LM Studio integration
4. **Handlers** (`src/memory_hub/core/handlers/`): MCP tool implementations
5. **Models** (`src/memory_hub/core/models.py`): Pydantic data models

### Key Design Patterns

- **stdio transport**: Direct MCP protocol communication (no HTTP)
- **Hierarchical memory**: Flexible app_id → project_id → ticket_id organization
- **Hybrid search**: Vector similarity + keyword matching + LLM synthesis
- **Async-first**: All operations use async/await patterns

### External Dependencies

- **Qdrant**: Vector database for embeddings storage
- **LM Studio**: Provides embeddings and chat completions
- **MCP Protocol**: stdio transport for client communication

## MCP Tools Available

1. **add_memory**: Store content with hierarchical metadata
2. **search_memories**: Semantic search with keyword enhancement
3. **get_project_memories**: Retrieve ALL memories for a specific app_id/project_id without search queries
4. **update_memory**: Update existing memories with automatic version incrementing
5. **get_recent_memories**: Retrieve memories from the last N hours (perfect for resuming work)
6. **list_app_ids**: List all application identifiers
7. **list_project_ids**: List all project identifiers
8. **list_ticket_ids**: List all ticket identifiers
9. **list_memory_types**: List memory types currently in use (with counts and metadata)
10. **get_memory_type_guide**: Get the recommended memory type conventions
11. **health_check**: Server health verification

## Configuration

### Environment Variables
- `QDRANT_URL`: Qdrant server URL (default: http://localhost:6333)
- `LM_STUDIO_BASE_URL`: LM Studio base URL (default: http://localhost:1234/v1)
- `MIN_SCORE_THRESHOLD`: Minimum similarity score for results (default: 0.60)
- `ENABLE_GEMMA_SUMMARIZATION`: Enable LLM summarization (default: true)

### CLI Arguments
- `--qdrant-url`: Override Qdrant URL
- `--lm-studio-url`: Override LM Studio URL  
- `--log-level`: Set logging level (DEBUG, INFO, WARNING, ERROR)

## Development Notes

### Important File Locations
- `src/memory_hub/core/config.py`: Configuration constants and environment variables
- `src/memory_hub/core/chunking.py`: Semantic text chunking implementation
- `src/memory_hub/core/utils/search_utils.py`: Search enhancement utilities
- `pyproject.toml`: Package configuration and dependencies

### Testing Considerations
- No formal test suite currently exists
- Manual testing requires running Qdrant and LM Studio locally
- Debug script available: `debug_memory_hub.py`

### Version Management
- Version defined in `pyproject.toml`
- Must increment for PyPI publishing
- Semantic versioning: MAJOR.MINOR.PATCH

## Agent Usage Patterns

### For Agents Saving Progress
When an agent needs to save work progress:
```
1. Use add_memory with:
   - app_id: Your application/domain (e.g., "eatzos", "motiv")
   - project_id: Specific project/feature (e.g., "next", "enhanced-chat")
   - type: Type of memory (e.g., "progress", "code_changes", "decisions")
   - content: Detailed progress, decisions, code changes, etc.

2. For updates to existing memories:
   - Use update_memory to increment version automatically
   - Specify app_id, project_id, and optionally memory_type
   - Provide new_content with the updated information
```

### For Agents Resuming Work
When an agent needs to continue previous work:
```
1. Use get_project_memories to retrieve ALL context:
   - Specify app_id and project_id
   - No need to guess search terms!
   - Automatically gets latest versions

2. Use get_recent_memories to see what changed:
   - Optionally filter by app_id/project_id
   - Default: last 24 hours
   - Includes AI-generated summary

3. Use search_memories only when:
   - Looking for specific concepts across projects
   - Need keyword-enhanced semantic search
```

### Best Practices for Agent Continuity
1. **Consistent Naming**: Use consistent app_id and project_id across sessions
2. **Meaningful Types**: Use descriptive memory types (e.g., "api_design", "bug_fix", "feature_implementation")
3. **Regular Updates**: Update memories as work progresses, not just at the end
4. **Version Awareness**: The system handles versioning automatically - just update when needed

## Troubleshooting

### Common Issues
1. **Qdrant connection errors**: Verify Qdrant is running and accessible
2. **LM Studio timeout**: Check LM Studio is running with appropriate models loaded
3. **Context length errors**: Reduce chunk size or query complexity
4. **Import errors**: Ensure all dependencies installed with `uv pip install -e .`

### Debugging
- Use `--log-level DEBUG` for verbose output
- Check `docker-compose.yml` for service configuration
- Review error messages in stdio output