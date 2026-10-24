from devdocs_hub.api.schemas.answer import AnswerResponse
from devdocs_hub.api.schemas.documents import DocumentCreate, DocumentListResponse, DocumentResponse
from devdocs_hub.application.errors import DocumentNotFound
from devdocs_hub.mcp.dependencies import answer_service_context, document_service_context

from mcp.server import MCPServer


def register_document_tools(mcp: MCPServer):
    @mcp.tool()
    async def get_documents(
        offset: int = 0,
        limit: int = 20,
    ) -> DocumentListResponse:
        with document_service_context() as service:
            docs = service.list_documents(offset, limit)
            return DocumentListResponse.from_docs(docs)

    @mcp.tool()
    async def get_document(doc_id: int) -> DocumentResponse:
        with document_service_context() as service:
            try:
                doc = service.get_document(doc_id)

            except DocumentNotFound as exc:
                raise ValueError("Requested document not found") from exc

            return DocumentResponse.from_doc(doc)

    @mcp.tool()
    async def create_document(
            doc: DocumentCreate
    ) -> DocumentResponse:
        with document_service_context() as service:
            res = service.create_document(doc.title, str(doc.source), doc.content)
            return DocumentResponse.from_doc(res)

    @mcp.tool()
    async def delete_document(doc_id: int) -> None:
        with document_service_context() as service:
            if not service.delete_document(doc_id):
                raise ValueError("Requested document could not be deleted")

    @mcp.tool()
    async def ask(question: str) -> AnswerResponse:
        with answer_service_context() as service:
            response = service.ask(question)
            return AnswerResponse(answer=response.answer, chunks=response.chunks)
