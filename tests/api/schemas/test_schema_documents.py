from sys import maxsize as MAX_SIZE_INDEX_INT

from hypothesis import given
from hypothesis import strategies as st
from pydantic import HttpUrl, ValidationError
from pytest import raises

from devdocs_hub.api.schemas.documents import DocumentCreate
from devdocs_hub.domain.documents import Document


class TestDocumentsSchema:
    def test_document_create(self):
        url = HttpUrl("http://example.com")
        url_https = HttpUrl("https://example.com")
        DocumentCreate(title="valid", source=url, content="example")
        DocumentCreate(title="valid", source=url_https, content="example")

    @given(st.text(min_size=1, max_size=200))
    def test_valid_title(self, title: str):
        url = HttpUrl("http://example.com")
        DocumentCreate(title=title, source=url, content="example")

    def test_empty_title(self):
        url = HttpUrl("http://example.com")

        with raises(ValidationError):
            DocumentCreate(title="", source=url, content="example")

    def test_empty_content(self):
        url = HttpUrl("http://example.com")

        with raises(ValidationError):
            DocumentCreate(title="title", source=url, content="")

    @given(st.integers(min_value=201, max_value=MAX_SIZE_INDEX_INT))
    def test_title_too_long(self, size: int):
        url = HttpUrl("http://example.com")
        title = "" * size

        with raises(ValidationError):
            DocumentCreate(title=title, source=url, content="")

    @given(st.text(min_size=1, max_size=200), st.text(min_size=1))
    def test_from_create_to_document(self, title: str, content: str):
        url = HttpUrl("http://example.com")
        create_doc = DocumentCreate(title=title, source=url, content=content)

        doc: Document = create_doc.to_document()

        assert doc.title == title
        assert doc.source == str(url)
        assert doc.content == content
