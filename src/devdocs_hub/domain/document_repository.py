from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from devdocs_hub import db
from devdocs_hub.db.core import Chunk
from devdocs_hub.db.core import Document as DbDocument
from devdocs_hub.rag.chunker import Chunker

from .documents import Document


class DocumentRepository:
    def __init__(self, session: Session, chunker: Chunker):
        self._session = session
        self._chunker = chunker

    def add(self, item: Document) -> Document:
        chunks = self._chunker.chunk_document(item)
        stmt = select(DbDocument).where(DbDocument.title == item.title)

        with self._session as session, session.begin():

            db_document = session.scalar(stmt)
            if db_document is None:
                db_document = DbDocument(
                    title=item.title,
                    source=item.source,
                    content=item.content,
                )
                session.add(db_document)
            else:
                db_document.source = item.source
                db_document.content = item.content
                db_document.chunks.clear()
                
            session.flush()

            if not chunks:
                chunk = Chunk(
                    document_id=db_document.id,
                    position=0,
                    content=item.content,
                    embedding_id=None,
                )
                chunks.append(chunk)

            for chunk in chunks:
                chunk.document_id = db_document.id

            session.add_all(chunks)

            item.id = db_document.id

        return item

    def get(self, id: int) -> Document | None:
        stmt = select(DbDocument).where(DbDocument.id == id)

        with self._session as session:
            result = session.scalar(stmt)

            return (
                None
                if result == None
                else Document(
                    id=result.id,
                    title=result.title,
                    source=result.source,
                    content=result.content,
                )
            )

    def list(self, offset: int, limit: int) -> list[Document]:
        stmt = select(DbDocument).offset(offset).limit(limit)

        with self._session as session:
            result = session.scalars(stmt).all()

            return [
                Document(id=d.id, title=d.title, source=d.source, content=d.content)
                for d in result
            ]

        return []

    def delete(self, id: int) -> bool:
        get_stmt = select(DbDocument).where(DbDocument.id == id)

        with self._session as session:
            result = session.scalar(get_stmt)
            if not result:
                return False

            session.delete(result)
            session.commit()
            return True

    def get_next_id(self) -> int:
        return 0
