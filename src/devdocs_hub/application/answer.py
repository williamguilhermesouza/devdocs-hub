from dataclasses import dataclass
from typing import Protocol

from devdocs_hub.db.core import Chunk
from devdocs_hub.rag.retriever import SearchResult


@dataclass
class AnswerResponse:
    answer: str
    chunks: list[Chunk]


@dataclass
class Context:
    metadata: dict[str, list[SearchResult]]


class LLMProvider(Protocol):
    def ask(self, content: Context, question: str) -> str: ...


class RetrieverProvider(Protocol):
    def search(self, query: str, limit: int = 5) -> list[SearchResult]: ...


class AnswerService:
    def __init__(self, retriever: RetrieverProvider, llmprovider: LLMProvider):
        self._retriever = retriever
        self._llmprovider = llmprovider

    def ask(self, question: str) -> AnswerResponse:
        search_results = self._retriever.search(question)
        context = Context(metadata={"embeddings": search_results})
        response = self._llmprovider.ask(context, question)

        return AnswerResponse(answer=response, chunks=[x.source for x in search_results])
