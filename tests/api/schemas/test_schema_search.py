
from hypothesis import strategies as st
from hypothesis import given
from pydantic import HttpUrl, ValidationError
from pydantic_core import to_json
from pytest import raises
from devdocs_hub.api.schemas.search import SearchRequest, SearchResult


class TestSearchSchema:
    def test_valid_search(self):
        SearchRequest(query="test", limit=1)

    def test_empty_query(self):
        with raises(ValidationError):
            SearchRequest(query="", limit=1)

    def test_query_bigger_than_allowed(self):
        with raises(ValidationError):
            SearchRequest(query=" " * 501, limit=1)

    def test_zero_limit(self):
        with raises(ValidationError):
            SearchRequest(query="test", limit=0)

    def test_limit_bigger_than_allowed(self):
        with raises(ValidationError):
            SearchRequest(query="test", limit=21)

    @given(st.text(min_size=1, max_size=500), st.integers(min_value=1, max_value=20))
    def test_valid_query_limit(self, query: str, limit:int):
        SearchRequest(query=query, limit=limit)

    def test_result_to_json(self):
        doc_id = 1
        chunk_id = 2
        score: float = 3.0
        content = "content"
        source = HttpUrl("http://example.com")

        res = SearchResult(document_id=doc_id, chunk_id=chunk_id, score=score, content=content, source=source)
        assert res.to_json() == '{"document_id":1,"chunk_id":2,"score":3.0,"content":"content","source":"http://example.com/"}'

