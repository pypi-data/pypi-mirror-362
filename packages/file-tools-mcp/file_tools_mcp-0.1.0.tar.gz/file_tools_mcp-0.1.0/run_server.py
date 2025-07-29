#!/usr/bin/env python3
# ABOUTME: Standalone runner for the MCP server
# Run this to start the server without the inspector

import sys
from src.server import mcp

if __name__ == "__main__":
    print("Starting File Tools MCP Server...")
    print("Transport: stdio (default)")
    print("Waiting for MCP client connections...")
    print("Press Ctrl+C to stop")
    
    try:
        mcp.run()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        sys.exit(0)