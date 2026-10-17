from collections.abc import Sequence
from typing import Protocol

Vector = list[float]

class EmbeddingProvider(Protocol):
    def embed_text(self, text: str) -> Vector:
        ...
    
    def embed_many(self, texts: Sequence[str]) -> list[Vector]:
        ...
