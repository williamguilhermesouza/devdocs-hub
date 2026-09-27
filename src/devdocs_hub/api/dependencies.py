from sqlalchemy import create_engine

from devdocs_hub.application.documents import DocumentService
from devdocs_hub.db.core import Database
from devdocs_hub.domain.document_repository import DocumentRepository

# repository = InMemoryRepository[Document]()
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
# engine = create_engine(settings.db_url, echo=True)
db = Database(engine)
db.init()
repository = DocumentRepository(engine, db)


def get_document_service() -> DocumentService:
    return DocumentService(repository)
