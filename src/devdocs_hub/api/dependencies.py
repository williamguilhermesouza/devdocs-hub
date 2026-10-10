from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from devdocs_hub.application.documents import DocumentService
from devdocs_hub.domain.document_repository import DocumentRepository
from devdocs_hub.settings import settings
from devdocs_hub.rag.chunker import Chunker

engine = create_engine(settings.db_url, echo=True)

def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

sessionDeps = Annotated[Session, Depends(get_session)]
chunker = Chunker()

def get_document_service(session: sessionDeps) -> DocumentService:
    repository = DocumentRepository(session, chunker)
    return DocumentService(repository)

serviceDeps = Annotated[DocumentService, Depends(get_document_service)]
