from devdocs_hub.domain.documents import Document
from devdocs_hub.mcp.dependencies import document_repository_context, get_document_repository
from mcp.server import MCPServer

from devdocs_hub.api.schemas.documents import DocumentResponse


def register_document_resources(mcp: MCPServer):

    @mcp.resource("document://{document_id}")
    def get_document_by_id(document_id: int) -> Document | None:
        with document_repository_context() as context:
            return context.get(document_id)

