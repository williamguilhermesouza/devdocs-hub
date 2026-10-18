from dataclasses import dataclass

from sqlalchemy import select
from sqlalchemy.orm import Session

from devdocs_hub.application.embeddings import EmbeddingProvider
from devdocs_hub.db.core import Chunk


@dataclass
class SearchResult:
    score: float
    source: Chunk


class Retriever:
    def __init__(
        self,
        session: Session,
        embedding_provider: EmbeddingProvider,
    ):
        self._session = session
        self._embedding_provider = embedding_provider

    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        if limit < 1:
            raise ValueError("limit must be positive")

        embedding = self._embedding_provider.embed_text(query)
        distance = Chunk.embedding.cosine_distance(embedding)
        similarity = (1.0 - distance).label("score")

        stmt = (
            select(Chunk, similarity)
            .where(Chunk.embedding.is_not(None))
            .order_by(distance.asc())
            .limit(limit)
        )

        rows = self._session.execute(stmt).all()

        return [SearchResult(score=score, source=chunk) for chunk, score in rows]
