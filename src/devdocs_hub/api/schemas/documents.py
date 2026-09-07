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
    id: int | None
    title: str
    source: HttpUrl
    word_count: int

    @classmethod
    def from_doc(cls, doc: Document) -> "DocumentResponse":
        return cls(id=doc.id, title=doc.title, source=HttpUrl(doc.source), word_count=doc.word_count())


class DocumentListResponse(BaseModel):
    items: list[DocumentResponse]
    total: int

    @classmethod
    def from_docs(cls, docs: list[Document]) -> "DocumentListResponse":
        list_resp = cls(items=[], total=0)

        for doc in docs:
            list_resp.items.append(DocumentResponse.from_doc(doc))
            list_resp.total += 1

        return list_resp

