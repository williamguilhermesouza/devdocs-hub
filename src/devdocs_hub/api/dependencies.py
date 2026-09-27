from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from typing import Annotated
from fastapi import Depends
from collections.abc import Iterator

from devdocs_hub.application.documents import DocumentService
from devdocs_hub.db.core import Database
from devdocs_hub.domain.document_repository import DocumentRepository
from devdocs_hub.settings import settings

engine = create_engine(settings.db_url, echo=True)
db = Database(engine) #TODO remove here and in tests

def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

sessionDeps = Annotated[Session, Depends(get_session)]

def get_document_service(session: sessionDeps) -> DocumentService:
    repository = DocumentRepository(session)
    return DocumentService(repository)

serviceDeps = Annotated[DocumentService, Depends(get_document_service)]
