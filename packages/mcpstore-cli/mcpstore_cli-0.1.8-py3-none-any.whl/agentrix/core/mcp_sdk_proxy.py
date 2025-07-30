"""
MCP SDK-based proxy implementation.

This module provides a proper MCP proxy using the official MCP Python SDK,
based on the working example provided.
"""

import asyncio
import sys
import os
from typing import Any, Dict, Optional
import anyio
import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.client.stdio import StdioServerParameters, stdio_client
from mcp.client.session import ClientSession
from mcp.server.stdio import stdio_server

from ..models.config import AgentrixConfig
from ..models.server import ServerConfig
from ..utils.logger import get_logger

logger = get_logger(__name__)


class StdioProxy:
    """A proxy that forwards MCP requests to another stdio server"""
    
    def __init__(self, server_config: ServerConfig):
        self.server_config = server_config
        self.client_session = None
        self.client_cm = None
        self._initialized = False
        
    async def start(self):
        """Start the target MCP server process and connect to it"""
        # Build command
        cmd = self._build_server_command()
        if not cmd:
            raise RuntimeError(f"Failed to build command for server: {self.server_config.name}")
        
        # Build environment
        env = self._build_environment()
        
        logger.info(f"Starting server: {cmd[0]} {cmd[1:]} with env keys: {list(env.keys())}")
        
        server_params = StdioServerParameters(
            command=cmd[0],
            args=cmd[1:],
            env=env
        )
        
        # Create stdio client connection to the target server
        self.client_cm = stdio_client(server_params)
        read_stream, write_stream = await self.client_cm.__aenter__()
            
        # Create client session
        session = ClientSession(read_stream, write_stream)
        self.client_session = await session.__aenter__()
        logger.info("Client session created, deferring initialization")
        
    async def _ensure_initialized(self):
        """Ensure the client session is initialized"""
        if not self._initialized and self.client_session:
            logger.info("Initializing client session on first use...")
            try:
                await self.client_session.initialize()
                self._initialized = True
                logger.info("Client session initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize client session: {e}")
                raise
        
    async def stop(self):
        """Stop the target MCP server process"""
        if self.client_session:
            await self.client_session.__aexit__(None, None, None)
        if self.client_cm:
            await self.client_cm.__aexit__(None, None, None)
        self.client_cm = None
        self.client_session = None
    
    def _build_server_command(self) -> Optional[list[str]]:
        """Build command to start the target MCP server"""
        if self.server_config.command:
            if isinstance(self.server_config.command, str):
                cmd = [self.server_config.command]
            else:
                cmd = list(self.server_config.command)
            cmd.extend(self.server_config.args)
            return cmd
        
        # Try to determine command from server name
        server_name = self.server_config.name.lower()
        
        if server_name.startswith('@'):
            # NPM package
            return ["npx", "-y", self.server_config.name]
        
        # Default fallback - Python package
        return ["uvx", self.server_config.name]
    
    def _build_environment(self) -> Dict[str, str]:
        """Build environment variables for the target server"""
        env = os.environ.copy()
        
        # Add API key if provided
        if self.server_config.api_key:
            env[f"{self.server_config.name.upper().replace('-', '_')}_API_KEY"] = self.server_config.api_key
        
        # Add custom environment variables
        env.update(self.server_config.env)
        
        return env
    
    async def list_tools(self) -> list[types.Tool]:
        """Forward list_tools request to target server"""
        try:
            await self._ensure_initialized()
            response = await self.client_session.list_tools()
            return response.tools
        except Exception as e:
            logger.error(f"Error listing tools: {e}")
            return []
            
    async def call_tool(self, name: str, arguments: dict) -> list[types.ContentBlock]:
        """Forward call_tool request to target server"""
        try:
            response = await self.client_session.call_tool(name, arguments)
            return response.content
        except Exception as e:
            logger.error(f"Error calling tool {name}: {e}")
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
            
    async def list_resources(self) -> list[types.Resource]:
        """Forward list_resources request to target server"""
        try:
            await self._ensure_initialized()
            response = await self.client_session.list_resources()
            return response.resources
        except Exception as e:
            if "Method not found" in str(e):
                logger.debug(f"Target server does not support resources")
            else:
                logger.error(f"Error listing resources: {e}")
            return []
            
    async def read_resource(self, uri: str) -> list[types.ContentBlock]:
        """Forward read_resource request to target server"""
        try:
            response = await self.client_session.read_resource(uri)
            return response.contents
        except Exception as e:
            logger.error(f"Error reading resource {uri}: {e}")
            return [types.TextContent(type="text", text=f"Error: {str(e)}")]
            
    async def list_prompts(self) -> list[types.Prompt]:
        """Forward list_prompts request to target server"""
        try:
            response = await self.client_session.list_prompts()
            return response.prompts
        except Exception as e:
            logger.error(f"Error listing prompts: {e}")
            return []
            
    async def get_prompt(self, name: str, arguments: dict = None) -> types.GetPromptResult:
        """Forward get_prompt request to target server"""
        try:
            response = await self.client_session.get_prompt(name, arguments)
            return response
        except Exception as e:
            logger.error(f"Error getting prompt {name}: {e}")
            return types.GetPromptResult(
                description=f"Error: {str(e)}",
                messages=[]
            )
    

async def run_mcp_sdk_proxy(config: AgentrixConfig, server_config: ServerConfig):
    """Run MCP proxy server using SDK - based on working example"""
    
    # Create proxy instance
    proxy = StdioProxy(server_config)
    
    # Create proxy server
    app = Server("agentrix-proxy")
    
    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        return await proxy.list_tools()
    
    @app.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.ContentBlock]:
        return await proxy.call_tool(name, arguments)
    
    @app.list_resources()
    async def list_resources() -> list[types.Resource]:
        return await proxy.list_resources()
    
    @app.read_resource()
    async def read_resource(uri: str) -> list[types.ContentBlock]:
        return await proxy.read_resource(uri)
    
    @app.list_prompts()
    async def list_prompts() -> list[types.Prompt]:
        return await proxy.list_prompts()
    
    @app.get_prompt()
    async def get_prompt(name: str, arguments: dict = None) -> types.GetPromptResult:
        return await proxy.get_prompt(name, arguments)

    async def arun():
        # Start the proxy connection to target server
        await proxy.start()
        
        try:
            async with stdio_server() as streams:
                await app.run(
                    streams[0], streams[1], app.create_initialization_options()
                )
        finally:
            # Clean up proxy connection
            await proxy.stop()

    # Run with anyio
    anyio.run(arun)
    return True