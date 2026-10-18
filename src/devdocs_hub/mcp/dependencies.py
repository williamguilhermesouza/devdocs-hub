from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from devdocs_hub.application.documents import DocumentService
from devdocs_hub.domain.document_repository import DocumentRepository
from devdocs_hub.rag.chunker import Chunker
from devdocs_hub.rag.embeddings import get_embedding_provider
from devdocs_hub.settings import settings


engine = create_engine(settings.db_url, echo=True)

def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

chunker = Chunker()

def get_document_service(session: Session) -> DocumentService:
    repository = DocumentRepository(session, chunker, get_embedding_provider())
    return DocumentService(repository)


@contextmanager
def document_service_context() -> Iterator[DocumentService]:
    with Session(engine) as session:
        yield get_document_service(session)
