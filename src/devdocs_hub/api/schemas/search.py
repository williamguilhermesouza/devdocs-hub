from collections.abc import Sequence

from pydantic import BaseModel, Field, HttpUrl


class SearchResult(BaseModel):
    document_id: int
    chunk_id: int
    score: float
    content: str
    source: HttpUrl

class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    limit: int = Field(gt=0, lt=21)

class SearchResponse(BaseModel):
    query: str
    results: Sequence[SearchResult]
