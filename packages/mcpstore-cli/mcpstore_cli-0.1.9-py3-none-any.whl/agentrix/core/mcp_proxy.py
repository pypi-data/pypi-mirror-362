"""
MCP Proxy Server Implementation - Python port of @smithery/cli

This implements a Model Context Protocol (MCP) proxy that:
1. Acts as an MCP server to the client (Cursor, Claude, etc.)
2. Forwards requests to target MCP servers
3. Manages server lifecycle and configuration

Based on the architecture found in @smithery/cli.
"""

import asyncio
import json
import sys
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
import logging

from ..models.config import AgentrixConfig
from ..models.server import ServerInfo, ServerConfig
from ..utils.logger import get_logger

logger = get_logger(__name__)


@dataclass
class MCPMessage:
    """MCP protocol message structure"""
    jsonrpc: str = "2.0"
    id: Optional[Union[str, int]] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


@dataclass 
class MCPCapabilities:
    """MCP server capabilities"""
    tools: Optional[Dict[str, Any]] = None
    resources: Optional[Dict[str, Any]] = None
    prompts: Optional[Dict[str, Any]] = None
    logging: Optional[Dict[str, Any]] = None
    experimental: Optional[Dict[str, Any]] = None


@dataclass
class MCPServerInfo:
    """MCP server information"""
    name: str
    version: str
    

class MCPProxy:
    """
    MCP Proxy that implements the MCP protocol and forwards requests
    to target servers. This is similar to how @smithery/cli works.
    """
    
    def __init__(self, config: AgentrixConfig):
        self.config = config
        self.target_process: Optional[subprocess.Popen] = None
        self.server_info: Optional[MCPServerInfo] = None
        self.capabilities: Optional[MCPCapabilities] = None
        self.message_id_counter = 0
        
    def generate_message_id(self) -> int:
        """Generate unique message ID"""
        self.message_id_counter += 1
        return self.message_id_counter
        
    async def start_target_server(self, server_config: ServerConfig) -> bool:
        """Start the target MCP server process"""
        try:
            logger.info(f"Starting target MCP server: {server_config.name}")
            
            # Build command based on server type
            cmd = self._build_server_command(server_config)
            
            if not cmd:
                logger.error(f"Failed to build command for server: {server_config.name}")
                return False
                
            # Build environment
            env = os.environ.copy()
            if server_config.api_key:
                env[f"{server_config.name.upper().replace('-', '_')}_API_KEY"] = server_config.api_key
            env.update(server_config.env)
            
            logger.info(f"Starting target server with command: {' '.join(cmd)}")
                
            # Start process with stdio pipes for MCP communication
            self.target_process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=False,  # Use bytes mode for better control
                bufsize=0,  # Unbuffered for real-time communication
                env=env
            )
            
            # Wait a moment for the server to start
            await asyncio.sleep(0.1)
            
            logger.info(f"Target MCP server started successfully: {server_config.name}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start target server: {e}")
            return False
    
    def _build_server_command(self, server_config: ServerConfig) -> Optional[List[str]]:
        """Build command to start the target MCP server"""
        if server_config.command:
            # Direct command specified
            if isinstance(server_config.command, str):
                return server_config.command.split()
            return server_config.command
        
        # Try to determine command from server type/name
        server_name = server_config.name.lower()
        
        if server_name.startswith('@'):
            # NPM package - try to run with npx
            return ["npx", "-y", server_config.name]
        
        # Default fallback
        return ["uvx", server_config.name]
    
    
    async def _send_to_target(self, message: MCPMessage):
        """Send message to target MCP server"""
        if not self.target_process or not self.target_process.stdin:
            raise RuntimeError("Target process not available")
        
        message_data = asdict(message)
        # Remove None values
        message_data = {k: v for k, v in message_data.items() if v is not None}
        
        message_json = json.dumps(message_data)
        logger.debug(f"Sending to target: {message_json}")
        
        try:
            # Write message to target process
            message_line = message_json + "\n"
            self.target_process.stdin.write(message_line.encode('utf-8'))
            # Use executor for flush to avoid blocking
            await asyncio.get_event_loop().run_in_executor(None, self.target_process.stdin.flush)
            
        except BrokenPipeError:
            logger.error("Target process stdin closed")
            raise RuntimeError("Target process not available")
        except Exception as e:
            logger.error(f"Error sending to target: {e}")
            raise RuntimeError(f"Failed to send to target: {e}")
    
    async def _read_from_target(self) -> Optional[MCPMessage]:
        """Read message from target MCP server"""
        if not self.target_process or not self.target_process.stdout:
            return None
        
        try:
            # Use executor to read from stdout in a non-blocking way
            def read_line():
                return self.target_process.stdout.readline()
            
            # Read line with timeout
            line_bytes = await asyncio.wait_for(
                asyncio.get_event_loop().run_in_executor(None, read_line),
                timeout=5.0
            )
            
            if not line_bytes:
                return None
            
            line_str = line_bytes.decode('utf-8').strip()
            if not line_str:
                return None
                
            logger.debug(f"Received from target: {line_str}")
            
            data = json.loads(line_str)
            return MCPMessage(**data)
            
        except asyncio.TimeoutError:
            logger.warning("Read from target timed out")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from target: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading from target: {e}")
            return None
    
    async def handle_mcp_message(self, message: MCPMessage) -> Optional[MCPMessage]:
        """Handle incoming MCP message from client"""
        logger.debug(f"Handling MCP message: method={message.method}, id={message.id}")
        
        if message.method == "initialize":
            return await self._handle_initialize(message)
        elif message.method == "notifications/initialized":
            # Handle initialized notification - no response needed
            await self._handle_initialized_notification(message)
            return None
        elif message.method == "tools/list":
            return await self._handle_tools_list(message)
        elif message.method == "tools/call":
            return await self._handle_tools_call(message)
        elif message.method == "resources/list":
            return await self._handle_resources_list(message)
        elif message.method == "resources/read":
            return await self._handle_resources_read(message)
        elif message.method == "prompts/list":
            return await self._handle_prompts_list(message)
        elif message.method == "prompts/get":
            return await self._handle_prompts_get(message)
        elif message.method and message.method.startswith("notifications/"):
            # Handle other notifications - forward to target but no response to client
            await self._forward_notification_to_target(message)
            return None
        else:
            # Forward other messages to target server
            return await self._forward_to_target(message)
    
    async def _handle_initialize(self, message: MCPMessage) -> MCPMessage:
        """Handle initialize request from client"""
        # Return our proxy capabilities based on target server capabilities
        capabilities = {}
        server_info = {"name": "agentrix-proxy", "version": "1.0.0"}
        
        if self.capabilities:
            capabilities = asdict(self.capabilities)
        else:
            capabilities = {"tools": {}, "resources": {}, "prompts": {}, "logging": {}}
            
        if self.server_info:
            server_info = {"name": self.server_info.name, "version": self.server_info.version}
        
        return MCPMessage(
            id=message.id,
            result={
                "protocolVersion": "2024-11-05",
                "capabilities": capabilities,
                "serverInfo": server_info
            }
        )
    
    async def _handle_initialized_notification(self, message: MCPMessage) -> None:
        """Handle initialized notification from client"""
        logger.debug("Received initialized notification from client")
        # Forward to target server if needed
        if self.target_process:
            await self._send_to_target(message)
    
    async def _forward_notification_to_target(self, message: MCPMessage) -> None:
        """Forward notification to target server"""
        if self.target_process:
            try:
                await self._send_to_target(message)
            except Exception as e:
                logger.error(f"Failed to forward notification to target: {e}")
    
    async def _handle_tools_list(self, message: MCPMessage) -> MCPMessage:
        """Handle tools/list request"""
        return await self._forward_to_target(message)
    
    async def _handle_tools_call(self, message: MCPMessage) -> MCPMessage:
        """Handle tools/call request"""
        return await self._forward_to_target(message)
    
    async def _handle_resources_list(self, message: MCPMessage) -> MCPMessage:
        """Handle resources/list request"""
        return await self._forward_to_target(message)
    
    async def _handle_resources_read(self, message: MCPMessage) -> MCPMessage:
        """Handle resources/read request"""
        return await self._forward_to_target(message)
    
    async def _handle_prompts_list(self, message: MCPMessage) -> MCPMessage:
        """Handle prompts/list request"""
        return await self._forward_to_target(message)
    
    async def _handle_prompts_get(self, message: MCPMessage) -> MCPMessage:
        """Handle prompts/get request"""
        return await self._forward_to_target(message)
    
    async def _forward_to_target(self, message: MCPMessage) -> MCPMessage:
        """Forward message to target server and return response"""
        if not self.target_process:
            return MCPMessage(
                id=message.id,
                error={
                    "code": -32603,
                    "message": "Target server not available"
                }
            )
        
        try:
            # Forward message to target
            await self._send_to_target(message)
            
            # Read response from target
            response = await self._read_from_target()
            
            if response:
                return response
            else:
                return MCPMessage(
                    id=message.id,
                    error={
                        "code": -32603,
                        "message": "No response from target server"
                    }
                )
                
        except Exception as e:
            logger.error(f"Error forwarding to target: {e}")
            return MCPMessage(
                id=message.id,
                error={
                    "code": -32603,
                    "message": f"Forward error: {str(e)}"
                }
            )
    
    async def run_stdio_proxy(self):
        """Run the MCP proxy using stdio transport - transparent proxy mode"""
        logger.info("Starting MCP proxy with stdio transport")
        
        try:
            # Create tasks for bidirectional communication
            tasks = [
                asyncio.create_task(self._handle_client_to_server()),
                asyncio.create_task(self._handle_server_to_client())
            ]
            
            # Wait for any task to complete (shouldn't happen in normal operation)
            done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)
            
            # Cancel remaining tasks
            for task in pending:
                task.cancel()
                
        except KeyboardInterrupt:
            logger.info("Received interrupt, shutting down")
        finally:
            await self.cleanup()
    
    async def _handle_client_to_server(self):
        """Handle messages from client to server"""
        # Create async stdin reader
        stdin_reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(stdin_reader)
        loop = asyncio.get_event_loop()
        await loop.connect_read_pipe(lambda: protocol, sys.stdin)
        
        while True:
            try:
                # Read from stdin (client) asynchronously
                line = await stdin_reader.readline()
                if not line:
                    break
                
                line_str = line.decode('utf-8').strip()
                if not line_str:
                    continue
                    
                logger.debug(f"Client -> Server: {line_str}")
                
                # Forward directly to target server
                if self.target_process and self.target_process.stdin:
                    self.target_process.stdin.write(line)
                    await asyncio.get_event_loop().run_in_executor(None, self.target_process.stdin.flush)
                    
            except Exception as e:
                logger.error(f"Error in client to server communication: {e}")
                break
    
    async def _handle_server_to_client(self):
        """Handle messages from server to client"""
        if not self.target_process or not self.target_process.stdout:
            return
            
        # Create async stdout reader
        stdout_reader = asyncio.StreamReader()
        protocol = asyncio.StreamReaderProtocol(stdout_reader)
        loop = asyncio.get_event_loop()
        transport, _ = await loop.connect_read_pipe(lambda: protocol, self.target_process.stdout)
        
        try:
            while True:
                # Read from target server stdout
                line = await stdout_reader.readline()
                if not line:
                    break
                
                line_str = line.decode('utf-8').strip()
                if not line_str:
                    continue
                    
                logger.debug(f"Server -> Client: {line_str}")
                
                # Forward directly to client (stdout)
                print(line_str, flush=True)
                
        except Exception as e:
            logger.error(f"Error in server to client communication: {e}")
        finally:
            transport.close()
    
    async def cleanup(self):
        """Clean up resources"""
        logger.info("Cleaning up MCP proxy")
        
        if self.target_process:
            try:
                self.target_process.terminate()
                self.target_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.target_process.kill()
            except Exception as e:
                logger.error(f"Error terminating target process: {e}")


async def run_mcp_proxy(config: AgentrixConfig, server_config: ServerConfig):
    """Run MCP proxy server in transparent mode"""
    proxy = MCPProxy(config)
    
    # Start target server
    if not await proxy.start_target_server(server_config):
        logger.error("Failed to start target server")
        return False
    
    # Run transparent proxy
    await proxy.run_stdio_proxy()
    return True 