import asyncio
import re
from devdocs_hub.api.routers.documents import create_document
from devdocs_hub.application.documents import DocumentService
from devdocs_hub.domain.documents import Document
from devdocs_hub.ingestion.fetcher import Fetcher
from devdocs_hub.rag.chunker import Chunker


class DocumentIngestionService:
    def __init__(self, fetcher: Fetcher, docsSv: DocumentService):
        self._fetcher = fetcher
        self._doc = docsSv
        self._re = re.compile(r'<title\b[^>]*>(.*?)</title>')

    async def ingest_url(self, url: str) -> Document:
        content = await self._fetcher.fetch_url(url)
        title = self.get_title(content)
        created_doc = self._doc.create_document(title=title, content=content, source=url)
        return created_doc

    async def ingest_urls(self, urls: list[str]) -> dict[str, Document | None]:
        docs: dict[str, Document | None] = { k: None for k in urls }

        content_by_url = await self._fetcher.fetch_urls(urls)
        for url, content in content_by_url.items():
            title = self.get_title(content)
            created_doc = self._doc.create_document(title=title, content=content, source=url)
            docs[url] = created_doc

        return docs




    def get_title(self, content: str) -> str:
        matched = self._re.search(content, re.IGNORECASE | re.DOTALL)
        return matched.group(1) if matched else ''




