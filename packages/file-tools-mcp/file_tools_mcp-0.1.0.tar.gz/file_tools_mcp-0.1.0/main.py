import sys
import os

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.server import mcp


def main():
    """Main entry point for the file-tools MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()
