import argparse
import os

from . import mcp


def run_http():
    host = os.getenv("SERVER_HOST", "127.0.0.1")
    port = int(os.getenv("SERVER_PORT", "9341"))
    mcp.run(transport="http", host=host, port=port, path="/")


def run_other(transport: str):
    """Run the FastMCP server. Note this is a synchronous function.

    Args:
        transport: Transport protocol to use ("stdio", "sse")
    """
    mcp.run(transport=transport)


def main():
    parser = argparse.ArgumentParser(description="Run MCP Server")
    parser.add_argument(
        "--transport",
        choices=["http", "stdio", "sse"],
        default="stdio",
        help="Transport protocol",
    )
    args = parser.parse_args()
    if args.transport == "http":
        run_http()
    else:
        run_other(args.transport)


if __name__ == "__main__":
    main()
