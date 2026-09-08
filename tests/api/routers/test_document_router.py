from fastapi import status
from fastapi.testclient import TestClient
from pydantic import HttpUrl
from pytest import fixture

from devdocs_hub.api.dependencies import get_document_service
from devdocs_hub.api.main import app
from devdocs_hub.api.schemas.documents import DocumentCreate
from devdocs_hub.application.documents import DocumentService
from devdocs_hub.domain.documents import Document
from devdocs_hub.domain.repository import InMemoryRepository


def create_test_service() -> DocumentService:
    repository = InMemoryRepository[Document]()

    repository.add(
        Document(
            id=0,
            title="Python",
            source="https://example.com/python",
            content="Python documentation",
        )
    )

    repository.add(
        Document(
            id=1,
            title="FastAPI",
            source="https://example.com/fastapi",
            content="FastAPI documentation",
        )
    )

    return DocumentService(repository)


@fixture
def document_service() -> DocumentService:
    return create_test_service()


@fixture
def client(document_service: DocumentService):
    app.dependency_overrides[get_document_service] = lambda: document_service

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


class TestDocumentRouter:
    def test_get_documents(self, client: TestClient):
        res = client.get("/documents")
        assert res.status_code == status.HTTP_200_OK
        assert len(res.json()) == 2

    def test_create_document(self, client: TestClient):
        doc_create = DocumentCreate(
            title="title", source=HttpUrl("http://example.com"), content="content"
        )

        res = client.post("/documents", json=doc_create.model_dump(mode="json"))

        assert res.status_code == status.HTTP_201_CREATED
        assert res.json() == {
            "id": 2,
            "title": "title",
            "source": "http://example.com/",
            "word_count": 1,
        }

    def test_create_invalid_doc(self, client: TestClient):
        res = client.post("/documents", json="")
        assert res.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_delete_document(self, client: TestClient):
        res = client.delete("/documents/1")
        assert res.status_code == status.HTTP_204_NO_CONTENT

        res_get = client.get("/documents/1")
        assert res_get.status_code == status.HTTP_404_NOT_FOUND

    def test_get_document(self, client: TestClient):
        res = client.get("/documents/0")

        assert res.status_code == status.HTTP_200_OK
        assert res.json() == {
            "id": 0,
            "title": "Python",
            "source": "https://example.com/python",
            "word_count": 2,
        }

    def test_get_document_not_found(self, client: TestClient):
        res = client.get("/documents/999")
        assert res.status_code == status.HTTP_404_NOT_FOUND
