from datetime import UTC, datetime

from sqlalchemy import (
    DateTime,
    Engine,
    ForeignKey,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Database:
    def __init__(self, engine: Engine):
        self._engine = engine

    def init(self):
        Base.metadata.create_all(self._engine)


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, nullable=False
    )
    username: Mapped[str] = mapped_column(String(30), nullable=False)


class Document(Base):
    __tablename__ = "documents"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(nullable=False)
    source: Mapped[str]
    content: Mapped[str]
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )


class Chunk(Base):
    __tablename__ = "chunks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    document_id = mapped_column(ForeignKey("documents.id"))
    position: Mapped[int]
    content: Mapped[str]
    document: Mapped["Document"] = relationship(back_populates="chunks")
    embedding_id = Mapped[int]
