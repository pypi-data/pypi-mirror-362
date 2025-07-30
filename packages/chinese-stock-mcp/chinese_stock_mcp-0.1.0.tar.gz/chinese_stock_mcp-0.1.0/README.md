# 股票数据 MCP Server

## 🚀 快速开始

### 手动安装
使用 uv:

```bash
uv tool install china-stock-mcp
```

### 🔌 MCP 集成

将此配置添加到您的 MCP 客户端配置文件中：

```json
{
    "mcpServers": {
        "china-stock-mcp": {
            "command": "uv",
            "args": [
                "tool",
                "run",
                "china-stock-mcp"
            ]
        }
    }
}
```
