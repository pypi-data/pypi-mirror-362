from fastmcp import FastMCP
from fastmcp.server.proxy import ProxyClient


def create_mcp_proxy(name, backend_url):
    backend = ProxyClient(backend_url)
    proxy = FastMCP.as_proxy(
        backend=backend,
        name=name,
    )
    return proxy


def run_proxy_stdio(name, backend_url):
    proxy = create_mcp_proxy(name, backend_url)
    proxy.run()


def run_proxy_streamable_http(name, backend_url, port):
    proxy = create_mcp_proxy(name, backend_url)
    proxy.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=port,
    )

