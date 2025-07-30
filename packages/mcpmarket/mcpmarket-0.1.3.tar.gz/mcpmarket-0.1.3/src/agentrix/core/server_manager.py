"""MCP server lifecycle management."""

import asyncio
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
import signal

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from ..models.config import AgentrixConfig
from ..models.server import (
    ServerInfo, ServerConfig, ServerInstance, ServerStatus, 
    ServerType, InstallationResult
)
from ..utils.logger import get_logger, LoggerMixin
from .registry import ServerRegistry
from .mcp_proxy import run_mcp_proxy

logger = get_logger(__name__)
console = Console()


class ServerManagerError(Exception):
    """Server manager related errors."""
    pass


class ServerManager(LoggerMixin):
    """Manages MCP server installations and runtime."""
    
    def __init__(self, config: AgentrixConfig):
        self.config = config
        self.registry = ServerRegistry(config)
        self.servers_dir = config.servers_dir
        self.running_servers: Dict[str, ServerInstance] = {}
        
        # Ensure servers directory exists
        self.servers_dir.mkdir(parents=True, exist_ok=True)
    
    async def install_server(
        self, 
        server_id: str, 
        version: str = "latest"
    ) -> InstallationResult:
        """Install a server from the registry."""
        start_time = time.time()
        
        try:
            # Get server info
            server_info = await self.registry.get_server_info(server_id)
            if not server_info:
                return InstallationResult(
                    success=False,
                    server_id=server_id,
                    version=version,
                    message=f"Server '{server_id}' not found in registry",
                    duration=time.time() - start_time
                )
            
            self.logger.info(f"Installing server: {server_id} v{version}")
            
            # Check if already installed
            if await self._is_server_installed(server_info):
                return InstallationResult(
                    success=True,
                    server_id=server_id,
                    version=version,
                    message=f"Server '{server_id}' is already available",
                    duration=time.time() - start_time
                )
            
            # Install based on type
            if server_info.type == ServerType.NPM:
                result = await self._install_npm_server(server_info, version)
            elif server_info.type == ServerType.PYPI:
                result = await self._install_pypi_server(server_info, version)
            elif server_info.type == ServerType.GITHUB:
                result = await self._install_github_server(server_info, version)
            elif server_info.type == ServerType.DOCKER:
                result = await self._install_docker_server(server_info, version)
            else:
                result = InstallationResult(
                    success=False,
                    server_id=server_id,
                    version=version,
                    message=f"Unsupported server type: {server_info.type}",
                    duration=time.time() - start_time
                )
            
            result.duration = time.time() - start_time
            return result
        
        except Exception as e:
            self.logger.error(f"Installation failed: {e}")
            return InstallationResult(
                success=False,
                server_id=server_id,
                version=version,
                message=f"Installation error: {e}",
                duration=time.time() - start_time
            )
    
    async def run_server_proxy(
        self, 
        server_id: str, 
        api_key: Optional[str] = None,
        config_str: Optional[str] = None
    ) -> None:
        """Run server in proxy mode (main entry point for MCP clients)."""
        self.logger.info(f"Starting MCP proxy for server: {server_id}")
        
        try:
            # Get server info from registry
            server_info = await self.registry.get_server_info(server_id)
            if not server_info:
                # Try to treat as a direct package name (similar to @smithery/cli)
                self.logger.warning(f"Server '{server_id}' not found in registry, trying as direct package")
                # Create minimal server info for direct packages
                server_info = ServerInfo(
                    id=server_id,
                    name=server_id,
                    description=f"Direct package: {server_id}",
                    version="latest",
                    author="Unknown",
                    type=ServerType.NPM if server_id.startswith("@") else ServerType.PYPI,
                    package_name=server_id
                )
            
            # Parse additional config
            extra_config = {}
            if config_str:
                try:
                    extra_config = json.loads(config_str)
                except json.JSONDecodeError as e:
                    self.logger.warning(f"Invalid config JSON: {e}")
            
            # Create server configuration
            server_config = ServerConfig(
                name=server_id,
                server_id=server_id,
                type=server_info.type,
                api_key=api_key,
                env=extra_config.get("env", {}),
                args=extra_config.get("args", [])
            )
            
            # Start the MCP proxy (this is the correct implementation)
            await run_mcp_proxy(self.config, server_config)
        
        except Exception as e:
            self.logger.error(f"Failed to run server proxy: {e}")
            raise
    
    async def _install_npm_server(
        self, 
        server_info: ServerInfo, 
        version: str
    ) -> InstallationResult:
        """Install NPM-based MCP server."""
        package_name = server_info.package_name or server_info.id
        install_cmd = ["npx", "-y", f"{package_name}@{version}"]
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task(f"Installing {package_name}...", total=None)
            
            try:
                # Test installation by running with --help
                result = await asyncio.create_subprocess_exec(
                    *install_cmd, "--help",
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await result.communicate()
                
                if result.returncode == 0:
                    progress.update(task, description=f"✅ Installed {package_name}")
                    return InstallationResult(
                        success=True,
                        server_id=server_info.id,
                        version=version,
                        message=f"Successfully installed {package_name}",
                        config=ServerConfig(
                            name=server_info.name,
                            server_id=server_info.id,
                            type=ServerType.NPM,
                            command="npx",
                            args=["-y", f"{package_name}@{version}"]
                        )
                    )
                else:
                    error_msg = stderr.decode() if stderr else "Unknown error"
                    return InstallationResult(
                        success=False,
                        server_id=server_info.id,
                        version=version,
                        message=f"NPM installation failed: {error_msg}"
                    )
            
            except Exception as e:
                return InstallationResult(
                    success=False,
                    server_id=server_info.id,
                    version=version,
                    message=f"NPM installation error: {e}"
                )
    
    async def _install_pypi_server(
        self, 
        server_info: ServerInfo, 
        version: str
    ) -> InstallationResult:
        """Install PyPI-based MCP server."""
        package_name = server_info.package_name or server_info.id
        version_spec = f"=={version}" if version != "latest" else ""
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task(f"Installing {package_name}...", total=None)
            
            try:
                # Use uvx for isolated installation
                install_cmd = ["uvx", f"{package_name}{version_spec}", "--help"]
                
                result = await asyncio.create_subprocess_exec(
                    *install_cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await result.communicate()
                
                if result.returncode == 0:
                    progress.update(task, description=f"✅ Installed {package_name}")
                    return InstallationResult(
                        success=True,
                        server_id=server_info.id,
                        version=version,
                        message=f"Successfully installed {package_name}",
                        config=ServerConfig(
                            name=server_info.name,
                            server_id=server_info.id,
                            type=ServerType.PYPI,
                            command="uvx",
                            args=[f"{package_name}{version_spec}"]
                        )
                    )
                else:
                    error_msg = stderr.decode() if stderr else "Unknown error"
                    return InstallationResult(
                        success=False,
                        server_id=server_info.id,
                        version=version,
                        message=f"PyPI installation failed: {error_msg}"
                    )
            
            except Exception as e:
                return InstallationResult(
                    success=False,
                    server_id=server_info.id,
                    version=version,
                    message=f"PyPI installation error: {e}"
                )
    
    async def _install_github_server(
        self, 
        server_info: ServerInfo, 
        version: str
    ) -> InstallationResult:
        """Install GitHub-based MCP server."""
        if not server_info.repository_url:
            return InstallationResult(
                success=False,
                server_id=server_info.id,
                version=version,
                message="No repository URL provided"
            )
        
        # For GitHub servers, we'll clone and install locally
        server_dir = self.servers_dir / server_info.id
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task(f"Cloning {server_info.id}...", total=None)
            
            try:
                # Clone repository
                if server_dir.exists():
                    # Update existing repository
                    result = await asyncio.create_subprocess_exec(
                        "git", "pull",
                        cwd=server_dir,
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                else:
                    result = await asyncio.create_subprocess_exec(
                        "git", "clone", str(server_info.repository_url), str(server_dir),
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE
                    )
                
                await result.communicate()
                
                if result.returncode != 0:
                    return InstallationResult(
                        success=False,
                        server_id=server_info.id,
                        version=version,
                        message="Failed to clone repository"
                    )
                
                progress.update(task, description=f"✅ Cloned {server_info.id}")
                
                return InstallationResult(
                    success=True,
                    server_id=server_info.id,
                    version=version,
                    message=f"Successfully cloned {server_info.id}",
                    config=ServerConfig(
                        name=server_info.name,
                        server_id=server_info.id,
                        type=ServerType.GITHUB,
                        working_dir=str(server_dir)
                    )
                )
            
            except Exception as e:
                return InstallationResult(
                    success=False,
                    server_id=server_info.id,
                    version=version,
                    message=f"GitHub installation error: {e}"
                )
    
    async def _install_docker_server(
        self, 
        server_info: ServerInfo, 
        version: str
    ) -> InstallationResult:
        """Install Docker-based MCP server."""
        if not server_info.docker_image:
            return InstallationResult(
                success=False,
                server_id=server_info.id,
                version=version,
                message="No Docker image provided"
            )
        
        image_name = f"{server_info.docker_image}:{version}"
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task(f"Pulling {image_name}...", total=None)
            
            try:
                result = await asyncio.create_subprocess_exec(
                    "docker", "pull", image_name,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                )
                
                stdout, stderr = await result.communicate()
                
                if result.returncode == 0:
                    progress.update(task, description=f"✅ Pulled {image_name}")
                    return InstallationResult(
                        success=True,
                        server_id=server_info.id,
                        version=version,
                        message=f"Successfully pulled {image_name}",
                        config=ServerConfig(
                            name=server_info.name,
                            server_id=server_info.id,
                            type=ServerType.DOCKER,
                            command="docker",
                            args=["run", "-i", "--rm", image_name]
                        )
                    )
                else:
                    error_msg = stderr.decode() if stderr else "Unknown error"
                    return InstallationResult(
                        success=False,
                        server_id=server_info.id,
                        version=version,
                        message=f"Docker pull failed: {error_msg}"
                    )
            
            except Exception as e:
                return InstallationResult(
                    success=False,
                    server_id=server_info.id,
                    version=version,
                    message=f"Docker installation error: {e}"
                )
    
    async def _run_server_process(
        self, 
        config: ServerConfig, 
        server_info: ServerInfo
    ) -> None:
        """Run the actual server process."""
        # Build command
        cmd = self._build_server_command(config, server_info)
        
        # Build environment
        env = os.environ.copy()
        if config.api_key:
            env[f"{server_info.id.upper().replace('-', '_')}_API_KEY"] = config.api_key
        env.update(config.env)
        
        self.logger.info(f"Starting server: {' '.join(cmd)}")
        
        try:
            # Start process
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
                env=env,
                cwd=config.working_dir
            )
            
            # Wait for process to complete
            await process.communicate()
            
            if process.returncode != 0:
                self.logger.error(f"Server exited with code {process.returncode}")
            else:
                self.logger.info("Server completed successfully")
        
        except Exception as e:
            self.logger.error(f"Failed to run server process: {e}")
            raise
    
    def _build_server_command(
        self, 
        config: ServerConfig, 
        server_info: ServerInfo
    ) -> List[str]:
        """Build the command to run the server."""
        if config.command:
            cmd = [config.command] + config.args
        elif server_info.type == ServerType.NPM:
            package_name = server_info.package_name or server_info.id
            cmd = ["npx", "-y", package_name]
        elif server_info.type == ServerType.PYPI:
            package_name = server_info.package_name or server_info.id
            cmd = ["uvx", package_name]
        elif server_info.type == ServerType.DOCKER:
            if not server_info.docker_image:
                raise ServerManagerError("No Docker image specified")
            cmd = ["docker", "run", "-i", "--rm", server_info.docker_image]
        else:
            raise ServerManagerError(f"Unsupported server type: {server_info.type}")
        
        # Add custom arguments
        cmd.extend(config.args)
        
        return cmd
    
    async def _is_server_installed(self, server_info: ServerInfo) -> bool:
        """Check if a server is already installed."""
        try:
            if server_info.type == ServerType.NPM:
                package_name = server_info.package_name or server_info.id
                result = await asyncio.create_subprocess_exec(
                    "npx", "-y", package_name, "--help",
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL
                )
                await result.communicate()
                return result.returncode == 0
            
            elif server_info.type == ServerType.PYPI:
                package_name = server_info.package_name or server_info.id
                result = await asyncio.create_subprocess_exec(
                    "uvx", package_name, "--help",
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL
                )
                await result.communicate()
                return result.returncode == 0
            
            elif server_info.type == ServerType.GITHUB:
                server_dir = self.servers_dir / server_info.id
                return server_dir.exists() and server_dir.is_dir()
            
            elif server_info.type == ServerType.DOCKER:
                if not server_info.docker_image:
                    return False
                result = await asyncio.create_subprocess_exec(
                    "docker", "image", "inspect", server_info.docker_image,
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL
                )
                await result.communicate()
                return result.returncode == 0
            
            return False
        
        except Exception:
            return False 