from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from devdocs_hub.application.answer import AnswerService, LLMProvider
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

sessionDeps = Annotated[Session, Depends(get_session)]
chunker = Chunker()

def get_document_service(session: sessionDeps) -> DocumentService:
    repository = DocumentRepository(session, chunker, get_embedding_provider())
    return DocumentService(repository)

def get_retriever(session: sessionDeps) -> Retriever:
    retriever = Retriever(session, get_embedding_provider())
    return retriever


retrieverDeps = Annotated[Retriever, Depends(get_retriever)]


def get_llm_provider() -> LLMProvider:
    return OpenAIProvider(
        endpoint=settings.llm_endpoint,
        model=settings.llm_model_name,
        key=settings.llm_api_key,
    )


def get_answer_service(
    retriever: retrieverDeps,
    llm_provider: Annotated[LLMProvider, Depends(get_llm_provider)],
) -> AnswerService:
    return AnswerService(retriever, llm_provider)

serviceDeps = Annotated[DocumentService, Depends(get_document_service)]
answerDeps = Annotated[AnswerService, Depends(get_answer_service)]
