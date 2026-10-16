from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from devdocs_hub.application.embeddings import EmbeddingProvider, Vector
from devdocs_hub.db.core import Chunk
from devdocs_hub.rag.similarity import cosine_similarity


@dataclass
class SearchResult:
    score: float
    source: Chunk


class Retriever:
    def __init__(
        self,
        session: Session,
        embedding_provider: EmbeddingProvider,
        embeddings: dict[str, Vector],
    ):
        self._session = session
        self._embedding_provider = embedding_provider
        self._embeddings = embeddings

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        if limit < 1:
            raise ValueError("limit must be positive")

        embedding = self._embedding_provider.embed_text(query)
        comparisons: dict[str, float] = {
            a: cosine_similarity(b, embedding) for a, b in self._embeddings.items()
        }

        ranked_ids = [
            embedding_id
            for embedding_id, score in sorted(
                comparisons.items(),
                key=lambda item: item[1],
                reverse=True,
            )[:limit]
        ]

        stmt = select(Chunk).where(Chunk.embedding_id.in_(ranked_ids))
        chunks = self._session.scalars(stmt).all()

        chunks_by_embedding_id = {
            chunk.embedding_id: chunk for chunk in chunks
        }

        return [
            SearchResult(
                score=comparisons[embedding_id],
                source=chunks_by_embedding_id[embedding_id],
            )
            for embedding_id in ranked_ids
            if embedding_id in chunks_by_embedding_id
        ]
