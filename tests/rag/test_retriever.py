from devdocs_hub.application.embeddings import Vector
import pytest
from typing import Sequence
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from devdocs_hub.db.core import Base, Chunk
from devdocs_hub.rag.retriever import Retriever
from tests.fakes.embeddings import FakeEmbeddingsProvider


class StubEmbeddingProvider:
    def embed_text(self, text: str) -> Vector:
        assert text == "query"
        return [1.0, 0.0]

    def embed_many(self, texts: Sequence[str]) -> list[Vector]:
        return [self.embed_text(text) for text in texts]


class TestRetriever:
    @pytest.fixture
    def setup_retriever(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        Base.metadata.create_all(engine)

        session = Session(engine)

        chunks = [
            Chunk(position=0, content="Low relevance", embedding_id="low"),
            Chunk(position=1, content="Medium relevance", embedding_id="medium"),
            Chunk(position=2, content="High relevance", embedding_id="high"),
        ]

        session.add_all(chunks)
        session.commit()

        embeddings = {"low": [-1.0, 0.0], "medium": [0.0, 1.0], "high": [1.0, 0.0]}

        stub = StubEmbeddingProvider()
        retriever = Retriever(session, stub, embeddings)

        yield retriever

        session.close()
        engine.dispose()

    def test_search_returns_chunks_with_similarity_scores(
        self, setup_retriever
    ):
        results = setup_retriever.search("query")

        assert len(results) == 3
        assert {result.source.content for result in results} == {
            "Low relevance",
            "Medium relevance",
            "High relevance",
        }

        scores = {
            result.source.content: result.score
            for result in results
        }
        assert scores["High relevance"] == pytest.approx(1.0)
        assert scores["Medium relevance"] == pytest.approx(0.0)
        assert scores["Low relevance"] == pytest.approx(-1.0)

    def test_search_returns_results_in_relevance_order(
        self, setup_retriever
    ):
        results = setup_retriever.search("query")

        assert [r.source.content for r in results] == [
            "High relevance",
            "Medium relevance",
            "Low relevance",
        ]

    def test_search_respects_limit(self, setup_retriever):
        results = setup_retriever.search("query", limit=2)

        assert len(results) == 2
        assert [r.source.content for r in results] == [
            "High relevance",
            "Medium relevance",
        ]

    def test_search_rejects_non_positive_limit(self, setup_retriever):
        with pytest.raises(ValueError, match="limit must be positive"):
            setup_retriever.search("query", limit=0)

        with pytest.raises(ValueError, match="limit must be positive"):
            setup_retriever.search("query", limit=-1)
