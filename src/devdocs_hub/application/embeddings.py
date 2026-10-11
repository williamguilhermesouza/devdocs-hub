from typing import Protocol, Sequence

Vector = list[float]

class EmbeddingProvider(Protocol):
    def embed_text(self, text: str) -> Vector:
        ...
    
    def embed_texts(self, texts: Sequence[str]) -> list[Vector]:
        ...
