from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from devdocs_hub.db.core import Chunk, Database
from devdocs_hub.db.core import Document as DbDocument

from .documents import Document


class DocumentRepository:
    def __init__(self, engine: Engine, db: Database):
        self._engine = engine
        self._db = db

    def add(self, item: Document) -> Document:
        return self.create_document_with_first_chunk(item)

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
        with Session(self._engine) as session, session.begin():
                db_document = DbDocument(title=item.title, source=item.source, content=item.content)
                session.add(db_document)
                session.flush()


                chunk = Chunk(
                    document_id=db_document.id,
                    position=0,
                    content=item.content,
                    embedding_id=None,
                )
                session.add(chunk)

                item.id = db_document.id

        return item

    def get_next_id(self) -> int:
        return 0
