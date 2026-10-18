from datetime import UTC, datetime
from pgvector.sqlalchemy import VECTOR

from sqlalchemy import (
    DateTime,
    ForeignKey,
    MetaData,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=NAMING_CONVENTION)


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
    language: Mapped[str] = mapped_column(nullable=True)
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="document", cascade="all, delete-orphan")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    def word_count(self) -> int:
        if not self.content:
            return 0

        words = self.content.split()
        return len(words)

    def is_empty(self) -> bool:
        return len(self.content) == 0

    def __post_init__(self):
        if not self.title:
            raise ValueError


class Chunk(Base):
    __tablename__ = "chunks"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    document_id = mapped_column(ForeignKey("documents.id"))
    position: Mapped[int]
    content: Mapped[str]
    document: Mapped["Document"] = relationship(back_populates="chunks")
    embedding_id = mapped_column(ForeignKey("embeddings.id"))

class Embedding(Base):
    __tablename__ = "embeddings"
    id: Mapped[int] = mapped_column(primary_key=True)
    vector: Mapped[list[float]] = mapped_column(VECTOR(384), nullable=False)
