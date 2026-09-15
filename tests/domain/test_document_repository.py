from sqlalchemy import create_engine

from devdocs_hub.db.core import Database
from devdocs_hub.domain.document_repository import DocumentRepository
from devdocs_hub.domain.documents import Document


class TestDocumentRepository:
    def test_create_10_document(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        db = Database(engine)
        db.init()
        repo = DocumentRepository(engine, db)

        for i in range(10):
            doc = Document(id=None,title=f"title{i}",source=f"source{i}",content=f"content{i}")
            created = repo.add(doc)
            assert created is not None
            assert created.id is not None

        docs = repo.list(0,10)
        assert docs != None
        assert len(docs) == 10

