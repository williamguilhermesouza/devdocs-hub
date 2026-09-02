import asyncio

from pytest import raises

from devdocs_hub.ingestion.errors import FetchError
from devdocs_hub.ingestion.fetcher import Fetcher
from tests.fakes.fake_client import FakeClient


class TestFetcher:
    def test_successful_response(self):
        client = FakeClient()
        fetcher = Fetcher(client, max_parallel=3)
        url = "http://example.org"
        fetched: str = asyncio.run(fetcher.fetch_url(url))
        assert fetched == url

    def test_404_response(self):
        client = FakeClient(raises=True)
        fetcher = Fetcher(client, max_parallel=3)
        url = "http://example.org"

        with raises(FetchError):
            asyncio.run(fetcher.fetch_url(url))

    def test_timeout(self):
        client = FakeClient(raises=True)
        fetcher = Fetcher(client, max_parallel=3)
        url = "http://example.org"

        with raises(FetchError):
            asyncio.run(fetcher.fetch_url(url))

    def test_3urlfetchedconcurrently(self):
        client = FakeClient()
        fetcher = Fetcher(client, max_parallel=3)
        url = "http://example.org"
        urls = [f"0{url}", f"1{url}", f"2{url}"]
        fetched: dict[str, str] = asyncio.run(fetcher.fetch_urls(urls))
        for i, text in enumerate(fetched.values()):
            assert text == f"{i}{url}"
