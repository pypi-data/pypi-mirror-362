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
                
            # Start process with stdio pipes for MCP communication
            self.target_process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=0  # Unbuffered for real-time communication
            )
            
            # Initialize connection with target server
            await self._initialize_target_server()
            
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
    
    async def _initialize_target_server(self):
        """Initialize connection with target MCP server"""
        if not self.target_process:
            raise RuntimeError("Target process not started")
        
        # Send initialize request to target server
        init_message = MCPMessage(
            id=self.generate_message_id(),
            method="initialize",
            params={
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {},
                    "resources": {},
                    "prompts": {},
                    "logging": {}
                },
                "clientInfo": {
                    "name": "agentrix-proxy",
                    "version": "1.0.0"
                }
            }
        )
        
        # Send message to target server
        await self._send_to_target(init_message)
        
        # Read initialize response
        response = await self._read_from_target()
        
        if response and response.result:
            self.server_info = MCPServerInfo(
                name=response.result.get("serverInfo", {}).get("name", "unknown"),
                version=response.result.get("serverInfo", {}).get("version", "unknown")
            )
            self.capabilities = MCPCapabilities(**response.result.get("capabilities", {}))
            logger.info(f"Initialized target server: {self.server_info.name} v{self.server_info.version}")
        
        # Send initialized notification
        initialized_message = MCPMessage(
            method="notifications/initialized"
        )
        await self._send_to_target(initialized_message)
    
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
            self.target_process.stdin.write(message_json + "\n")
            self.target_process.stdin.flush()
        except BrokenPipeError:
            logger.error("Target process stdin closed")
            raise RuntimeError("Target process not available")
    
    async def _read_from_target(self) -> Optional[MCPMessage]:
        """Read message from target MCP server"""
        if not self.target_process or not self.target_process.stdout:
            return None
        
        try:
            # Use a timeout to avoid blocking forever
            import threading
            import queue
            
            result_queue = queue.Queue()
            
            def read_line():
                try:
                    line = self.target_process.stdout.readline()
                    result_queue.put(('success', line))
                except Exception as e:
                    result_queue.put(('error', e))
            
            thread = threading.Thread(target=read_line)
            thread.daemon = True
            thread.start()
            thread.join(timeout=5.0)  # 5 second timeout
            
            if thread.is_alive():
                logger.warning("Read from target timed out")
                return None
            
            try:
                result_type, result = result_queue.get_nowait()
                if result_type == 'error':
                    raise result
                line = result
            except queue.Empty:
                logger.warning("No result from read thread")
                return None
            
            if not line:
                return None
            
            logger.debug(f"Received from target: {line.strip()}")
            
            data = json.loads(line)
            return MCPMessage(**data)
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from target: {e}")
            return None
        except Exception as e:
            logger.error(f"Error reading from target: {e}")
            return None
    
    async def handle_mcp_message(self, message: MCPMessage) -> MCPMessage:
        """Handle incoming MCP message from client"""
        logger.debug(f"Handling MCP message: method={message.method}, id={message.id}")
        
        if message.method == "initialize":
            return await self._handle_initialize(message)
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
        else:
            # Forward other messages to target server
            return await self._forward_to_target(message)
    
    async def _handle_initialize(self, message: MCPMessage) -> MCPMessage:
        """Handle initialize request from client"""
        # Return our proxy capabilities
        return MCPMessage(
            id=message.id,
            result={
                "protocolVersion": "2024-11-05",
                "capabilities": asdict(self.capabilities) if self.capabilities else {
                    "tools": {},
                    "resources": {},
                    "prompts": {},
                    "logging": {}
                },
                "serverInfo": {
                    "name": "agentrix-proxy",
                    "version": "1.0.0"
                }
            }
        )
    
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
        """Run the MCP proxy using stdio transport"""
        logger.info("Starting MCP proxy with stdio transport")
        
        try:
            while True:
                # Read from stdin (client)
                line = sys.stdin.readline()
                if not line:
                    break
                
                try:
                    # Parse incoming message
                    data = json.loads(line.strip())
                    message = MCPMessage(**data)
                    
                    # Handle message
                    response = await self.handle_mcp_message(message)
                    
                    # Send response to stdout (client)
                    if response.id is not None or response.error:
                        response_data = asdict(response)
                        response_data = {k: v for k, v in response_data.items() if v is not None}
                        print(json.dumps(response_data), flush=True)
                        
                except json.JSONDecodeError as e:
                    logger.error(f"Failed to parse client message: {e}")
                except Exception as e:
                    logger.error(f"Error handling message: {e}")
                    
        except KeyboardInterrupt:
            logger.info("Received interrupt, shutting down")
        finally:
            await self.cleanup()
    
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
    """Run MCP proxy server"""
    proxy = MCPProxy(config)
    
    # Start target server
    if not await proxy.start_target_server(server_config):
        logger.error("Failed to start target server")
        return False
    
    # Run proxy
    await proxy.run_stdio_proxy()
    return True 