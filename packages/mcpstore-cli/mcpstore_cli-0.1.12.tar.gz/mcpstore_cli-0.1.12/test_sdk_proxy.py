#!/usr/bin/env python3
"""
Test script for MCP SDK proxy functionality.
"""

import asyncio
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from agentrix.core.mcp_sdk_proxy import StdioProxy
from agentrix.models.server import ServerConfig

async def test_proxy():
    """Test the StdioProxy functionality"""
    print("Testing StdioProxy...")
    
    # Create a test server config
    config = ServerConfig(
        name='mcp-server-fetch',
        server_id='mcp-server-fetch',
        command='uvx',
        args=['mcp-server-fetch'],
        env={}
    )
    
    # Create proxy instance
    proxy = StdioProxy(config)
    
    try:
        print("✓ StdioProxy created successfully")
        
        # Test command building
        cmd = proxy._build_server_command()
        print(f"✓ Command built: {cmd}")
        
        # Test environment building
        env = proxy._build_environment()
        print(f"✓ Environment built with {len(env)} variables")
        
        # Note: We don't actually start the proxy here to avoid hanging
        # In real usage, you would call await proxy.start()
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        return False
    finally:
        await proxy.stop()

if __name__ == "__main__":
    success = asyncio.run(test_proxy())
    sys.exit(0 if success else 1)