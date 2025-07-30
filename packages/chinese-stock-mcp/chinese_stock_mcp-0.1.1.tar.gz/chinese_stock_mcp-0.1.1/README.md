# 股票数据 MCP Server

基于 [pysnowball](https://github.com/uname-yang/pysnowball) 库的 MCP Server，用于获取中国股票市场数据。
该 MCP 服务器能力参考 [pysnowball](https://github.com/uname-yang/pysnowball) 。

## 🚀 快速开始

### 手动安装
使用 uv:

```bash
uv tool install chinese-stock-mcp
```

### 🔌 MCP 集成

将此配置添加到您的 MCP 客户端配置文件中：

```json
{
    "mcpServers": {
        "chinese-stock-mcp": {
            "command": "uv",
            "args": [
                "tool",
                "run",
                "chinese-stock-mcp",
                "--token",
                "xueqiu-token"
            ]
        }
    }
}
```

注：
  - 如果不设置 `--token` 参数，很多功能将无法使用。 
  - [如何获取雪球的 Token](https://blog.crackcreed.com/diy-xue-qiu-app-shu-ju-api/)
