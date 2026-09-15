from pytest import raises
from sqlalchemy import create_engine

from devdocs_hub.application.documents import DocumentService
from devdocs_hub.application.errors import DocumentNotFound
from devdocs_hub.db.core import Database
from devdocs_hub.domain.document_repository import DocumentRepository
from devdocs_hub.domain.documents import Document
from devdocs_hub.domain.repository import InMemoryRepository


class TestDocumentService:
    def test_create_get_document(self):
        repo = InMemoryRepository[Document]()
        service = DocumentService(repo)
        created = service.create_document("title", "source", "content")
        assert created is not None
        assert created.id is not None

        doc = service.get_document(created.id)
        assert doc != None
        assert doc.id == created.id

    def test_delete_document(self):
        repo = InMemoryRepository[Document]()
        service = DocumentService(repo)
        created = service.create_document("title", "source", "content")
        assert created is not None
        assert created.id is not None

        deleted = service.delete_document(created.id)
        assert deleted

        with raises(DocumentNotFound):
            service.get_document(created.id)

    def test_list_documents(self):
        repo = InMemoryRepository[Document]()
        service = DocumentService(repo)
        service.create_document("title0", "source", "content")
        service.create_document("title1", "source", "content")
        service.create_document("title2", "source", "content")

        docs = service.list_documents()
        assert docs != None
        assert len(docs) == 3 

        for i, doc in enumerate(docs):
            assert doc.title == f'title{i}'

    def test_create_get_document_sqlite(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        db = Database(engine)
        db.init()
        repo = DocumentRepository(engine, db)
        service = DocumentService(repo)
        created = service.create_document("title", "source", "content")
        assert created is not None
        assert created.id is not None

        doc = service.get_document(created.id)
        assert doc != None
        assert doc.id == created.id

    def test_delete_document_sqlite(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        db = Database(engine)
        db.init()
        repo = DocumentRepository(engine, db)
        service = DocumentService(repo)
        created = service.create_document("title", "source", "content")
        assert created is not None
        assert created.id is not None

        deleted = service.delete_document(created.id)
        assert deleted

        with raises(DocumentNotFound):
            service.get_document(created.id)

    def test_list_documents_sqlite(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        db = Database(engine)
        db.init()
        repo = DocumentRepository(engine, db)
        service = DocumentService(repo)
        service.create_document("title0", "source", "content")
        service.create_document("title1", "source", "content")
        service.create_document("title2", "source", "content")

        docs = service.list_documents()
        assert docs != None
        assert len(docs) == 3 

        for i, doc in enumerate(docs):
            assert doc.title == f'title{i}'
