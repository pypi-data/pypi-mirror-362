# CLAUDE.md

please follow the coding guidance mentioned in ~/.claude/docs/writing-code.md
Follow additional guidance mentioned in ~/.claude/docs/python.md & ~/.claude/docs/using-uv.md

Use the available MCP tools for searching up the latest documentation on MCP server implementation and follow the best practices outlined there. We will be using the official python-sdk for MCP servers. Use context7 mcp server to get the latest documentation and examples when implementing the server.

## Project Overview
This is an MCP (Model Context Protocol) server implementation for file tools. The goal is provide tools to LLMs and coding agents to quickly get context of a project by getting project structure and contents of multiple files in a single request.

## Available Tools

### project_structure
Generates a tree view of a directory structure while respecting `.gitignore` patterns.

**Parameters:**
- `path` (str, optional): Directory path to analyze (default: current working directory)
- `max_depth` (int, optional): Maximum depth to traverse (default: None for unlimited)
- `show_hidden` (bool, optional): Include hidden files and directories (default: False)

**Example usage:**
```python
# Get structure of current directory
result = await session.call_tool("project_structure", {})

# Get structure with depth limit
result = await session.call_tool("project_structure", {
    "path": "/path/to/project",
    "max_depth": 3
})

# Include hidden files
result = await session.call_tool("project_structure", {
    "show_hidden": True
})
```

### read_multiple_files
Reads multiple files and returns their contents in a single response with clear separation.

**Parameters:**
- `paths` (list[str], required): List of file paths to read (absolute or relative paths)

**Features:**
- Each file's content is clearly separated with headers showing the file path and size
- Handles errors gracefully (file not found, permission denied, binary files)
- Returns all results in a single response for efficient LLM processing

**Example usage:**
```python
# Read multiple files at once
result = await session.call_tool("read_multiple_files", {
    "paths": [
        "src/main.py",
        "src/config.py",
        "README.md"
    ]
})

# Mix of existing and non-existing files
result = await session.call_tool("read_multiple_files", {
    "paths": [
        "main.py",
        "non_existent.txt"  # Will show error in output
    ]
})
```

## Running the Server

### Development Mode
```bash
# Run with MCP inspector
uv run mcp dev main.py

# Or run directly
uv run python main.py
```

### Install to Claude Desktop
```bash
uv run mcp install main.py
```

## Available Resources

### project://info
Quick project overview combining package info, git status, and available scripts.

### git://status  
Detailed git status with file changes, branch info, and recent commits.

### dependencies://list
All project dependencies based on detected package manager.

### config://list
Lists all configuration files organized by category.

### files://recent
Shows 20 most recently modified files with timestamps.

### context://full
Complete project snapshot: directory tree + all text files under 50KB. Perfect for giving full context to LLMs.

## Architecture

### Key Components
- `src/server.py`: FastMCP server implementation with tools and resources
  - Tools: `project_structure`, `read_multiple_files`
  - Resources: Project info, git status, dependencies, config files, recent files
- `src/tree_generator.py`: Core logic for generating directory trees with gitignore support
  - Uses `pathspec` library for accurate gitignore pattern matching
  - Handles circular symlinks and permission errors gracefully
  - Provides formatted output similar to Unix `tree` command

### Design Decisions
- Uses `pathspec.GitIgnoreSpec` for exact gitignore behavior matching
- Separates tree generation logic for potential reuse in other tools
- Returns formatted string output for easy reading by LLMs
- Includes file/directory count statistics in output
- Resources provide quick read-only access to project context
- Tools allow for more complex operations with parameters

# Working style 
- Work in parallel whenever possible.
- Use the task tool to run multiple tasks in parallel. 

### Dependency Management
```bash
# Install dependencies
uv sync

# Add a new dependency
uv add <package-name>

# Add a development dependency
uv add --dev <package-name>

# Update lock file
uv pip compile
```

### Environment Setup
- Python version: 3.12 (specified in `.python-version`)
- Package manager: uv (v0.7.20)

