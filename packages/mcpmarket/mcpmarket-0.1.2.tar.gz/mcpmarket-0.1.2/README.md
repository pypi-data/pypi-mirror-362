# 🤖 Agentrix

**Python MCP 服务器注册表和代理，专为 AI 智能体设计**

Agentrix 是一个功能强大的 Python 工具，类似于 [@smithery/cli](https://smithery.ai)，用于管理和代理 Model Context Protocol (MCP) 服务器。它提供了服务器发现、安装、配置和运行的完整解决方案。

## ✨ 特性

- 🔍 **服务器发现**: 从中央注册表搜索和发现 MCP 服务器
- 📦 **一键安装**: 自动安装和配置 MCP 服务器到各种客户端
- 🔧 **多客户端支持**: 支持 Cursor、Claude Desktop、VS Code 等
- 🚀 **代理模式**: 作为 MCP 服务器代理运行
- 🛠️ **多语言支持**: 支持 NPM、PyPI、GitHub、Docker 等多种服务器类型
- 📊 **统计信息**: 提供注册表统计和服务器信息
- 🎨 **美观界面**: 使用 Rich 提供美观的命令行界面

## 🚀 快速开始

### 安装

使用 `uv` 安装 (推荐):

```bash
uv add agentrix
```

或使用 `pip`:

```bash
pip install agentrix
```

### 基本使用

1. **搜索服务器**:
```bash
agentrix search weather
agentrix search --category "productivity" --type npm
```

2. **查看服务器信息**:
```bash
agentrix info @turkyden/weather
```

3. **安装服务器到客户端**:
```bash
# 安装到 Cursor
agentrix install @turkyden/weather --client cursor --key your-api-key

# 安装到 Claude Desktop
agentrix install @smithery-ai/brave-search --client claude --key your-api-key
```

4. **列出已安装的服务器**:
```bash
# 列出所有客户端
agentrix list

# 列出特定客户端的服务器
agentrix list --client cursor

# 列出所有客户端的服务器
agentrix list --all
```

5. **卸载服务器**:
```bash
agentrix uninstall weather --client cursor
```

## 🔧 配置

### 客户端配置

Agentrix 支持以下 MCP 客户端：

| 客户端 | 配置文件路径 | 格式 |
|--------|-------------|------|
| Cursor | `~/.cursor/mcp.json` | JSON |
| Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` | JSON |
| VS Code | `~/.vscode/settings.json` | JSON |

### 环境变量

可以通过环境变量配置 Agentrix：

```bash
export AGENTRIX_REGISTRY__URL="https://registry.agentrix.dev"
export AGENTRIX_REGISTRY__API_KEY="your-api-key"
export AGENTRIX_LOGGING__LEVEL="DEBUG"
```

### 配置文件

创建 `~/.agentrix/config.toml` 进行自定义配置：

```toml
[registry]
url = "https://registry.agentrix.dev"
api_key = "your-api-key"
cache_ttl = 3600

[logging]
level = "INFO"
console_enabled = true
log_file = "~/.agentrix/logs/agentrix.log"

[proxy]
host = "127.0.0.1"
port = 8080
enable_auth = false
```

## 🏗️ 架构设计

### 代理模式

类似于 @smithery/cli，Agentrix 使用代理模式运行：

1. **客户端配置**: MCP 客户端配置指向 `agentrix run <server-id>`
2. **代理启动**: Agentrix 接收请求并启动目标 MCP 服务器
3. **透明代理**: 所有 MCP 通信透明地转发到目标服务器

```json
{
  "mcpServers": {
    "weather": {
      "command": "uvx",
      "args": [
        "agentrix",
        "run", 
        "@turkyden/weather",
        "--key",
        "your-api-key"
      ]
    }
  }
}
```

### 调用流程

```
Cursor/Claude Desktop → agentrix run → Target MCP Server
     ↑                      ↓              ↓
     ←─── MCP Protocol ─────┴──────────────┘
```

## 📚 高级用法

### 运行服务器 (代理模式)

```bash
# 直接运行服务器
agentrix run @turkyden/weather --key your-api-key

# 使用配置字符串
agentrix run @turkyden/weather --config '{"env":{"API_TIMEOUT":"30"}}'
```

### 查看统计信息

```bash
# 注册表统计
agentrix stats

# 可用分类
agentrix categories

# 精选服务器
agentrix featured
```

### 缓存管理

```bash
# 清除缓存
agentrix clear-cache
```

## 🛠️ 开发

### 项目结构

```
src/agentrix/
├── __init__.py              # 包初始化
├── cli.py                   # CLI 界面
├── core/                    # 核心功能
│   ├── config.py           # 配置管理
│   ├── registry.py         # 服务器注册表
│   ├── server_manager.py   # 服务器管理
│   └── proxy.py            # MCP 代理
├── models/                  # 数据模型
│   ├── config.py           # 配置模型
│   └── server.py           # 服务器模型
└── utils/                   # 工具函数
    └── logger.py           # 日志工具
```

### 开发环境设置

```bash
# 克隆项目
git clone https://github.com/agentrix-ai/agentrix.git
cd agentrix

# 创建虚拟环境
uv venv
source .venv/bin/activate

# 安装依赖
uv sync --all-extras

# 运行测试
pytest

# 代码格式化
black src tests
ruff check src tests --fix
```

### 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

## 📋 命令参考

### 全局选项

- `--verbose, -v`: 启用详细日志
- `--debug`: 启用调试模式
- `--config`: 指定配置文件路径

### 命令列表

| 命令 | 描述 | 示例 |
|------|------|------|
| `search [query]` | 搜索服务器 | `agentrix search weather` |
| `info <server-id>` | 显示服务器信息 | `agentrix info @turkyden/weather` |
| `install <server-id>` | 安装服务器 | `agentrix install @turkyden/weather --client cursor` |
| `uninstall <server-name>` | 卸载服务器 | `agentrix uninstall weather --client cursor` |
| `list` | 列出客户端或服务器 | `agentrix list --client cursor` |
| `run <server-id>` | 运行服务器 | `agentrix run @turkyden/weather --key api-key` |
| `featured` | 显示精选服务器 | `agentrix featured` |
| `categories` | 显示分类 | `agentrix categories` |
| `stats` | 显示统计信息 | `agentrix stats` |
| `clear-cache` | 清除缓存 | `agentrix clear-cache` |
| `version` | 显示版本信息 | `agentrix version` |

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🤝 致谢

- 感谢 [Smithery](https://smithery.ai) 提供的设计灵感
- 感谢 [Anthropic](https://anthropic.com) 开发的 Model Context Protocol
- 感谢所有贡献者和用户的支持

## 🔗 相关链接

- [MCP 官方文档](https://modelcontextprotocol.io)
- [Smithery 官网](https://smithery.ai)
- [问题反馈](https://github.com/agentrix-ai/agentrix/issues)
- [讨论区](https://github.com/agentrix-ai/agentrix/discussions) 