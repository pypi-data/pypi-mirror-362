"""
Agentrix - Python MCP server registry and proxy for AI agents.

A powerful tool for managing and proxying Model Context Protocol (MCP) servers,
similar to @smithery/cli but built for Python developers.
"""

__version__ = "0.1.1"
__author__ = "Agentrix Team"
__email__ = "team@agentrix.dev"

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