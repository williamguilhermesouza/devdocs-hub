
from collections.abc import Sequence

from devdocs_hub.application.embeddings import Vector


class FakeEmbeddingsProvider:
    def embed_text(self, text: str) -> Vector:
        return [float(ord(c)) for c in text]

    def embed_many(self, texts: Sequence[str]) -> list[Vector]:
        return [self.embed_text(t) for t in texts]
