#!/usr/bin/env python3
"""Test script for MCP stdio proxy"""

import asyncio
import json
import sys
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession

async def test_proxy():
    """Test the MCP stdio proxy functionality"""
    
    # Connect to the proxy server
    server_params = StdioServerParameters(
        command=".venv/bin/python",
        args=["-m", "agentrix.cli", "run", "mcp-server-fetch"],
    )
    
    try:
        async with stdio_client(server_params) as (read_stream, write_stream):
            print("✓ Connected to proxy server")
            
            # Create a client session
            async with ClientSession(read_stream, write_stream) as session:
            
                # Initialize the session
                await session.initialize()
                print("✓ Session initialized")
                
                # Test list_tools
                print("\n--- Testing list_tools ---")
                try:
                    response = await session.list_tools()
                    print(f"✓ Tools available: {len(response.tools)}")
                    for tool in response.tools:
                        print(f"  - {tool.name}: {tool.description}")
                except Exception as e:
                    print(f"✗ Error listing tools: {e}")
                
                # Test list_resources
                print("\n--- Testing list_resources ---")
                try:
                    response = await session.list_resources()
                    print(f"✓ Resources available: {len(response.resources)}")
                    for resource in response.resources:
                        print(f"  - {resource.uri}: {resource.name}")
                except Exception as e:
                    print(f"✗ Error listing resources: {e}")
                
                # Test a simple tool call if any tools are available
                print("\n--- Testing tool call ---")
                try:
                    tools_response = await session.list_tools()
                    if tools_response.tools:
                        tool = tools_response.tools[0]
                        print(f"Testing tool: {tool.name}")
                        
                        # Try calling the tool with minimal arguments
                        result = await session.call_tool(tool.name, {"url": "https://mcp.so","max_length": 5000})
                        print(f"✓ Tool call successful")
                        for content in result.content:
                            print(f"  {content}")
                    else:
                        print("No tools available to test")
                except Exception as e:
                    print(f"✗ Error calling tool: {e}")
                
    except Exception as e:
        print(f"✗ Failed to connect to proxy: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_proxy())
    sys.exit(0 if success else 1)