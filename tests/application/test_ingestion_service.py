import asyncio

from sqlalchemy import NotNullable
from pytest import raises

from devdocs_hub.application.documents import DocumentService
from devdocs_hub.application.ingestion import DocumentIngestionService
from devdocs_hub.domain.repository import InMemoryRepository
from devdocs_hub.domain.documents import Document
from devdocs_hub.ingestion.errors import FetchError
from devdocs_hub.ingestion.fetcher import Fetcher
from tests.fakes.fake_client import FakeClient

example_response = r'<!doctype html><html lang=en><head><meta charset=utf-8><link rel=icon href=data:,><meta name=viewport content="width=device-width,initial-scale=1"><title>Example Domain</title><style>html{color-scheme:light dark;background:light-dark(#eee,#222)}body{font:16px/1.6 system-ui,sans-serif;max-width:26em;margin:auto;padding:25vh 2em 2em;text-align:center}</style></head><body><p>This domain is for use in documentation examples without needing permission. This is not a service; avoid relying on it for testing and monitoring purposes.</p><script src=/s.js></script></body></html>'
example_title = 'Example Domain'

class TestIngestionService:
    def test_valid(self):
        asyncio.run(self._test_valid())

    async def _test_valid(self):
        repo = InMemoryRepository[Document]()
        client = FakeClient(response=example_response)
        fetcher = Fetcher(client, max_parallel=3)
        docSv = DocumentService(repo)

        sut = DocumentIngestionService(fetcher, docSv)
        url = 'http://example.org'
        created_doc = await sut.ingest_url(url)

        assert created_doc is not None 
        assert created_doc.title == example_title
        assert created_doc.content == example_response
        assert created_doc.source == url

    def test_fetcherror(self):
        asyncio.run(self._test_fetcherror())

    async def _test_fetcherror(self):
        repo = InMemoryRepository[Document]()
        client = FakeClient(response=example_response, raises=True)
        fetcher = Fetcher(client, max_parallel=3)
        docSv = DocumentService(repo)

        sut = DocumentIngestionService(fetcher, docSv)
        url = 'http://example.org'

        with raises(FetchError):
            created_doc = await sut.ingest_url(url)
