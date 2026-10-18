from mcp.server import MCPServer

mcp = MCPServer("devdocs-hub")

@mcp.tool()
def health():
    return { 'status' : 'ok' }
