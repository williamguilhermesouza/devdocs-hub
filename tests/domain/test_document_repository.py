from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from devdocs_hub.db.core import Base, Chunk
from devdocs_hub.domain.document_repository import DocumentRepository
from devdocs_hub.domain.documents import Document
from devdocs_hub.rag.chunker import Chunker


class TestDocumentRepository:
    def test_create_10_document(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            chunker = Chunker()
            repo = DocumentRepository(session, chunker)

            for i in range(10):
                doc = Document(id=None,title=f"title{i}",source=f"source{i}",content=f"content{i}")
                created = repo.add(doc)
                assert created is not None
                assert created.id is not None

            docs = repo.list(0,10)
            assert docs != None
            assert len(docs) == 10

    def test_create_chunked_doc(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        Base.metadata.create_all(engine)
        chunker = Chunker(max_words=1, overlap_words=0)

        with Session(engine) as session:
            repo = DocumentRepository(session, chunker)

            doc_content = 'this should persist 5 chunks'
            splitted_content = doc_content.split()
            doc = Document(id=None,title="title",source="source",content=doc_content)
            created = repo.add(doc)
            assert created is not None
            assert created.id is not None

            stmt = select(Chunk).where(Chunk.document_id == created.id)
            chunks = session.scalars(stmt).all()

            assert len(chunks) == 5

            for i, chunk in enumerate(chunks):
                assert i == chunk.position
                assert splitted_content[i] == chunk.content

    def test_create_chunked_doc_dontduplicatechunks(self):
        engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
        Base.metadata.create_all(engine)
        chunker = Chunker(max_words=1, overlap_words=0)

        with Session(engine) as session:
            repo = DocumentRepository(session, chunker)

            doc_content = 'this should persist 5 chunks'
            doc = Document(id=None,title="title",source="source",content=doc_content)
            created = repo.add(doc)
            assert created is not None
            assert created.id is not None

            doc_content2 = 'update to 3'
            doc = Document(id=None,title="title",source="source",content=doc_content2)
            created2 = repo.add(doc)
            assert created2 is not None
            assert created2.id is not None
            assert created2.id == created.id

            stmt = select(Chunk).where(Chunk.document_id == created.id)
            chunks = session.scalars(stmt).all()

            assert len(chunks) == 3 # old chunks are not here

