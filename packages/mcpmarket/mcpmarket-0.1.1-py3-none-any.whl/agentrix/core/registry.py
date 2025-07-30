"""MCP server registry for discovering and managing servers."""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Set
from urllib.parse import urljoin

import httpx
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table

from ..models.config import AgentrixConfig, RegistryConfig
from ..models.server import ServerInfo, ServerType
from ..utils.logger import get_logger

logger = get_logger(__name__)
console = Console()


class RegistryError(Exception):
    """Registry-related errors."""
    pass


class ServerRegistry:
    """Manages MCP server registry operations."""
    
    def __init__(self, config: AgentrixConfig):
        self.config = config
        self.registry_config = config.registry
        self.cache_dir = self.registry_config.local_cache_dir
        self.cache_file = self.cache_dir / "servers.json"
        self._cache: Dict[str, ServerInfo] = {}
        self._cache_timestamp: float = 0
        
        # Ensure cache directory exists
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Load cached data
        self._load_cache()
    
    async def search_servers(
        self, 
        query: Optional[str] = None,
        category: Optional[str] = None,
        server_type: Optional[ServerType] = None,
        limit: int = 50
    ) -> List[ServerInfo]:
        """Search for servers in the registry."""
        await self._refresh_cache_if_needed()
        
        servers = list(self._cache.values())
        
        # Apply filters
        if query:
            query_lower = query.lower()
            servers = [
                server for server in servers
                if (query_lower in server.name.lower() or 
                    query_lower in server.description.lower() or
                    any(query_lower in tag.lower() for tag in server.tags))
            ]
        
        if category:
            servers = [
                server for server in servers
                if category.lower() in [cat.lower() for cat in server.categories]
            ]
        
        if server_type:
            servers = [server for server in servers if server.type == server_type]
        
        # Sort by popularity (downloads * stars)
        servers.sort(key=lambda s: s.downloads * max(s.stars, 1), reverse=True)
        
        return servers[:limit]
    
    async def get_server_info(self, server_id: str) -> Optional[ServerInfo]:
        """Get information about a specific server."""
        try:
            await self._refresh_cache_if_needed()
        except Exception as e:
            logger.warning(f"Failed to refresh cache, continuing without registry: {e}")
        
        # Check cache first
        if server_id in self._cache:
            return self._cache[server_id]
        
        # Try to fetch from remote registry
        try:
            async with httpx.AsyncClient(timeout=self.registry_config.timeout) as client:
                url = urljoin(str(self.registry_config.url), f"/api/servers/{server_id}")
                headers = self._get_auth_headers()
                
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                server_data = response.json()
                server_info = ServerInfo(**server_data)
                
                # Update cache
                self._cache[server_id] = server_info
                self._save_cache()
                
                return server_info
        
        except Exception as e:
            logger.debug(f"Failed to fetch server info for {server_id}: {e}")
            # Return None so ServerManager can create a fallback
            return None
    
    async def list_featured_servers(self) -> List[ServerInfo]:
        """Get list of featured servers."""
        try:
            async with httpx.AsyncClient(timeout=self.registry_config.timeout) as client:
                url = urljoin(str(self.registry_config.url), "/api/servers/featured")
                headers = self._get_auth_headers()
                
                response = await client.get(url, headers=headers)
                response.raise_for_status()
                
                servers_data = response.json()
                return [ServerInfo(**server_data) for server_data in servers_data]
        
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch featured servers: {e}")
            return []
        except Exception as e:
            logger.error(f"Error getting featured servers: {e}")
            return []
    
    async def get_categories(self) -> List[str]:
        """Get list of available categories."""
        await self._refresh_cache_if_needed()
        
        categories: Set[str] = set()
        for server in self._cache.values():
            categories.update(server.categories)
        
        return sorted(list(categories))
    
    async def get_server_stats(self) -> Dict[str, int]:
        """Get registry statistics."""
        await self._refresh_cache_if_needed()
        
        total_servers = len(self._cache)
        total_downloads = sum(server.downloads for server in self._cache.values())
        
        type_counts = {}
        for server in self._cache.values():
            type_counts[server.type.value] = type_counts.get(server.type.value, 0) + 1
        
        return {
            "total_servers": total_servers,
            "total_downloads": total_downloads,
            "by_type": type_counts
        }
    
    def display_search_results(self, servers: List[ServerInfo]) -> None:
        """Display search results in a formatted table."""
        if not servers:
            console.print("❌ No servers found", style="yellow")
            return
        
        table = Table(title="🔍 MCP Servers")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Description", style="white")
        table.add_column("Type", style="magenta")
        table.add_column("Downloads", style="green", justify="right")
        table.add_column("Stars", style="yellow", justify="right")
        
        for server in servers:
            # Truncate description if too long
            description = server.description
            if len(description) > 60:
                description = description[:57] + "..."
            
            table.add_row(
                server.name,
                description,
                server.type.value,
                f"{server.downloads:,}",
                str(server.stars)
            )
        
        console.print(table)
    
    def display_server_info(self, server: ServerInfo) -> None:
        """Display detailed server information."""
        console.print(f"\n📦 [bold cyan]{server.name}[/bold cyan] v{server.version}")
        console.print(f"   {server.description}")
        console.print(f"   👤 Author: {server.author}")
        console.print(f"   📁 Type: {server.type.value}")
        
        if server.tags:
            console.print(f"   🏷️  Tags: {', '.join(server.tags)}")
        
        if server.categories:
            console.print(f"   📂 Categories: {', '.join(server.categories)}")
        
        console.print(f"   📊 Downloads: {server.downloads:,}")
        console.print(f"   ⭐ Stars: {server.stars}")
        
        if server.tools:
            console.print(f"   🔧 Tools: {len(server.tools)} available")
            for tool in server.tools[:3]:  # Show first 3 tools
                console.print(f"      • {tool.name}: {tool.description}")
            if len(server.tools) > 3:
                console.print(f"      ... and {len(server.tools) - 3} more")
        
        if server.repository_url:
            console.print(f"   🔗 Repository: {server.repository_url}")
        
        console.print()
    
    async def _refresh_cache_if_needed(self) -> None:
        """Refresh cache if it's stale."""
        cache_age = time.time() - self._cache_timestamp
        
        if cache_age > self.registry_config.cache_ttl or not self._cache:
            try:
                await self._fetch_all_servers()
            except Exception as e:
                logger.warning(f"Failed to refresh registry cache: {e}")
                # Continue with existing cache or empty cache
    
    async def _fetch_all_servers(self) -> None:
        """Fetch all servers from the registry."""
        logger.info("Fetching servers from registry...")
        
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
                transient=True
            ) as progress:
                task = progress.add_task("🔄 Fetching servers...", total=None)
                
                async with httpx.AsyncClient(timeout=self.registry_config.timeout) as client:
                    url = urljoin(str(self.registry_config.url), "/api/servers")
                    headers = self._get_auth_headers()
                    
                    response = await client.get(url, headers=headers)
                    response.raise_for_status()
                    
                    servers_data = response.json()
                    
                    # Update cache
                    self._cache.clear()
                    for server_data in servers_data:
                        try:
                            server_info = ServerInfo(**server_data)
                            self._cache[server_info.id] = server_info
                        except Exception as e:
                            logger.warning(f"Failed to parse server data: {e}")
                    
                    self._cache_timestamp = time.time()
                    self._save_cache()
                    
                    progress.update(task, description=f"✅ Loaded {len(self._cache)} servers")
            
            logger.info(f"Successfully cached {len(self._cache)} servers")
        
        except httpx.HTTPError as e:
            logger.error(f"Failed to fetch servers from registry: {e}")
            raise RegistryError(f"Failed to fetch servers: {e}")
        except Exception as e:
            logger.error(f"Error fetching servers: {e}")
            raise RegistryError(f"Registry error: {e}")
    
    def _load_cache(self) -> None:
        """Load servers from local cache."""
        if not self.cache_file.exists():
            return
        
        try:
            with open(self.cache_file, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            self._cache_timestamp = cache_data.get('timestamp', 0)
            servers_data = cache_data.get('servers', {})
            
            self._cache.clear()
            for server_id, server_data in servers_data.items():
                try:
                    server_info = ServerInfo(**server_data)
                    self._cache[server_id] = server_info
                except Exception as e:
                    logger.warning(f"Failed to load cached server {server_id}: {e}")
            
            logger.debug(f"Loaded {len(self._cache)} servers from cache")
        
        except Exception as e:
            logger.warning(f"Failed to load cache: {e}")
            self._cache.clear()
            self._cache_timestamp = 0
    
    def _save_cache(self) -> None:
        """Save servers to local cache."""
        try:
            cache_data = {
                'timestamp': self._cache_timestamp,
                'servers': {
                    server_id: server_info.dict()
                    for server_id, server_info in self._cache.items()
                }
            }
            
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, indent=2, default=str, ensure_ascii=False)
            
            logger.debug(f"Saved {len(self._cache)} servers to cache")
        
        except Exception as e:
            logger.warning(f"Failed to save cache: {e}")
    
    def _get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for registry requests."""
        headers = {
            "User-Agent": "agentrix/0.1.0",
            "Accept": "application/json"
        }
        
        if self.registry_config.api_key:
            headers["Authorization"] = f"Bearer {self.registry_config.api_key}"
        
        return headers
    
    def clear_cache(self) -> None:
        """Clear local cache."""
        self._cache.clear()
        self._cache_timestamp = 0
        
        if self.cache_file.exists():
            self.cache_file.unlink()
        
        logger.info("Cache cleared")
        console.print("✅ Registry cache cleared", style="green") 