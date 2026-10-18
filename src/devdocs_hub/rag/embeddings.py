from collections.abc import Sequence
from functools import lru_cache

from devdocs_hub.application.embeddings import Vector


class EmbeddingException(Exception):
    pass


class SentenceTransformerProvider:
    def __init__(self, model_name: str):
        from sentence_transformers import SentenceTransformer

        self._model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> Vector:
        return self.embed_many([text])[0]

    def embed_many(self, texts: Sequence[str]) -> list[Vector]:
        if not texts:
            return []

        try:
            embeddings = self._model.encode(
                texts, normalize_embeddings=True, convert_to_numpy=True
            )
            return [vector.tolist() for vector in embeddings]
        except Exception as e:
            raise EmbeddingException("Failed to generate text embeddings") from e


@lru_cache(maxsize=1)
def get_embedding_provider() -> SentenceTransformerProvider:
    """Return the process-wide embedding provider, loading its model once."""
    from devdocs_hub.settings import settings

    return SentenceTransformerProvider(model_name=settings.embedding_model_name)
