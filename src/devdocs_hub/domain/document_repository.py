from sqlalchemy import Engine, delete, insert, select

from devdocs_hub.db.core import Database

from .documents import Document


class DocumentRepository:
    def __init__(self, engine: Engine, db: Database):
        self._engine = engine
        self._db = db

    def add(self, item: Document) -> Document:
        stmt = (
            insert(self._db.documents)
            .values(title=item.title, source=item.source, content=item.content)
            .returning(self._db.documents.c.id)
        )

        with self._engine.connect() as conn:
            result = conn.execute(stmt)
            row = result.fetchone()
            if row is None:
                return item

            item.id = row.id
            conn.commit()

        return item

    def get(self, id: int) -> Document | None:
        stmt = select(self._db.documents).where(self._db.documents.c.id == id)

        with self._engine.connect() as conn:
            result = conn.execute(stmt).first()

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
        stmt = select(self._db.documents).offset(offset).limit(limit)

        with self._engine.connect() as conn:
            result = conn.execute(stmt).all()
            conn.commit()
            return [
                Document(id=d.id, title=d.title, source=d.source, content=d.content)
                for d in result
            ]

        return []

    def delete(self, id: int) -> bool:
        stmt = delete(self._db.documents).where(self._db.documents.c.id == id)

        with self._engine.connect() as conn:
            result = conn.execute(stmt)
            conn.commit()

        return result.rowcount == 1

    def get_next_id(self) -> int:
        return 0
