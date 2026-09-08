from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status

from devdocs_hub.api.dependencies import get_document_service
from devdocs_hub.api.schemas.documents import (
    DocumentCreate,
    DocumentListResponse,
    DocumentResponse,
)
from devdocs_hub.application.documents import DocumentService
from devdocs_hub.application.errors import DocumentNotFound

serviceDeps = Annotated[DocumentService, Depends(get_document_service)]

router = APIRouter(
    prefix="/documents",
)


@router.get(
    "/",
    responses={
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"description": "invalid request"}
    },
)
async def get_documents(
    service: serviceDeps,
    offset: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(gt=0, le=100)] = 20,
) -> DocumentListResponse:
    docs = service.list_documents(offset, limit)
    res = DocumentListResponse.from_docs(docs)
    return res


@router.get(
    "/{doc_id}",
    responses={
        status.HTTP_422_UNPROCESSABLE_CONTENT: {"description": "invalid request"}
    },
)
async def get_document(service: serviceDeps, doc_id: int) -> DocumentResponse:
    try:
        doc = service.get_document(doc_id)

    except DocumentNotFound:
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


@router.delete("/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_document(service: serviceDeps, doc_id: int) -> None:
    if not service.delete_document(doc_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Error deleting document"
        )
