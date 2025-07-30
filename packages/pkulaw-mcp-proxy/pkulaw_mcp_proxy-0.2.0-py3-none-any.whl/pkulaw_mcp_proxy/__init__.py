import argparse

from .proxy import run_proxy_stdio
from .proxy import run_proxy_streamable_http


def main():
    parser = argparse.ArgumentParser(description="PKULAW MCP server proxy")
    parser.add_argument(
        "--type",
        type=str,
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="MCP server type of the proxied MCP server",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="mcp-server",
        help="MCP server name of the proxied MCP server",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=3000,
        help="Port to run the proxied MCP server with type streamable-http",
    )
    parser.add_argument(
        "--backend-url",
        type=str,
        help="URL of the backend MCP server",
    )
    parser.add_argument(
        "--backend-token",
        type=str,
        default='',
        help="Token for the backend MCP server",
    )
    args = parser.parse_args()

    if args.type == "stdio":
        run_proxy_stdio(args.name, args.backend_url, args.backend_token)
    else:
        run_proxy_streamable_http(args.name, args.backend_url, args.backend_token, args.port)


if __name__ == "__main__":
    main()

