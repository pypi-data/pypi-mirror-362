"""Interactive server inspection for Agentrix."""

import asyncio
import json
from typing import Dict, List, Optional, Any

from rich.console import Console
from rich.prompt import Prompt, Confirm
from rich.table import Table
from rich.panel import Panel
from rich.json import JSON

from ..models.config import AgentrixConfig
from ..models.server import ServerInfo, ToolInfo
from ..utils.logger import get_logger, LoggerMixin

logger = get_logger(__name__)
console = Console()


class ServerInspector(LoggerMixin):
    """Interactive server inspection and testing."""
    
    def __init__(self, config: AgentrixConfig):
        self.config = config
        self.current_server: Optional[ServerInfo] = None
    
    async def inspect_server(self, server: ServerInfo) -> None:
        """Start interactive inspection of a server."""
        self.current_server = server
        
        console.print(f"\n🔍 [bold cyan]Interactive Inspection: {server.name}[/bold cyan]")
        console.print(f"Server ID: {server.id}")
        console.print(f"Version: {server.version}")
        console.print(f"Type: {server.type.value}")
        
        while True:
            try:
                choice = await self._show_inspection_menu()
                
                if choice == "1":
                    await self._show_server_details()
                elif choice == "2":
                    await self._list_tools()
                elif choice == "3":
                    await self._test_tool()
                elif choice == "4":
                    await self._show_requirements()
                elif choice == "5":
                    await self._test_connection()
                elif choice == "6":
                    await self._show_configuration_help()
                elif choice == "0":
                    break
                else:
                    console.print("❌ Invalid choice", style="red")
                
                # Pause before showing menu again
                if choice != "0":
                    input("\nPress Enter to continue...")
            
            except KeyboardInterrupt:
                break
        
        console.print("\n👋 Exiting inspection mode")
    
    async def _show_inspection_menu(self) -> str:
        """Show the inspection menu and get user choice."""
        console.print("\n" + "="*50)
        console.print("🔍 [bold]Inspection Menu[/bold]")
        console.print("="*50)
        
        table = Table(show_header=False, box=None)
        table.add_column("Option", style="cyan", width=8)
        table.add_column("Description", style="white")
        
        table.add_row("1", "📋 Show detailed server information")
        table.add_row("2", "🔧 List available tools")
        table.add_row("3", "🧪 Test a tool interactively")
        table.add_row("4", "📦 Show requirements and dependencies")
        table.add_row("5", "🔗 Test server connection")
        table.add_row("6", "💡 Show configuration help")
        table.add_row("0", "❌ Exit inspection")
        
        console.print(table)
        
        return Prompt.ask("\n[cyan]Choose an option[/cyan]", choices=["0", "1", "2", "3", "4", "5", "6"])
    
    async def _show_server_details(self) -> None:
        """Show detailed server information."""
        if not self.current_server:
            return
        
        server = self.current_server
        
        console.print(f"\n📋 [bold]Detailed Server Information[/bold]")
        
        details = Table(show_header=False, box=None)
        details.add_column("Field", style="cyan", width=20)
        details.add_column("Value", style="white")
        
        details.add_row("Name", server.name)
        details.add_row("ID", server.id)
        details.add_row("Version", server.version)
        details.add_row("Author", server.author)
        details.add_row("Type", server.type.value)
        details.add_row("Description", server.description)
        
        if server.package_name:
            details.add_row("Package", server.package_name)
        
        if server.repository_url:
            details.add_row("Repository", str(server.repository_url))
        
        if server.docker_image:
            details.add_row("Docker Image", server.docker_image)
        
        details.add_row("Downloads", f"{server.downloads:,}")
        details.add_row("Stars", str(server.stars))
        details.add_row("Categories", ", ".join(server.categories) if server.categories else "None")
        details.add_row("Tags", ", ".join(server.tags) if server.tags else "None")
        
        console.print(details)
        
        # Show authentication requirements
        if server.auth.required:
            console.print(f"\n🔐 [yellow]Authentication Required[/yellow]")
            if server.auth.api_key_env:
                console.print(f"   Environment variable: {server.auth.api_key_env}")
            if server.auth.scopes:
                console.print(f"   Required scopes: {', '.join(server.auth.scopes)}")
    
    async def _list_tools(self) -> None:
        """List all available tools."""
        if not self.current_server or not self.current_server.tools:
            console.print("❌ No tools information available", style="yellow")
            return
        
        console.print(f"\n🔧 [bold]Available Tools ({len(self.current_server.tools)})[/bold]")
        
        for i, tool in enumerate(self.current_server.tools, 1):
            console.print(f"\n{i}. [cyan]{tool.name}[/cyan]")
            console.print(f"   {tool.description}")
            
            if tool.input_schema:
                console.print("   [dim]Input schema available[/dim]")
    
    async def _test_tool(self) -> None:
        """Interactively test a tool."""
        if not self.current_server or not self.current_server.tools:
            console.print("❌ No tools available for testing", style="yellow")
            return
        
        # Let user select a tool
        console.print(f"\n🧪 [bold]Tool Testing[/bold]")
        console.print("Available tools:")
        
        for i, tool in enumerate(self.current_server.tools, 1):
            console.print(f"  {i}. {tool.name}")
        
        try:
            choice = int(Prompt.ask("Select tool number", default="1"))
            if 1 <= choice <= len(self.current_server.tools):
                tool = self.current_server.tools[choice - 1]
                await self._test_specific_tool(tool)
            else:
                console.print("❌ Invalid tool selection", style="red")
        except ValueError:
            console.print("❌ Invalid input", style="red")
    
    async def _test_specific_tool(self, tool: ToolInfo) -> None:
        """Test a specific tool."""
        console.print(f"\n🧪 Testing tool: [cyan]{tool.name}[/cyan]")
        console.print(f"Description: {tool.description}")
        
        # Show input schema if available
        if tool.input_schema:
            console.print("\n📝 Input Schema:")
            console.print(JSON(json.dumps(tool.input_schema, indent=2)))
            
            if Confirm.ask("\nWould you like to provide input parameters?"):
                params = self._collect_tool_parameters(tool.input_schema)
                console.print(f"\n📤 Tool call parameters:")
                console.print(JSON(json.dumps(params, indent=2)))
                
                # Note: In a real implementation, we would actually call the tool here
                console.print("\n💡 [yellow]Note: Actual tool execution requires a running server instance.[/yellow]")
        else:
            console.print("\n💡 [yellow]No input schema available for this tool.[/yellow]")
    
    def _collect_tool_parameters(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """Collect parameters for tool testing."""
        params = {}
        
        properties = schema.get("properties", {})
        required = schema.get("required", [])
        
        for param_name, param_info in properties.items():
            param_type = param_info.get("type", "string")
            param_desc = param_info.get("description", "")
            is_required = param_name in required
            
            prompt_text = f"{param_name}"
            if param_desc:
                prompt_text += f" ({param_desc})"
            if is_required:
                prompt_text += " [required]"
            
            try:
                value = Prompt.ask(prompt_text, default="" if not is_required else None)
                
                if value:
                    # Try to convert to appropriate type
                    if param_type == "integer":
                        params[param_name] = int(value)
                    elif param_type == "number":
                        params[param_name] = float(value)
                    elif param_type == "boolean":
                        params[param_name] = value.lower() in ["true", "yes", "1", "on"]
                    else:
                        params[param_name] = value
            except ValueError as e:
                console.print(f"❌ Invalid value for {param_name}: {e}", style="red")
        
        return params
    
    async def _show_requirements(self) -> None:
        """Show server requirements and dependencies."""
        if not self.current_server:
            return
        
        server = self.current_server
        
        console.print(f"\n📦 [bold]Requirements and Dependencies[/bold]")
        
        # System requirements
        requirements = []
        if server.python_version:
            requirements.append(f"Python {server.python_version}")
        if server.node_version:
            requirements.append(f"Node.js {server.node_version}")
        
        if requirements:
            console.print(f"\n🔧 Runtime Requirements:")
            for req in requirements:
                console.print(f"  • {req}")
        
        # Dependencies
        if server.dependencies:
            console.print(f"\n📚 System Dependencies:")
            for dep in server.dependencies:
                console.print(f"  • {dep}")
        
        # Installation command
        console.print(f"\n💻 Installation Command:")
        if server.type.value == "npm":
            package = server.package_name or server.id
            console.print(f"  npx -y {package}")
        elif server.type.value == "pypi":
            package = server.package_name or server.id
            console.print(f"  uvx {package}")
        elif server.type.value == "docker":
            if server.docker_image:
                console.print(f"  docker run -i --rm {server.docker_image}")
        elif server.type.value == "github":
            if server.repository_url:
                console.print(f"  git clone {server.repository_url}")
        
        if not requirements and not server.dependencies:
            console.print("✅ No special requirements")
    
    async def _test_connection(self) -> None:
        """Test connection to the server."""
        if not self.current_server:
            return
        
        console.print(f"\n🔗 [bold]Testing Server Connection[/bold]")
        console.print("💡 [yellow]This would attempt to start the server and test connectivity.[/yellow]")
        console.print("💡 [yellow]In a real implementation, this would:[/yellow]")
        console.print("   • Install the server if not present")
        console.print("   • Start the server process")
        console.print("   • Test MCP protocol handshake")
        console.print("   • Verify tool availability")
        console.print("   • Clean up the test instance")
        
        # This is a placeholder for actual connection testing
        console.print("\n⚠️  [yellow]Connection testing not yet implemented[/yellow]")
    
    async def _show_configuration_help(self) -> None:
        """Show configuration help for the server."""
        if not self.current_server:
            return
        
        server = self.current_server
        
        console.print(f"\n💡 [bold]Configuration Help[/bold]")
        
        # Installation command
        console.print(f"\n📦 To install this server:")
        console.print(f"  [cyan]agentrix install {server.id} --client cursor[/cyan]")
        
        # Authentication setup
        if server.auth.required:
            console.print(f"\n🔐 Authentication setup:")
            if server.auth.api_key_env:
                console.print(f"  Set environment variable: [cyan]{server.auth.api_key_env}[/cyan]")
            console.print(f"  Or provide API key: [cyan]--key your-api-key[/cyan]")
        
        # Configuration example
        console.print(f"\n⚙️  Configuration example:")
        config_example = {
            "command": "uvx",
            "args": ["agentrix", "run", server.id]
        }
        
        if server.auth.required:
            config_example["args"].extend(["--key", "your-api-key"])
        
        console.print(JSON(json.dumps(config_example, indent=2)))
        
        # Direct run command
        console.print(f"\n🚀 To run directly:")
        run_cmd = f"agentrix run {server.id}"
        if server.auth.required:
            run_cmd += " --key your-api-key"
        console.print(f"  [cyan]{run_cmd}[/cyan]") 