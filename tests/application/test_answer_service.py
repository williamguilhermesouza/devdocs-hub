from devdocs_hub.application.answer import AnswerService, Context
from devdocs_hub.db.core import Chunk
from devdocs_hub.rag.retriever import SearchResult


class FakeLLM:
    def ask(self, content: Context, question: str) -> str:
        return "llm"

fake_chunk = Chunk(id=0, document_id=0, position=0, content='test')

class FakeRetriever:
    def search(self, query: str, limit: int = 5) -> list[SearchResult]:
        return [SearchResult(score=1.0, source=fake_chunk)]


class TestAnswerService:
    def test_answer_service(self):
        sut = AnswerService(FakeRetriever(), FakeLLM())
        response = sut.ask("why the sky is blue?")
        assert response is not None
        assert response.answer == 'llm'
        assert response.chunks == [fake_chunk]


