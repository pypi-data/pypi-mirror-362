# Memory Hub Agent Integration Guide

This guide helps AI agents effectively use Memory Hub as their "central brain" for preserving and retrieving context across sessions.

## Quick Start for Agents

### First Time Setup
When an agent starts working on a new project, establish your memory space:

```python
# Define your identity
app_id = "your_app_name"      # e.g., "eatzos", "motiv", "bedrock-agent"
project_id = "your_project"    # e.g., "next", "api-redesign", "chat-enhancement"

# Save initial context
add_memory(
    content="Starting work on [describe your task]...",
    metadata={
        "app_id": app_id,
        "project_id": project_id,
        "type": "initialization",
        "agent_name": "your_agent_identifier"  # optional but recommended
    }
)
```

### Saving Progress During Work

Save different types of memories as you work:

```python
# Save code changes
add_memory(
    content="Modified authentication.py to add refresh token support:\n```python\n[code]\n```",
    metadata={
        "app_id": "eatzos",
        "project_id": "next",
        "type": "code_changes",
        "files_modified": ["authentication.py", "token_manager.py"]
    }
)

# Save decisions
add_memory(
    content="Decided to use JWT tokens instead of sessions because...",
    metadata={
        "app_id": "eatzos",
        "project_id": "next", 
        "type": "technical_decision",
        "importance": "high"
    }
)

# Save progress summaries
add_memory(
    content="Completed 3/5 authentication endpoints. Remaining: password reset, 2FA",
    metadata={
        "app_id": "eatzos",
        "project_id": "next",
        "type": "progress_summary"
    }
)
```

### Creating vs Updating Memories

**Important**: Most memories should be CREATED (not updated) to preserve history!

#### When to CREATE New Memories (Default Approach)
Use `add_memory` for most things - each memory is a historical record:

```python
# Each code change is a new memory
add_memory(content="Added login endpoint", metadata={...,"type":"code_change"})
add_memory(content="Fixed login bug", metadata={...,"type":"code_change"})

# Each progress update is a new memory
add_memory(content="Completed login feature", metadata={...,"type":"progress_update"})
add_memory(content="Started working on registration", metadata={...,"type":"progress_update"})

# Each decision is a new memory
add_memory(content="Decided to use JWT tokens", metadata={...,"type":"decision"})
```

#### When to UPDATE Memories (Rare Cases)
Only update memories that are meant to be "living documents":

```python
# Update a single project status document
update_memory(
    app_id="eatzos",
    project_id="next",
    memory_type="project_status",  # Living document type
    new_content="Current Status: Auth 100% complete, API 60% complete"
)

# Update a todo list
update_memory(
    app_id="eatzos",
    project_id="next",
    memory_type="todo_list",  # Another living document
    new_content="Remaining: 1. Add email verification 2. Rate limiting"
)

# Correct an error in previous memory
update_memory(
    app_id="eatzos",
    project_id="next",
    memory_type="technical_stack",
    new_content="Using MySQL (not PostgreSQL as previously stated)"
)
```

### Resuming Work (Most Important!)

When returning to continue work:

```python
# STEP 1: Get all project context (no guessing needed!)
memories = get_project_memories(
    app_id="eatzos",
    project_id="next",
    limit=100  # Get comprehensive context
)

# STEP 2: Check recent changes
recent = get_recent_memories(
    app_id="eatzos",
    project_id="next",
    hours=48,  # Last 2 days
    include_summary=True
)

# STEP 3: Search for specific topics only if needed
results = search_memories(
    query_text="authentication endpoints",
    metadata_filters={
        "app_id": "eatzos",
        "project_id": "next"
    }
)
```

## Memory Types Reference

Use consistent memory types for better organization:

| Type | Usage | Purpose | Example Content |
|------|-------|---------|-----------------|
| `initialization` | CREATE | Project setup and initial context | Project goals, tech stack, constraints |
| `code_change` | CREATE | Actual code modifications | File changes, new implementations |
| `decision` | CREATE | Architecture and design choices | Why certain approaches were chosen |
| `progress_update` | CREATE | Progress milestones | What was completed when |
| `bug_fix` | CREATE | Issues found and resolved | Problem description and solution |
| `research_finding` | CREATE | Information gathered | API docs, best practices found |
| `test_result` | CREATE | Testing outcomes | Test failures, coverage reports |
| **`project_status`** | **UPDATE** | Single living status doc | Current overall state |
| **`todo_list`** | **UPDATE** | Evolving task list | What needs to be done |
| **`configuration`** | **UPDATE** | Current config state | Active settings/config |
| **`team_notes`** | **UPDATE** | Shared understanding | Key points to remember |

**Rule of thumb**: If the memory type is plural or implies history (like "changes", "updates", "fixes"), CREATE new memories. If it's singular and represents current state (like "status", "configuration"), UPDATE it.

## Best Practices

### 1. Consistent Naming
- Always use the same `app_id` for a given application
- Keep `project_id` consistent across sessions
- Use standard `type` values from the table above

### 2. Rich Content
- Include code snippets with proper markdown formatting
- Add file paths and line numbers when referencing code
- Explain the "why" not just the "what"

### 3. Regular Updates
- Save progress after completing each significant task
- Update existing memories instead of creating duplicates
- Use `update_memory` when information changes

### 4. Effective Retrieval
- Start with `get_project_memories` to get full context
- Use `get_recent_memories` to catch up on changes
- Only use `search_memories` for specific concept searches

### 5. Metadata Usage
- Add `importance: "high"` for critical decisions
- Include `files_modified` for code changes
- Add `agent_name` to track which agent made changes

## Common Patterns

### Pattern 1: Daily Standup
```python
# At start of session
recent = get_recent_memories(hours=24, include_summary=True)
# Review what was done yesterday

# At end of session
add_memory(
    content="Today's progress: [summary]",
    metadata={
        "app_id": app_id,
        "project_id": project_id,
        "type": "progress_summary",
        "date": datetime.now().isoformat()
    }
)
```

### Pattern 2: Feature Implementation
```python
# Start feature
add_memory(content="Starting implementation of [feature]", 
          metadata={...,"type": "initialization"})

# During development
add_memory(content="[code changes]", 
          metadata={...,"type": "code_changes"})

# Complete feature
update_memory(memory_type="progress_summary",
             new_content="Feature [X] completed and tested")
```

### Pattern 3: Debugging Session
```python
# Document the issue
add_memory(content="Bug: [description]", 
          metadata={...,"type": "bug_fix", "status": "investigating"})

# Document the fix
update_memory(memory_type="bug_fix",
             new_content="Bug fixed: [solution]",
             metadata_updates={"status": "resolved"})
```

## Troubleshooting

### "No memory found" on update
- Check exact spelling of app_id, project_id, and memory_type
- Verify the memory exists with `get_project_memories` first

### Getting too many results
- Use more specific memory types
- Set appropriate limits
- Filter by time with `get_recent_memories`

### Lost context between sessions
- Always use `get_project_memories` first (not search!)
- Check if memories were saved with correct app_id/project_id
- Verify Memory Hub server is using the same Qdrant instance

## Integration Example

Here's a complete example of an agent work session:

```python
# Beginning of session - Resume context
print("Resuming work on eatzos/next project...")

# Get all context
all_memories = get_project_memories(
    app_id="eatzos",
    project_id="next"
)

# Check recent changes
recent = get_recent_memories(
    app_id="eatzos",
    hours=24,
    include_summary=True
)

print(f"Found {len(all_memories)} total memories")
print(f"Recent summary: {recent.summary}")

# Do work...
# [Agent performs tasks]

# Save progress
add_memory(
    content="Implemented password reset endpoint with email verification",
    metadata={
        "app_id": "eatzos",
        "project_id": "next",
        "type": "code_changes",
        "files_modified": ["auth/password_reset.py", "email/templates.py"]
    }
)

# Update overall progress
update_memory(
    app_id="eatzos",
    project_id="next",
    memory_type="progress_summary",
    new_content="Authentication module 90% complete. Only 2FA setup remaining."
)

print("Progress saved to Memory Hub!")
```

Remember: Memory Hub is your persistent brain across sessions. Use it liberally and consistently!