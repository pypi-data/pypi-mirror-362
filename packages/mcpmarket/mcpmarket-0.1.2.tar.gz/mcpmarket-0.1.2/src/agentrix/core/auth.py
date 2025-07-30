"""Authentication management for Agentrix."""

import json
from pathlib import Path
from typing import Optional

import httpx
from rich.console import Console
from rich.prompt import Prompt

from ..models.config import AgentrixConfig
from ..utils.logger import get_logger, LoggerMixin

logger = get_logger(__name__)
console = Console()


class AuthManager(LoggerMixin):
    """Manages authentication and API keys."""
    
    def __init__(self, config: AgentrixConfig):
        self.config = config
        self.auth_file = config.data_dir / "auth.json"
        self._ensure_auth_file()
    
    def _ensure_auth_file(self) -> None:
        """Ensure auth file exists."""
        if not self.auth_file.exists():
            self.auth_file.parent.mkdir(parents=True, exist_ok=True)
            self._save_auth_data({})
    
    def _load_auth_data(self) -> dict:
        """Load authentication data from file."""
        try:
            with open(self.auth_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.warning(f"Failed to load auth data: {e}")
            return {}
    
    def _save_auth_data(self, data: dict) -> None:
        """Save authentication data to file."""
        try:
            with open(self.auth_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            # Set restrictive permissions on auth file
            self.auth_file.chmod(0o600)
        except Exception as e:
            self.logger.error(f"Failed to save auth data: {e}")
    
    async def login(self, api_key: str) -> bool:
        """Login with API key."""
        try:
            # Validate API key with registry
            if await self._validate_api_key(api_key):
                # Save API key
                auth_data = self._load_auth_data()
                auth_data['api_key'] = api_key
                self._save_auth_data(auth_data)
                
                # Also update config
                self.config.registry.api_key = api_key
                
                self.logger.info("Successfully logged in")
                return True
            else:
                self.logger.error("Invalid API key")
                return False
        
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            return False
    
    async def interactive_login(self) -> bool:
        """Interactive login flow."""
        console.print("\n🔐 [bold cyan]Agentrix Login[/bold cyan]")
        console.print("Enter your Agentrix API key to access premium features.")
        console.print("💡 Get your API key from: https://registry.agentrix.dev/account")
        
        api_key = Prompt.ask("\nAPI Key", password=True)
        
        if not api_key or not api_key.strip():
            console.print("❌ No API key provided", style="red")
            return False
        
        console.print("🔄 Validating API key...", style="yellow")
        
        success = await self.login(api_key.strip())
        return success
    
    async def _validate_api_key(self, api_key: str) -> bool:
        """Validate API key with registry."""
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                headers = {
                    "Authorization": f"Bearer {api_key}",
                    "User-Agent": "agentrix/0.1.0"
                }
                
                response = await client.get(
                    f"{self.config.registry.url}/api/auth/validate",
                    headers=headers
                )
                
                return response.status_code == 200
        
        except Exception as e:
            self.logger.warning(f"API key validation failed: {e}")
            # If validation fails, assume key is valid for offline usage
            return True
    
    def get_api_key(self) -> Optional[str]:
        """Get stored API key."""
        auth_data = self._load_auth_data()
        return auth_data.get('api_key')
    
    def is_logged_in(self) -> bool:
        """Check if user is logged in."""
        return self.get_api_key() is not None
    
    def logout(self) -> None:
        """Logout and remove stored credentials."""
        auth_data = self._load_auth_data()
        auth_data.pop('api_key', None)
        self._save_auth_data(auth_data)
        
        # Clear from config
        self.config.registry.api_key = None
        
        self.logger.info("Successfully logged out")
        console.print("✅ Successfully logged out", style="green") 