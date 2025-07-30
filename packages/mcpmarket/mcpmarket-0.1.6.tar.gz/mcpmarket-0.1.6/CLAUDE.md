# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agentrix is a Python MCP (Model Context Protocol) server registry and proxy, similar to @smithery/cli. It provides server discovery, installation, configuration and runtime management for AI agents. The project is published as "mcpmarket" on PyPI but internally uses "agentrix" as the package name.

## Development Commands

### Setup and Installation
```bash
# Install dependencies (uses uv for package management)
uv sync --all-extras

# Install development dependencies only
uv sync --extra dev

# Install in development mode
uv pip install -e .
```

### Testing
```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=agentrix --cov-report=html

# Run specific test file
pytest tests/test_filename.py

# Run tests excluding slow tests
pytest -m "not slow"
```

### Code Quality
```bash
# Format code
black src tests

# Lint code
ruff check src tests

# Fix linting issues
ruff check src tests --fix

# Type checking
mypy src
```

### Build and Distribution
```bash
# Build package
python -m build

# Publish (development)
python scripts/publish.py

# Publish (production)
./publish.sh
```

## Architecture

### Core Components

1. **CLI Interface (`cli.py`)**: Main command-line interface using Typer
   - Entry point: `mcpmarket` command (defined in pyproject.toml)
   - Commands: search, install, uninstall, run, dev, build, playground, etc.

2. **Registry System (`core/registry.py`)**: 
   - Manages server discovery from central registry
   - Handles caching and server metadata
   - Supports search, filtering, and server information retrieval

3. **Server Manager (`core/server_manager.py`)**:
   - Handles server installation (NPM, PyPI, GitHub, Docker)
   - Manages server lifecycle and runtime
   - Implements proxy mode for MCP communication

4. **Configuration Manager (`core/config.py`)**:
   - Manages client configurations (Cursor, Claude Desktop, VS Code)
   - Handles JSON/TOML config file operations
   - Supports backup and restore operations

5. **MCP Proxy (`core/mcp_proxy.py`)**:
   - Core proxy functionality for MCP protocol
   - Transparent communication between clients and servers
   - Handles server process management

### Key Design Patterns

**Proxy Architecture**: Similar to @smithery/cli, Agentrix uses a proxy pattern where:
- MCP clients are configured to run `agentrix run <server-id>`
- Agentrix receives the request and starts the target MCP server
- All MCP communication is transparently forwarded

**Server Types**: Supports multiple server distribution methods:
- `NPM`: JavaScript/Node.js packages via npx
- `PYPI`: Python packages via uvx
- `GITHUB`: Git repositories (cloned locally)
- `DOCKER`: Docker containers

**Configuration Flow**:
1. Client config files are read/written (JSON/TOML)
2. Server configurations are injected with proxy commands
3. Environment variables and API keys are managed automatically

### Data Models

Located in `models/` directory:
- `config.py`: Configuration classes (AgentrixConfig, ClientConfig, etc.)
- `server.py`: Server-related models (ServerInfo, ServerConfig, ServerInstance)

## Common Development Patterns

### Adding New Commands
1. Add command function to `cli.py` with `@app.command()` decorator
2. Create async implementation function (e.g., `_command_name`)
3. Add error handling and logging
4. Update help text and examples

### Server Type Support
To add a new server type:
1. Add enum value to `ServerType` in `models/server.py`
2. Implement installation logic in `server_manager.py`
3. Add command building logic in `_build_server_command`
4. Update registry search and filtering

### Client Configuration
To add a new MCP client:
1. Add client configuration to `AgentrixConfig.get_default_client_configs()`
2. Ensure config format (JSON/TOML) is supported
3. Test configuration read/write operations

## Key Entry Points

- **Main CLI**: `agentrix.cli:main_cli` (defined in pyproject.toml scripts)
- **Config Loading**: `get_config()` in `cli.py` 
- **Server Proxy**: `run_server_proxy()` in `server_manager.py`
- **Registry Operations**: `ServerRegistry` class methods

## Configuration Files

- Main config: `~/.agentrix/config.toml`
- Client configs: Various paths (see `example.config.toml`)
- Cache: `~/.agentrix/cache/servers.json`

## Development vs Production

- Development mode: `config.dev_mode = True`
- Debug logging: `config.debug = True`
- Registry URL: Configurable via `config.registry.url`

## Testing Strategy

- Unit tests for core functionality
- Integration tests for server installation/management
- Async test support with pytest-asyncio
- Coverage reporting with pytest-cov
- Slow tests marked with `@pytest.mark.slow`