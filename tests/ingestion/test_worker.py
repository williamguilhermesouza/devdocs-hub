import asyncio

from pytest import raises

from devdocs_hub.ingestion.fetcher import Fetcher
from devdocs_hub.ingestion.worker import IngestionWorker
from tests.fakes.fake_client import FakeClient


class TestIngestionWorker:
    def test_process_urls(self):
        asyncio.run(self._test_process_urls())

    async def _test_process_urls(self):
        client = FakeClient()
        fetcher = Fetcher(client, max_parallel=10)
        worker = IngestionWorker(fetcher, maxsize=10, r_maxsize=10)
        worker.start()
        url_list = [f'{i}url' for i in range(10)]

        try:
            for u in url_list:
                worker.submit(u)

            results = [
                await asyncio.wait_for(worker.r_queue.get(), timeout=1)
                for _ in url_list
            ]

            assert set(results) == set(url_list)
        finally:
            worker.stop()
            with raises(asyncio.CancelledError):
                await worker.process_task
