from devdocs_hub.application.documents import DocumentService
from devdocs_hub.domain.documents import Document
from devdocs_hub.domain.repository import InMemoryRepository

repository = InMemoryRepository[Document]()


def get_document_service() -> DocumentService:
    return DocumentService(repository)
