from collections.abc import Iterator
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from devdocs_hub.application.answer import AnswerService
from devdocs_hub.application.documents import DocumentService
from devdocs_hub.domain.document_repository import DocumentRepository
from devdocs_hub.providers.OpenAIProvider import OpenAIProvider
from devdocs_hub.rag.chunker import Chunker
from devdocs_hub.rag.embeddings import get_embedding_provider
from devdocs_hub.rag.retriever import Retriever
from devdocs_hub.settings import settings


engine = create_engine(settings.db_url, echo=True)

def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session

chunker = Chunker()

def get_document_repository(session: Session) -> DocumentRepository:
    return DocumentRepository(session, chunker, get_embedding_provider())


def get_document_service(session: Session) -> DocumentService:
    repository = DocumentRepository(session, chunker, get_embedding_provider())
    return DocumentService(repository)

def get_answer_service(session: Session) -> AnswerService:
    retriever = Retriever(session, get_embedding_provider())
    llm = OpenAIProvider(endpoint=settings.llm_endpoint, model=settings.llm_model_name, key=settings.llm_api_key)
    service = AnswerService(retriever, llm)
    return service

@contextmanager
def document_repository_context() -> Iterator[DocumentRepository]:
    with Session(engine) as session:
        yield get_document_repository(session)

@contextmanager
def document_service_context() -> Iterator[DocumentService]:
    with Session(engine) as session:
        yield get_document_service(session)

@contextmanager
def answer_service_context() -> Iterator[AnswerService]:
    with Session(engine) as session:
        yield get_answer_service(session)
