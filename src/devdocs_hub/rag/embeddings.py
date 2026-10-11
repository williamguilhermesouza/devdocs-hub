from sentence_transformers import SentenceTransformer
from devdocs_hub.application.embeddings import EmbeddingProvider, Vector


class EmbeddingException(Exception):
    pass


class SentenceTransformerProvider:
    def __init__(self, model_name: str):
        self._model = SentenceTransformer(model_name)

    def embed_text(self, text: str) -> Vector:
        return self.embed_many([text])[0]

    def embed_many(self, texts: list[str]) -> list[Vector]:
        if not texts:
            return []

        try:
            embeddings = self._model.encode(
                texts, normalize_embeddings=True, convert_to_numpy=True
            )
            return [vector.tolist() for vector in embeddings]
        except Exception as e:
            raise EmbeddingException("Failed to generate text embeddings") from e
