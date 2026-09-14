from sqlalchemy import Engine, insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from devdocs_hub.db.core import Chunk, Database
from devdocs_hub.db.core import Document as DbDocument

from .documents import Document


class DocumentRepository:
    def __init__(self, engine: Engine, db: Database):
        self._engine = engine
        self._db = db

    def add(self, item: Document) -> Document:
        stmt = (
            insert(DbDocument)
            .values(title=item.title, source=item.source, content=item.content)
            .returning(DbDocument)
        )

        with Session(self._engine) as session:
            result = session.scalar(stmt)
            if result is None:
                return item

            session.commit()
            item.id = result.id

        return item

    def get(self, id: int) -> Document | None:
        stmt = select(DbDocument).where(DbDocument.id == id)

        with Session(self._engine) as session:
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

        with Session(self._engine) as session:
            result = session.scalars(stmt).all()

            return [
                Document(id=d.id, title=d.title, source=d.source, content=d.content)
                for d in result
            ]

        return []

    def delete(self, id: int) -> bool:
        get_stmt = select(DbDocument).where(DbDocument.id == id)

        with Session(self._engine) as session:
            result = session.scalar(get_stmt)
            if not result:
                return False

            session.delete(result)
            session.commit()
            return True

    def create_document_with_first_chunk(self, item: Document) -> Document:
        doc_stmt = (
            insert(DbDocument)
            .values(title=item.title, source=item.source, content=item.content)
            .returning(DbDocument.id)
        )

        with Session(self._engine) as session:
            try:
                result = session.scalar(doc_stmt)

                if result is None:
                    raise SQLAlchemyError("failed creating document")

                item.id = result

                chunk_stmt = insert(Chunk).values(
                    document_id=item.id,
                    position=0,
                    content=item.content,
                    embedding_id=None,
                )

                session.add(chunk_stmt)
                session.commit()
            except SQLAlchemyError:
                session.rollback()

        return item

    def get_next_id(self) -> int:
        return 0
