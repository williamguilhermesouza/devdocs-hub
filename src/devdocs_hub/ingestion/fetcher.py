import asyncio
from httpx import AsyncClient

from devdocs_hub.application.protocols import HttpClientProtocol
from devdocs_hub.ingestion.errors import FetchError


class Fetcher:
    def __init__(self, client: HttpClientProtocol, max_parallel: int):
        if max_parallel <= 0:
            raise ValueError("max parallel must be greater than 0")

        self.max_parallel = max_parallel
        self.client = client

    async def fetch_url(self, url: str) -> str:
        try:
            response = await self.client.get(url)
            response.raise_for_status()
        except Exception as e:
            raise FetchError(e)

        return response.text
        
    async def fetch_urls(self, urls: list[str]) -> dict[str, str]:
        processed = 0
        results: list[str] = []
        while processed < len(urls):
            next_urls = urls[processed:processed + self.max_parallel]
            tasks = [asyncio.create_task(self.fetch_url(url)) for url in next_urls]
            results.extend(await asyncio.gather(*tasks))
            processed += len(next_urls)

        results_dict = dict(zip(urls, results))
        return results_dict
