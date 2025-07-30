import os

from fastmcp import FastMCP


API_TOKEN = os.getenv('API_TOKEN')


def create_mcp_proxy(name, backend_url, backend_token):
    api_token = backend_token or API_TOKEN
    headers = {}
    if api_token:
        headers["Authorization"] = f"Bearer {api_token}"

    config = {
        "mcpServers": {
            "default": {  # For single server configs, 'default' is commonly used
                "url": backend_url,
                "transport": "streamable-http",
                "headers": headers,
            }
        }
    }

    proxy = FastMCP.as_proxy(config, name=name)
    return proxy


def run_proxy_stdio(name, backend_url, backend_token):
    proxy = create_mcp_proxy(name, backend_url, backend_token)
    proxy.run()


def run_proxy_streamable_http(name, backend_url, backend_token, port):
    proxy = create_mcp_proxy(name, backend_url, backend_token)
    proxy.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
    )

