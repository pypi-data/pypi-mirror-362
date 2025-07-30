"""Configuration models for Agentrix."""

from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from pydantic import BaseModel, Field, HttpUrl, validator
from pydantic_settings import BaseSettings


class ClientType(str, Enum):
    """Supported MCP client types."""
    
    CURSOR = "cursor"
    CLAUDE_DESKTOP = "claude"
    VSCODE = "vscode"
    CLINE = "cline"
    WINDSURF = "windsurf"
    CUSTOM = "custom"


class TransportType(str, Enum):
    """MCP transport types."""
    
    STDIO = "stdio"
    HTTP = "http"
    WEBSOCKET = "websocket"


class LogLevel(str, Enum):
    """Logging levels."""
    
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ClientConfig(BaseModel):
    """Configuration for a specific MCP client."""
    
    type: ClientType = Field(..., description="Client type")
    config_path: Path = Field(..., description="Path to client config file")
    transport: TransportType = Field(default=TransportType.STDIO, description="Transport type")
    
    # Client-specific settings
    supports_env_vars: bool = Field(default=True, description="Supports environment variables")
    config_format: str = Field(default="json", description="Config file format (json/toml)")
    server_key: str = Field(default="mcpServers", description="Key for servers in config")
    
    @validator('config_path')
    def expand_path(cls, v: Path) -> Path:
        """Expand user home directory in path."""
        return Path(v).expanduser().resolve()


class RegistryConfig(BaseModel):
    """Registry configuration."""
    
    url: HttpUrl = Field(default="https://registry.agentrix.dev", description="Registry URL")
    api_key: Optional[str] = Field(None, description="Registry API key")
    cache_ttl: int = Field(default=3600, description="Cache TTL in seconds")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    
    # Local registry settings
    local_cache_dir: Path = Field(
        default=Path.home() / "cache",
        description="Local cache directory"
    )
    
    @validator('local_cache_dir')
    def expand_cache_dir(cls, v: Path) -> Path:
        """Expand cache directory path."""
        return Path(v).expanduser().resolve()


class ProxyConfig(BaseModel):
    """Proxy server configuration."""
    
    host: str = Field(default="127.0.0.1", description="Proxy host")
    port: int = Field(default=8080, description="Proxy port")
    path: str = Field(default="/mcp", description="Proxy endpoint path")
    
    # Security settings
    enable_auth: bool = Field(default=False, description="Enable authentication")
    api_keys: List[str] = Field(default_factory=list, description="Valid API keys")
    cors_origins: List[str] = Field(default_factory=list, description="CORS origins")
    
    # Performance settings
    max_connections: int = Field(default=100, description="Max concurrent connections")
    timeout: int = Field(default=300, description="Connection timeout")
    
    @validator('port')
    def validate_port(cls, v: int) -> int:
        """Validate port number."""
        if not 1 <= v <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return v


class LoggingConfig(BaseModel):
    """Logging configuration."""
    
    level: LogLevel = Field(default=LogLevel.INFO, description="Log level")
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    
    # File logging
    log_file: Optional[Path] = Field(None, description="Log file path")
    max_file_size: int = Field(default=10 * 1024 * 1024, description="Max log file size")
    backup_count: int = Field(default=5, description="Number of backup files")
    
    # Console logging
    console_enabled: bool = Field(default=True, description="Enable console logging")
    colorize: bool = Field(default=True, description="Colorize console output")


class AgentrixConfig(BaseSettings):
    """Main Agentrix configuration."""
    
    # Core settings
    registry: RegistryConfig = Field(default_factory=RegistryConfig)
    proxy: ProxyConfig = Field(default_factory=ProxyConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    # Data directories
    data_dir: Path = Field(
        default=Path.home() / ".agentrix",
        description="Data directory"
    )
    servers_dir: Path = Field(
        default=Path.home() / ".agentrix" / "servers",
        description="Servers directory"
    )
    
    # Client configurations
    clients: Dict[str, ClientConfig] = Field(
        default_factory=dict,
        description="Client configurations"
    )
    
    # Development settings
    dev_mode: bool = Field(default=False, description="Development mode")
    debug: bool = Field(default=False, description="Debug mode")
    
    class Config:
        env_prefix = "AGENTRIX_"
        env_file = ".env"
        env_nested_delimiter = "__"
        extra = "ignore"  # 忽略额外的环境变量
    
    @validator('data_dir', 'servers_dir')
    def expand_directories(cls, v: Path) -> Path:
        """Expand directory paths."""
        return Path(v).expanduser().resolve()
    
    def get_client_config(self, client_type: str) -> Optional[ClientConfig]:
        """Get configuration for a specific client."""
        return self.clients.get(client_type)
    
    def set_client_config(self, client_type: str, config: ClientConfig) -> None:
        """Set configuration for a specific client."""
        self.clients[client_type] = config
    
    @classmethod
    def get_default_client_configs(cls) -> Dict[str, ClientConfig]:
        """Get default client configurations."""
        return {
            "cursor": ClientConfig(
                type=ClientType.CURSOR,
                config_path=Path.home() / ".cursor" / "mcp.json",
                transport=TransportType.STDIO,
                config_format="json",
                server_key="mcpServers"
            ),
            "claude": ClientConfig(
                type=ClientType.CLAUDE_DESKTOP,
                config_path=Path.home() / "Library" / "Application Support" / "Claude" / "claude_desktop_config.json",
                transport=TransportType.STDIO,
                config_format="json", 
                server_key="mcpServers"
            ),
            "vscode": ClientConfig(
                type=ClientType.VSCODE,
                config_path=Path.home() / ".vscode" / "settings.json",
                transport=TransportType.STDIO,
                config_format="json",
                server_key="mcp.servers"
            )
        }
    
    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        for dir_path in [self.data_dir, self.servers_dir, self.registry.local_cache_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)


class ClientInstallConfig(BaseModel):
    """Configuration for installing to a specific client."""
    
    client: str = Field(..., description="Client name")
    server_name: str = Field(..., description="Server name in client config")
    server_id: str = Field(..., description="Server identifier")
    
    # Installation options
    api_key: Optional[str] = Field(None, description="API key for server")
    custom_args: List[str] = Field(default_factory=list, description="Custom arguments")
    env_vars: Dict[str, str] = Field(default_factory=dict, description="Environment variables")
    
    # Advanced options
    auto_start: bool = Field(default=True, description="Auto-start server")
    restart_on_fail: bool = Field(default=True, description="Restart on failure")
    
    class Config:
        frozen = True 