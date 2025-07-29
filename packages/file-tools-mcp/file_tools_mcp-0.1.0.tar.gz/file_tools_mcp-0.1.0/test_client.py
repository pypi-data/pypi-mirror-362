#!/usr/bin/env python3
# ABOUTME: Test client for file-tools MCP server
# Simple script to test the MCP server functionality

import asyncio
from mcp.client.session import ClientSession
from mcp.client.stdio import StdioServerParameters, stdio_client


async def main():
    # Connect to the server
    server_params = StdioServerParameters(
        command="uv",
        args=["run", "python", "main.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()
            print("Connected to file-tools MCP server!")
            
            # List available tools
            tools = await session.list_tools()
            print("\nAvailable tools:")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
                
            # List available resources
            resources = await session.list_resources()
            print("\nAvailable resources:")
            for resource in resources.resources:
                print(f"  - {resource.uri}: {resource.name}")
            
            # Test the project_structure tool
            print("\n\nTesting project_structure tool...")
            
            # Test 1: Current directory
            result = await session.call_tool("project_structure", {})
            print("\n1. Current directory structure:")
            print(result.content[0].text)
            
            # Test 2: With max depth
            result = await session.call_tool("project_structure", {"max_depth": 2})
            print("\n2. Structure with max_depth=2:")
            print(result.content[0].text)
            
            # Test 3: Show hidden files
            result = await session.call_tool("project_structure", {"show_hidden": True})
            print("\n3. Structure with hidden files:")
            print(result.content[0].text)
            
            # Test the read_multiple_files tool
            print("\n\nTesting read_multiple_files tool...")
            
            # Test reading multiple files
            result = await session.call_tool("read_multiple_files", {
                "paths": ["main.py", "pyproject.toml", "src/__init__.py"]
            })
            print("\n4. Reading multiple files:")
            print(result.content[0].text)
            
            # Test with non-existent file
            result = await session.call_tool("read_multiple_files", {
                "paths": ["main.py", "non_existent_file.txt"]
            })
            print("\n5. Reading with non-existent file:")
            print(result.content[0].text)
            
            # Test resources
            print("\n\nTesting resources...")
            
            # Test project-info resource
            print("\n6. Testing project-info resource:")
            from mcp.types import AnyUrl
            resource = await session.read_resource(AnyUrl("project://info"))
            print(resource.contents[0].text if resource.contents else "No content")
            
            # Test git-status resource
            print("\n7. Testing git-status resource:")
            resource = await session.read_resource(AnyUrl("git://status"))
            print(resource.contents[0].text[:500] + "..." if resource.contents else "No content")  # Truncate for readability
            
            # Test recent-files resource
            print("\n8. Testing recent-files resource:")
            resource = await session.read_resource(AnyUrl("files://recent"))
            print(resource.contents[0].text[:500] + "..." if resource.contents else "No content")  # Truncate for readability
            
            # Test full context resource
            print("\n9. Testing context://full resource:")
            resource = await session.read_resource(AnyUrl("context://full"))
            # Show just first 1000 chars as it will be very long
            print(resource.contents[0].text[:1000] + "..." if resource.contents else "No content")
            
            # Show the summary at the end
            if resource.contents:
                lines = resource.contents[0].text.split('\n')
                print("\n...Summary from end of output:")
                print('\n'.join(lines[-5:]))


if __name__ == "__main__":
    asyncio.run(main())