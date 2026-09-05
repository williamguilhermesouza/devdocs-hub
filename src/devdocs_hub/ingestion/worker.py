
import asyncio

from devdocs_hub.ingestion.fetcher import Fetcher


class IngestionWorker:
    def __init__(self, fetcher: Fetcher, maxsize: int = 0, r_maxsize: int = 0):
        self.fetcher = fetcher
        self.queue = asyncio.Queue[str](maxsize=maxsize)
        self.r_queue = asyncio.Queue[str](maxsize=r_maxsize)

    def start(self):
        self.process_task = asyncio.create_task(self.process())

    def submit(self, url: str) -> None:
        self.queue.put_nowait(url)

    async def process(self) -> None:
        while (True):
            next_urls = [await self.queue.get()]

            while (True):
                try:
                    next_urls.append(self.queue.get_nowait())
                except asyncio.QueueEmpty:
                    break

            responses = await self.fetcher.fetch_urls(next_urls)
            for res in responses.values():
                await self.r_queue.put(res)

    def stop(self):
        self.process_task.cancel()

