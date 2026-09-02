from devdocs_hub.application.errors import DocumentNotFound
from devdocs_hub.application.protocols import RepositoryProtocol
from devdocs_hub.domain.documents import Document


class DocumentService:
    def __init__(self, repository: RepositoryProtocol[Document]):
        self._repository = repository

    def create_document(self, title: str, source: str, content: str) -> Document:
        doc_id = self._repository.get_next_id()
        document = Document(id=doc_id, title=title, source=source, content=content)
        added = self._repository.add(document)

        if added is None:
            raise DocumentNotFound

        return added

    def get_document(self, id: int) -> Document | None:
        doc = self._repository.get(id)

        if doc is None:
            raise DocumentNotFound

        return doc

    def list_documents(self) -> list[Document]:
        return self._repository.list()

    def delete_document(self, id: int) -> bool:
        return self._repository.delete(id)
