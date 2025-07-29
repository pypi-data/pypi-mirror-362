# ABOUTME: MCP server implementation for file tools
# Provides tools for LLMs to understand project structure

from mcp.server.fastmcp import FastMCP
from pathlib import Path
from typing import Optional
import sys
import os
import json
import subprocess
from datetime import datetime

# Add the parent directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.tree_generator import generate_directory_tree

# Create MCP server instance
mcp = FastMCP("file-tools")


@mcp.tool()
def read_multiple_files(
    paths: list[str]
) -> str:
    """
    Read multiple files and return their contents in a single response.
    
    Each file's content is clearly separated with a header showing its path.
    Failed reads (e.g., file not found, permission denied) are reported in the output.
    
    Args:
        paths: List of file paths to read (absolute or relative paths)
    
    Returns:
        Combined content of all files with clear separators
    """
    if not paths:
        return "No file paths provided"
    
    results = []
    separator = "=" * 80
    
    # Get current working directory for helpful error messages
    cwd = os.getcwd()
    
    for file_path in paths:
        try:
            path_obj = Path(file_path).resolve()
            
            # Check if file exists first to provide better error message
            if not path_obj.exists():
                # Provide helpful context about paths
                relative_path = Path(file_path)
                expected_absolute = Path(cwd) / relative_path
                
                error_msg = f"""
{separator}
File: {file_path}
Error: File not found

Attempted to read: {path_obj}
Current working directory: {cwd}

If using relative paths, the file would be expected at: {expected_absolute}

Note: When using MCP servers, you may need to:
1. Use absolute paths, or
2. Configure root paths in your MCP client, or
3. Ensure the server is running in the expected directory
{separator}
""".strip()
                results.append(error_msg)
                continue
            
            # Read file content
            with open(path_obj, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get file info
            file_size = path_obj.stat().st_size
            
            # Format the file section
            file_section = f"""
{separator}
File: {path_obj}
Size: {file_size:,} bytes
{separator}

{content}
"""
            results.append(file_section.strip())
            
        except PermissionError:
            results.append(f"""
{separator}
File: {file_path}
Error: Permission denied
Attempted to read: {path_obj}
{separator}
""".strip())
            
        except UnicodeDecodeError:
            results.append(f"""
{separator}
File: {file_path}
Error: Unable to decode file (binary file or invalid encoding)
{separator}
""".strip())
            
        except Exception as e:
            results.append(f"""
{separator}
File: {file_path}
Error: {str(e)}
{separator}
""".strip())
    
    # Join all results with double newlines
    return "\n\n".join(results)


@mcp.tool()
def project_structure(
    path: str = ".",
    max_depth: Optional[int] = None,
    show_hidden: bool = False
) -> str:
    """
    Generate a tree view of the project directory structure.
    
    This tool displays the directory structure while respecting .gitignore patterns,
    helping LLMs quickly understand project organization.
    
    Args:
        path: Directory path to analyze (default: current working directory)
        max_depth: Maximum depth to traverse (default: None for unlimited)
        show_hidden: Include hidden files and directories (default: False)
    
    Returns:
        A formatted tree structure of the directory
    """
    try:
        # Convert to absolute path for clarity
        abs_path = Path(path).resolve()
        
        # Check if directory exists
        if not abs_path.exists():
            cwd = os.getcwd()
            relative_path = Path(path)
            expected_absolute = Path(cwd) / relative_path
            
            return f"""Error: Directory not found

Attempted to read: {abs_path}
Current working directory: {cwd}

If using relative paths, the directory would be expected at: {expected_absolute}

Note: When using MCP servers, you may need to:
1. Use absolute paths, or
2. Configure root paths in your MCP client, or
3. Ensure the server is running in the expected directory"""

        if not abs_path.is_dir():
            return f"Error: Path '{abs_path}' is not a directory"
        
        # Generate the tree
        tree = generate_directory_tree(
            path=str(abs_path),
            max_depth=max_depth,
            show_hidden=show_hidden
        )
        
        return tree
        
    except PermissionError:
        return f"Error: Permission denied accessing directory '{path}'"
    except Exception as e:
        return f"Error generating directory tree: {str(e)}\nPath attempted: {Path(path).resolve()}"


# Resources section
@mcp.resource("project://info")
def get_project_info() -> str:
    """
    Get comprehensive project information including package details,
    dependencies, available scripts, and git status.
    """
    info_parts = []
    cwd = os.getcwd()
    
    info_parts.append(f"Project Directory: {cwd}")
    info_parts.append("=" * 80)
    
    # Detect project type and get package info
    package_files = {
        "package.json": "Node.js/JavaScript",
        "pyproject.toml": "Python",
        "Cargo.toml": "Rust",
        "go.mod": "Go",
        "pom.xml": "Java (Maven)",
        "build.gradle": "Java (Gradle)",
    }
    
    project_type = None
    for file, ptype in package_files.items():
        if Path(file).exists():
            project_type = ptype
            info_parts.append(f"\nProject Type: {ptype}")
            
            # Read package file
            try:
                if file == "package.json":
                    with open(file, 'r') as f:
                        data = json.load(f)
                        info_parts.append(f"Name: {data.get('name', 'N/A')}")
                        info_parts.append(f"Version: {data.get('version', 'N/A')}")
                        info_parts.append(f"Description: {data.get('description', 'N/A')}")
                        
                        # Scripts
                        if 'scripts' in data:
                            info_parts.append("\nAvailable Scripts:")
                            for script, command in data['scripts'].items():
                                info_parts.append(f"  npm run {script}")
                                
                        # Dependencies count
                        deps = len(data.get('dependencies', {}))
                        dev_deps = len(data.get('devDependencies', {}))
                        info_parts.append(f"\nDependencies: {deps} production, {dev_deps} development")
                        
                elif file == "pyproject.toml":
                    with open(file, 'r') as f:
                        content = f.read()
                        # Basic parsing (could use tomli for proper parsing)
                        if '[project]' in content:
                            for line in content.split('\n'):
                                if line.startswith('name = '):
                                    info_parts.append(f"Name: {line.split('=')[1].strip().strip('\"')}")
                                elif line.startswith('version = '):
                                    info_parts.append(f"Version: {line.split('=')[1].strip().strip('\"')}")
                                elif line.startswith('description = '):
                                    info_parts.append(f"Description: {line.split('=')[1].strip().strip('\"')}")
                                    
                        # Scripts
                        if '[project.scripts]' in content:
                            info_parts.append("\nAvailable Scripts:")
                            in_scripts = False
                            for line in content.split('\n'):
                                if '[project.scripts]' in line:
                                    in_scripts = True
                                elif in_scripts and line.strip() and not line.startswith('['):
                                    if '=' in line:
                                        script = line.split('=')[0].strip()
                                        info_parts.append(f"  {script}")
                                elif in_scripts and line.startswith('['):
                                    break
                                    
            except Exception as e:
                info_parts.append(f"Error reading {file}: {str(e)}")
            break
    
    if not project_type:
        info_parts.append("\nProject Type: Unknown")
    
    # Git information
    info_parts.append("\n" + "=" * 80)
    info_parts.append("Git Information:")
    
    try:
        # Check if git repo
        subprocess.run(['git', 'rev-parse', '--git-dir'], 
                      capture_output=True, check=True, cwd=cwd)
        
        # Current branch
        branch = subprocess.run(['git', 'branch', '--show-current'], 
                               capture_output=True, text=True, cwd=cwd)
        info_parts.append(f"Current Branch: {branch.stdout.strip()}")
        
        # Git status summary
        status = subprocess.run(['git', 'status', '--porcelain'], 
                               capture_output=True, text=True, cwd=cwd)
        status_lines = status.stdout.strip().split('\n') if status.stdout.strip() else []
        
        modified = len([l for l in status_lines if l.startswith(' M')])
        added = len([l for l in status_lines if l.startswith('A ')])
        deleted = len([l for l in status_lines if l.startswith(' D')])
        untracked = len([l for l in status_lines if l.startswith('??')])
        
        info_parts.append(f"Changes: {modified} modified, {added} added, {deleted} deleted, {untracked} untracked")
        
        # Recent commits
        commits = subprocess.run(['git', 'log', '--oneline', '-5'], 
                                capture_output=True, text=True, cwd=cwd)
        if commits.stdout:
            info_parts.append("\nRecent Commits:")
            for line in commits.stdout.strip().split('\n'):
                info_parts.append(f"  {line}")
                
    except subprocess.CalledProcessError:
        info_parts.append("Not a git repository")
    except FileNotFoundError:
        info_parts.append("Git not found")
    
    return '\n'.join(info_parts)


@mcp.resource("git://status")
def get_git_status() -> str:
    """
    Get detailed git repository status including modified files,
    branch information, and recent commits.
    """
    cwd = os.getcwd()
    status_parts = []
    
    try:
        # Check if git repo
        subprocess.run(['git', 'rev-parse', '--git-dir'], 
                      capture_output=True, check=True, cwd=cwd)
        
        # Current branch
        branch = subprocess.run(['git', 'branch', '--show-current'], 
                               capture_output=True, text=True, cwd=cwd)
        status_parts.append(f"Current Branch: {branch.stdout.strip()}")
        
        # Remote tracking
        tracking = subprocess.run(['git', 'rev-parse', '--abbrev-ref', '@{u}'], 
                                 capture_output=True, text=True, cwd=cwd)
        if tracking.returncode == 0:
            status_parts.append(f"Tracking: {tracking.stdout.strip()}")
            
            # Ahead/behind
            ahead_behind = subprocess.run(['git', 'rev-list', '--left-right', '--count', 'HEAD...@{u}'],
                                         capture_output=True, text=True, cwd=cwd)
            if ahead_behind.returncode == 0:
                ahead, behind = ahead_behind.stdout.strip().split('\t')
                status_parts.append(f"Status: {ahead} ahead, {behind} behind")
        
        status_parts.append("\n" + "=" * 80 + "\n")
        
        # Full git status
        full_status = subprocess.run(['git', 'status', '--porcelain=v1'], 
                                   capture_output=True, text=True, cwd=cwd)
        
        if full_status.stdout:
            status_parts.append("File Changes:")
            staged = []
            modified = []
            untracked = []
            
            for line in full_status.stdout.strip().split('\n'):
                if line.startswith('A '):
                    staged.append(f"  + {line[3:]}")
                elif line.startswith('M '):
                    staged.append(f"  * {line[3:]}")
                elif line.startswith(' M'):
                    modified.append(f"  M {line[3:]}")
                elif line.startswith('??'):
                    untracked.append(f"  ? {line[3:]}")
                elif line.startswith(' D'):
                    modified.append(f"  D {line[3:]}")
                elif line.startswith('D '):
                    staged.append(f"  - {line[3:]}")
            
            if staged:
                status_parts.append("\nStaged:")
                status_parts.extend(staged)
            if modified:
                status_parts.append("\nModified:")
                status_parts.extend(modified)
            if untracked:
                status_parts.append("\nUntracked:")
                status_parts.extend(untracked)
        else:
            status_parts.append("Working tree clean")
        
        # Recent commits
        status_parts.append("\n" + "=" * 80 + "\n")
        commits = subprocess.run(['git', 'log', '--oneline', '-10'], 
                                capture_output=True, text=True, cwd=cwd)
        if commits.stdout:
            status_parts.append("Recent Commits:")
            for line in commits.stdout.strip().split('\n'):
                status_parts.append(f"  {line}")
                
    except subprocess.CalledProcessError:
        status_parts.append("Error: Not a git repository")
    except FileNotFoundError:
        status_parts.append("Error: Git not found")
    
    return '\n'.join(status_parts)


@mcp.resource("dependencies://list")
def get_dependencies() -> str:
    """
    List all project dependencies based on the package manager used.
    """
    cwd = os.getcwd()
    deps_parts = []
    
    # Check for different package managers
    if Path("package.json").exists():
        deps_parts.append("Package Manager: npm/yarn/pnpm")
        deps_parts.append("=" * 80 + "\n")
        
        try:
            with open("package.json", 'r') as f:
                data = json.load(f)
                
                # Production dependencies
                if 'dependencies' in data:
                    deps_parts.append("Production Dependencies:")
                    for dep, version in sorted(data['dependencies'].items()):
                        deps_parts.append(f"  {dep}: {version}")
                
                # Dev dependencies
                if 'devDependencies' in data:
                    deps_parts.append("\nDevelopment Dependencies:")
                    for dep, version in sorted(data['devDependencies'].items()):
                        deps_parts.append(f"  {dep}: {version}")
                        
                # Peer dependencies
                if 'peerDependencies' in data:
                    deps_parts.append("\nPeer Dependencies:")
                    for dep, version in sorted(data['peerDependencies'].items()):
                        deps_parts.append(f"  {dep}: {version}")
                        
        except Exception as e:
            deps_parts.append(f"Error reading package.json: {str(e)}")
            
    elif Path("pyproject.toml").exists():
        deps_parts.append("Package Manager: pip/poetry/uv")
        deps_parts.append("=" * 80 + "\n")
        
        try:
            with open("pyproject.toml", 'r') as f:
                content = f.read()
                
                # Simple parsing for dependencies
                in_deps = False
                in_dev_deps = False
                deps_parts.append("Dependencies:")
                
                for line in content.split('\n'):
                    if 'dependencies = [' in line:
                        in_deps = True
                        continue
                    elif '[tool.poetry.dev-dependencies]' in line or '[tool.uv.dev-dependencies]' in line:
                        in_dev_deps = True
                        in_deps = False
                        deps_parts.append("\nDevelopment Dependencies:")
                        continue
                    elif line.strip() == ']':
                        in_deps = False
                        in_dev_deps = False
                    elif (in_deps or in_dev_deps) and line.strip() and not line.strip().startswith('#'):
                        # Clean up the dependency line
                        dep_line = line.strip().strip(',').strip('"')
                        if dep_line:
                            deps_parts.append(f"  {dep_line}")
                            
        except Exception as e:
            deps_parts.append(f"Error reading pyproject.toml: {str(e)}")
            
    elif Path("requirements.txt").exists():
        deps_parts.append("Package Manager: pip")
        deps_parts.append("=" * 80 + "\n")
        deps_parts.append("Dependencies (from requirements.txt):")
        
        try:
            with open("requirements.txt", 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        deps_parts.append(f"  {line}")
        except Exception as e:
            deps_parts.append(f"Error reading requirements.txt: {str(e)}")
            
    else:
        deps_parts.append("No package manager configuration found")
    
    return '\n'.join(deps_parts)


@mcp.resource("config://list")
def get_config_files() -> str:
    """
    List all configuration files in the project.
    """
    cwd = os.getcwd()
    config_parts = []
    
    config_patterns = {
        "Environment": [".env", ".env.*", "*.env"],
        "TypeScript": ["tsconfig.json", "tsconfig.*.json"],
        "JavaScript": [".eslintrc*", ".prettierrc*", ".babelrc*", "webpack.config.*", "vite.config.*"],
        "Python": ["pyproject.toml", "setup.py", "setup.cfg", ".flake8", ".pylintrc", "mypy.ini"],
        "CI/CD": [".github/workflows/*.yml", ".gitlab-ci.yml", ".travis.yml", "Jenkinsfile"],
        "Docker": ["Dockerfile*", "docker-compose*.yml", ".dockerignore"],
        "Git": [".gitignore", ".gitattributes"],
        "Package Managers": ["package.json", "yarn.lock", "package-lock.json", "pnpm-lock.yaml"],
        "Editor": [".vscode/*", ".idea/*", ".editorconfig"],
    }
    
    config_parts.append(f"Configuration Files in {cwd}")
    config_parts.append("=" * 80)
    
    for category, patterns in config_patterns.items():
        found_files = []
        
        for pattern in patterns:
            # Handle simple patterns
            if '*' not in pattern or pattern.endswith('*'):
                # Simple prefix matching
                prefix = pattern.rstrip('*')
                for file in Path('.').iterdir():
                    if file.name.startswith(prefix) and file.is_file():
                        found_files.append(str(file))
            else:
                # Use glob for more complex patterns
                from pathlib import Path
                for file in Path('.').glob(pattern):
                    if file.is_file():
                        found_files.append(str(file))
        
        if found_files:
            config_parts.append(f"\n{category}:")
            for file in sorted(set(found_files)):
                size = Path(file).stat().st_size
                config_parts.append(f"  {file} ({size:,} bytes)")
    
    return '\n'.join(config_parts)


@mcp.resource("files://recent") 
def get_recent_files() -> str:
    """
    Get recently modified files in the project.
    """
    cwd = os.getcwd()
    recent_parts = []
    
    recent_parts.append(f"Recently Modified Files in {cwd}")
    recent_parts.append("=" * 80)
    
    try:
        # Get all files with modification times
        files_with_mtime = []
        
        # Walk through directory tree
        for root, dirs, files in os.walk('.'):
            # Skip hidden directories and common ignore patterns
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.venv']]
            
            for file in files:
                # Skip hidden files and common ignore patterns
                if file.startswith('.') or file.endswith('.pyc'):
                    continue
                    
                file_path = Path(root) / file
                try:
                    stat = file_path.stat()
                    files_with_mtime.append((file_path, stat.st_mtime, stat.st_size))
                except:
                    continue
        
        # Sort by modification time (newest first)
        files_with_mtime.sort(key=lambda x: x[1], reverse=True)
        
        # Take top 20
        recent_parts.append("\nMost recently modified files:")
        for file_path, mtime, size in files_with_mtime[:20]:
            mod_time = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
            recent_parts.append(f"  {file_path} - {mod_time} ({size:,} bytes)")
            
        if not files_with_mtime:
            recent_parts.append("No files found")
            
    except Exception as e:
        recent_parts.append(f"Error scanning files: {str(e)}")
    
    return '\n'.join(recent_parts)


@mcp.resource("context://full")
def get_full_context() -> str:
    """
    Get complete project context including directory structure and 
    contents of all files smaller than 50KB.
    """
    cwd = os.getcwd()
    context_parts = []
    
    context_parts.append(f"Full Project Context: {cwd}")
    context_parts.append("=" * 80)
    
    # First, generate the directory structure
    context_parts.append("\nDirectory Structure:")
    context_parts.append("-" * 40)
    
    try:
        tree = generate_directory_tree(
            path=str(cwd),
            max_depth=None,
            show_hidden=False
        )
        context_parts.append(tree)
    except Exception as e:
        context_parts.append(f"Error generating tree: {str(e)}")
    
    context_parts.append("\n" + "=" * 80)
    context_parts.append("File Contents (files under 50KB):")
    context_parts.append("=" * 80)
    
    # Get all files and their contents
    files_read = 0
    files_skipped = 0
    total_size = 0
    
    # Load gitignore patterns
    from src.tree_generator import TreeGenerator
    tree_gen = TreeGenerator(Path(cwd))
    
    for root, dirs, files in os.walk('.'):
        # Skip hidden directories and common ignore patterns
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', 'venv', '.venv', 'dist', 'build']]
        
        for file in files:
            # Skip hidden files and common ignore patterns
            if file.startswith('.') or file.endswith(('.pyc', '.pyo', '.so', '.dll', '.dylib')):
                files_skipped += 1
                continue
                
            file_path = Path(root) / file
            
            # Check if file is gitignored
            if tree_gen._is_ignored(file_path):
                files_skipped += 1
                continue
            
            try:
                # Check file size
                file_size = file_path.stat().st_size
                
                # Skip files larger than 50KB
                if file_size > 50 * 1024:
                    files_skipped += 1
                    continue
                
                # Skip binary files by checking extensions
                binary_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.svg',
                                   '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
                                   '.zip', '.tar', '.gz', '.rar', '.7z', '.exe', '.dmg', '.pkg',
                                   '.deb', '.rpm', '.jar', '.war', '.ear', '.class', '.pyc',
                                   '.pyo', '.mo', '.pot', '.so', '.dylib', '.dll', '.a', '.lib',
                                   '.node', '.woff', '.woff2', '.ttf', '.eot', '.mp3', '.mp4',
                                   '.avi', '.mov', '.wmv', '.flv', '.webm', '.m4a', '.aac',
                                   '.wav', '.flac', '.lock'}
                
                if any(str(file_path).endswith(ext) for ext in binary_extensions):
                    files_skipped += 1
                    continue
                
                # Read file content
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Add file to context
                    context_parts.append(f"\n{'=' * 80}")
                    context_parts.append(f"File: {file_path}")
                    context_parts.append(f"Size: {file_size:,} bytes")
                    context_parts.append("=" * 80)
                    context_parts.append(content)
                    
                    files_read += 1
                    total_size += file_size
                    
                except UnicodeDecodeError:
                    # Skip binary files that can't be decoded
                    files_skipped += 1
                    
            except Exception as e:
                files_skipped += 1
                continue
    
    # Add summary
    context_parts.append(f"\n{'=' * 80}")
    context_parts.append("Summary:")
    context_parts.append(f"Files included: {files_read}")
    context_parts.append(f"Files skipped: {files_skipped} (binary, >50KB, or gitignored)")
    context_parts.append(f"Total size of included files: {total_size:,} bytes")
    
    return '\n'.join(context_parts)


# Export the mcp instance
__all__ = ['mcp', 'run']


# Entry point for the server
def run():
    import sys
    # Check if we should run in SSE mode
    if "--sse" in sys.argv or "--transport=sse" in sys.argv:
        mcp.run(transport="sse")
    else:
        mcp.run()