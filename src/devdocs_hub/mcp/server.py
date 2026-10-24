from devdocs_hub.mcp.resources.documents import register_document_resources
from devdocs_hub.mcp.tools.documents import register_document_tools
from mcp.server import MCPServer
from devdocs_hub.rag.embeddings import get_embedding_provider

mcp = MCPServer("devdocs-hub")

@mcp.tool()
def health() -> dict[str, str]:
    """Check that the DevDocs Hub MCP server is available."""
    return {"status": "ok"}

register_document_tools(mcp)
register_document_resources(mcp)


def main() -> None:
    """Run the MCP server over stdio for local MCP clients."""
    get_embedding_provider()
    mcp.run(transport="stdio")

if __name__ == '__main__':
    main()
