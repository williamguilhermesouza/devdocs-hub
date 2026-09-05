from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl

from devdocs_hub.domain.documents import Document


class DocumentCreate(BaseModel):
    title: Annotated[str, Field(min_length=1, max_length=200)]
    source: HttpUrl
    content: str = Field(min_length=1)

    def to_document(self) -> Document:
        return Document(id=None, title=self.title, source=str(self.source), content=self.content)

class DocumentResponse(BaseModel):
    id: int
    title: str
    source: HttpUrl
    word_count: int


class DocumentListResponse(BaseModel):
    items: list[DocumentResponse]
    total: int
