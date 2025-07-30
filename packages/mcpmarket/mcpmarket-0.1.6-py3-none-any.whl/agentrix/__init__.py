"""
Agentrix - Python MCP server registry and proxy for AI agents.

A powerful tool for managing and proxying Model Context Protocol (MCP) servers,
"""

__version__ = "0.1.6"
__author__ = "xray918"
__email__ = "xiexinfa@gmail.com"

from .core.mcp_proxy import MCPProxy
from .core.registry import ServerRegistry
from .core.server_manager import ServerManager
from .models.server import ServerInfo, ServerConfig
from .models.config import AgentrixConfig

__all__ = [
    "MCPProxy",
    "ServerRegistry", 
    "ServerManager",
    "ServerInfo",
    "ServerConfig",
    "AgentrixConfig",
] 