from datetime import UTC, datetime

from sqlalchemy import (
    Column,
    DateTime,
    Engine,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
)


class Database:
    def __init__(self, engine: Engine):
        self._metadata_obj = MetaData()
        self._engine = engine

    def init(self):

        self.users = Table(
            "users",
            self._metadata_obj,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("username", String),
        )

        self.documents = Table(
            "documents",
            self._metadata_obj,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("title", String, nullable=False),
            Column("source", String),
            Column("content", String),
            Column(
                "created_at",
                DateTime(timezone=True),
                default=lambda: datetime.now(UTC),
            ),
        )
        self.chunks = Table(
            "chunks",
            self._metadata_obj,
            Column("id", Integer, primary_key=True, autoincrement=True),
            Column("document_id", ForeignKey("documents.id")),
            Column("position", Integer),
            Column("content", String),
            Column("embedding_id", Integer, nullable=True),
        )

        self._metadata_obj.create_all(self._engine)


# DON'T USE THAT YET, LEARN SQLALCHEMY CORE FIRST
# from datetime import datetime, timezone
# from sqlalchemy import DateTime, Engine, ForeignKey, String
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
# from sqlalchemy.orm.session import PROVISIONING_CONNECTION


# class Base(DeclarativeBase):
#     pass
#
#
# class User(Base):
#     __tablename__ = 'users'
#     id: Mapped[int] = mapped_column(
#         primary_key=True, autoincrement=True, nullable=False
#     )
#     username: Mapped[str] = mapped_column(String(30), nullable=False)
#
#
# class Document(Base):
#     __tablename__ = 'documents'
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     title: Mapped[str] = mapped_column(nullable=False)
#     source: Mapped[str]
#     content: Mapped[str]
#     created_at: Mapped[datetime] = mapped_column(
#         DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
#     )
#
#
# class Chunk(Base):
#     __tablename__ = 'chunks'
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     document_id = mapped_column(ForeignKey("documents.id"))
#     position: Mapped[int]
#     content: Mapped[str]
#     embedding_id = Mapped[int]
#
#
# def emit_ddl(engine: Engine):
#     Base.metadata.create_all(engine)
