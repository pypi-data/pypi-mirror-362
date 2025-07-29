# Jay MCP

A demo MCP (Model Context Protocol) server with tools and resources for demonstration purposes.

## Features

- **Tools**: Mathematical operations and server information
- **Resources**: Personalized greetings and server documentation
- **Easy to use**: Simple command-line interface
- **Extensible**: Modular design for easy customization

## Installation

### Quick Install from PyPI

```bash
pip install jay-mcp
```

### MCP Client Installation (Recommended)

For MCP clients, use uvx for automatic latest version loading:

```bash
uvx install jay-mcp
```

### GitHub Token Configuration

Configure your GitHub token for higher API rate limits (5000/hour vs 60/hour):

```bash
# Method 1: Environment variable
export GITHUB_TOKEN="your_github_token_here"

# Method 2: .env file
echo "GITHUB_TOKEN=your_github_token_here" > .env
```

Get your token at: [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)

### From Source

```bash
git clone https://github.com/your-username/jay-mcp.git
cd jay-mcp
pip install -e .
```

## Usage

### As an MCP Server

```bash
# Start the MCP server
python -m jay_mcp.cli

# Check version
python -m jay_mcp.cli --version
```

### MCP Client Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "jay-mcp": {
      "command": "uvx",
      "args": ["jay-mcp"],
      "env": {
        "GITHUB_TOKEN": "your_github_token_here"
      }
    }
  }
}
```

### AI Usage Examples

Once configured, you can use these commands in your AI client:

- "获取 React 的 GitHub 仓库信息"
- "比较这些项目的 star 数：facebook/react, vuejs/vue"
- "查询 microsoft/vscode 的详细信息"
- "分析这些机器学习项目：tensorflow/tensorflow, pytorch/pytorch"

## Available Tools

- **batch_get_repo_info(repos)**: 批量获取GitHub仓库信息
  - 参数: `repos` - 仓库列表，格式：["owner/repo", ...]
  - 返回: 包含仓库详细信息的字典列表
  - 功能: 并行查询多个GitHub仓库的基本信息（stars、forks、语言等）
  - 限制: 单次最多查询50个仓库

## Available Resources

- **greeting://{name}**: Get a personalized greeting
- **info://server**: Get server information and documentation

## Development

### Setup Development Environment

```bash
git clone https://github.com/your-username/jay-mcp.git
cd jay-mcp
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black jay_mcp/
isort jay_mcp/
```

### Type Checking

```bash
mypy jay_mcp/
```

## MCP Client Configuration

To use jay-mcp with an MCP client, add this configuration to your MCP settings:

```json
{
  "mcpServers": {
    "jay-mcp": {
      "command": "uvx",
      "args": ["jay-mcp@latest"],
      "description": "Jay MCP Demo Server - Auto-updates to latest version"
    }
  }
}
```

The `@latest` tag ensures you always get the newest version automatically.

For a complete configuration example with tool and resource definitions, see [mcp_config.json](mcp_config.json).

## Advanced Configuration

You can also create a custom server instance programmatically:

```python
from jay_mcp.server import create_server

# Create a custom server
server = create_server("My Custom MCP Server")
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

### 0.1.0 (2025-07-14)

- Initial release
- Basic MCP server with tools and resources
- Command-line interface
- PyPI package support
