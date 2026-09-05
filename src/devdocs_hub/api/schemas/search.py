from pydantic import BaseModel, Field, HttpUrl


class SearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=500)
    limit: int = Field(gt=1, lt=20)

class SearchResult(BaseModel):
    document_id: int
    chunk_id: int
    score: float
    content: str
    source: HttpUrl

class SearchResponse(BaseModel):
    query: str
    results: list[SearchResult]
