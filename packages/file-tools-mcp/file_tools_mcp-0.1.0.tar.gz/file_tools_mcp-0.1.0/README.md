# File Tools MCP Server

An MCP (Model Context Protocol) server that provides file and directory tools for LLMs, with built-in support for respecting `.gitignore` patterns.

## Features

### Tools
- **project_structure**: Generates a tree view of directory structures while respecting `.gitignore` patterns
- **read_multiple_files**: Reads multiple files in a single request with clear content separation

### Resources
- **project://info**: Comprehensive project information (type, dependencies, scripts, git status)
- **git://status**: Detailed git repository status with file changes and recent commits
- **dependencies://list**: Lists all project dependencies by package manager
- **config://list**: Finds and lists all configuration files in the project
- **files://recent**: Shows the 20 most recently modified files
- **context://full**: Complete project context with directory structure and all text files under 50KB

### Additional Features
- Handles circular symlinks and permission errors gracefully
- Supports depth limiting and hidden file visibility options
- Clear error messages with helpful context for path issues

## Installation

### For Claude Desktop

1. Install the server to Claude Desktop:
   ```bash
   uv run mcp install main.py --name "File Tools"
   ```

2. Restart Claude Desktop

### For Development

1. Clone the repository
2. Install dependencies:
   ```bash
   uv sync
   ```

## Usage

### Development Mode (with Inspector)
```bash
uv run mcp dev main.py
```
This opens the MCP Inspector for debugging and testing.

### Standalone Mode
```bash
uv run python main.py
```
Runs the server in stdio mode, waiting for MCP client connections.

### Testing
```bash
uv run python test_client.py
```
Runs a test client to verify server functionality.

## Available Tools

### project_structure

Generates a tree view of a directory structure while respecting `.gitignore` patterns.

**Parameters:**
- `path` (str, optional): Directory path to analyze (default: current working directory)
- `max_depth` (int, optional): Maximum depth to traverse (default: None for unlimited)
- `show_hidden` (bool, optional): Include hidden files and directories (default: False)

**Example:**
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

Reads multiple files and returns their contents in a single response.

**Parameters:**
- `paths` (list[str], required): List of file paths to read

**Features:**
- Clear separation between files with headers showing path and size
- Graceful error handling for missing or inaccessible files
- Efficient for reading multiple files in one request

**Example:**
```python
# Read multiple files
result = await session.call_tool("read_multiple_files", {
    "paths": [
        "src/main.py",
        "config.json",
        "README.md"
    ]
})
```

## Available Resources

### project://info
Provides comprehensive project information in one request:
- Project type detection (Node.js, Python, Rust, etc.)
- Package metadata (name, version, description)
- Available scripts/commands
- Dependency counts
- Git status summary
- Recent commits

### git://status
Detailed git repository status:
- Current branch and tracking information
- Ahead/behind status with remote
- Staged, modified, and untracked files
- Last 10 commits

### dependencies://list
Lists all project dependencies:
- Supports npm, yarn, pnpm, pip, poetry, uv
- Shows production and development dependencies
- Handles multiple package manager formats

### config://list
Finds all configuration files:
- Environment files (.env)
- Language configs (tsconfig.json, pyproject.toml)
- Linters and formatters
- CI/CD configurations
- Editor settings

### files://recent
Shows recently modified files:
- 20 most recently modified files
- File modification timestamps
- File sizes
- Excludes common ignore patterns

### context://full
Complete project context in one request:
- Full directory structure
- Contents of all text files under 50KB
- Respects .gitignore patterns
- Skips binary files automatically
- Provides summary of files included/skipped
- Perfect for giving LLMs complete project understanding

## Configuration

### Root Paths

When using the MCP Inspector or other MCP clients, you may need to configure root paths to allow the server to access your project directories. This is a security feature that prevents unauthorized file access.

In the MCP Inspector:
1. Click on the server configuration
2. Add root paths for directories you want to access
3. Example: `/home/user/projects/my-project`

Without proper root paths configured, you may see "File not found" errors even for files that exist.

## Security Considerations

When deploying this server:
- Bind to localhost (127.0.0.1) only for local deployments
- Use proper authentication if exposing to network
- Consider path traversal risks - the server allows reading any accessible directory
- Configure root paths to limit file access to specific directories

## License

MIT