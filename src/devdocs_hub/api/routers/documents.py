from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from devdocs_hub.application.documents import DocumentService
from devdocs_hub.application.errors import DocumentNotFound
from devdocs_hub.domain.documents import Document
from devdocs_hub.domain.repository import InMemoryRepository
from devdocs_hub.api.schemas.documents import (
    DocumentCreate,
    DocumentResponse,
    DocumentListResponse,
)

repository = InMemoryRepository[Document]()


def get_document_service() -> DocumentService:
    return DocumentService(repository)


serviceDeps = Annotated[DocumentService, Depends(get_document_service)]

router = APIRouter(
    prefix="/documents",
)


@router.get("/")
async def get_documents(service: serviceDeps) -> DocumentListResponse:
    docs = service.list_documents()
    res = DocumentListResponse.from_docs(docs)
    return res


@router.get("/{doc_id}", responses={422: {"description": "invalid request"}})
async def get_document(service: serviceDeps, doc_id: int) -> DocumentResponse:
    try:
        doc = service.get_document(doc_id)

    except DocumentNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Requested document not found"
        )

    return DocumentResponse.from_doc(doc)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_document(
    service: serviceDeps, doc: DocumentCreate
) -> DocumentResponse:
    res = service.create_document(doc.title, str(doc.source), doc.content)
    return DocumentResponse.from_doc(res)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(service: serviceDeps, doc_id: int) -> None:
    if not service.delete_document(doc_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Error deleting document"
        )
