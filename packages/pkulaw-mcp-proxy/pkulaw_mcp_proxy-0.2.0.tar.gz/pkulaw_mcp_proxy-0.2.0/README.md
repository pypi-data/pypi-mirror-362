# PKULAW MCP server proxy

Proxy existing MCP servers for bridging transports - exposing a server running on streamable-http to a different transport. 


## Usage

Run (exposing streamable-http):

    uv run pkulaw-mcp-proxy \
    --type streamable-http \
    --name proxy-mcp-server \
    --backend-url http://${URL}:3000/mcp \
    --backend-token xxxxxx \
    --port 3000


Run (exposing stdio):

    uv run pkulaw-mcp-proxy \
    --name proxy-mcp-server \
    --backend-url http://${URL}:3000/mcp


