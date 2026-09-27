from sqlalchemy import create_engine

from devdocs_hub.application.documents import DocumentService
from devdocs_hub.db.core import Database
from devdocs_hub.domain.document_repository import DocumentRepository
from devdocs_hub.settings import settings

engine = create_engine(settings.db_url, echo=True)
db = Database(engine)
repository = DocumentRepository(engine, db)


def get_document_service() -> DocumentService:
    return DocumentService(repository)
