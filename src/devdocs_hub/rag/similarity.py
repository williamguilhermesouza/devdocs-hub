from math import sqrt, pow

from devdocs_hub.application.embeddings import Vector
from devdocs_hub.rag.errors import VectorWithDifferentDimensionException


def cosine_similarity(a: Vector, b: Vector) -> float:
    if len(a) != len(b):
        raise VectorWithDifferentDimensionException("Vectors must have same dimensions")
        
    dot_prod = sum([m * n for m, n in zip(a, b)])
    magnitude_a = sqrt(sum([pow(val, 2) for val in a]))
    magnitude_b = sqrt(sum([pow(val, 2) for val in b]))
    magnitude = magnitude_a * magnitude_b

    return 0 if magnitude == 0 else dot_prod / magnitude
