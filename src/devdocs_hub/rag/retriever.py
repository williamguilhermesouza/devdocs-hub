
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
    def __init__(self, session: Session, embedding_provider: EmbeddingProvider, embeddings: dict[str, Vector]):
        self._session = session
        self._embedding_provider = embedding_provider
        self._embeddings = embeddings

    def search(self, query: str, limit:int = 5) -> list[SearchResult]:
        if limit < 1:
            raise ValueError("limit must be positive")

        embedding = self._embedding_provider.embed_text(query)
        comparisons: dict[str, float] = { a: cosine_similarity(b, embedding) for a, b in self._embeddings.items() }
        s = sorted(comparisons.items(), key=lambda item: item[1], reverse=True)

        s = s[:limit]
        embed_ids = [x[0] for x in s]
        results: list[SearchResult] = []

        stmt = select(Chunk).where(Chunk.embedding_id.in_(embed_ids))
        with self._session as session:
            chunks = session.scalars(stmt).all()

            for chunk in chunks:
                results.append(SearchResult(score=comparisons[chunk.embedding_id], source=chunk))

        return results








        
