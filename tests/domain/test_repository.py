from devdocs_hub.domain.documents import Document
from devdocs_hub.domain.repository import InMemoryRepository


class TestRepository:
    def test_add_returns_same_obj(self):
        doc_repo = InMemoryRepository[Document]()
        doc = Document(0, "title", "source", "content")
        added = doc_repo.add(item=doc)
        assert doc == added

    def test_get_returns_same_obj(self):
        doc_repo = InMemoryRepository[Document]()
        doc = Document(0, "title", "source", "content")
        added = doc_repo.add(doc)
        get_res = doc_repo.get(0)
        assert doc == added == get_res

    def test_missing_id_returns_none(self):
        doc_repo = InMemoryRepository[Document]()
        doc = Document(0, "title", "source", "content")
        added = doc_repo.add(doc)
        added = doc_repo.get(3)
        assert added == None

    def test_list_returns_all_docs(self):
        doc_repo = InMemoryRepository[Document]()
        doc = Document(0, "title", "source", "content")
        doc2 = Document(1, "title1", "source1", "content1")
        doc3 = Document(2, "title2", "source2", "content2")
        doc_repo.add(doc)
        doc_repo.add(doc2)
        doc_repo.add(doc3)

        all_docs = doc_repo.list()
        assert all_docs == [doc, doc2, doc3]

    def test_delete_in_repo(self):
        doc_repo = InMemoryRepository[Document]()
        doc = Document(0, "title", "source", "content")
        doc_repo.add(doc)
        deleted = doc_repo.delete(0)
        assert deleted

        deleted = doc_repo.delete(0)
        assert not deleted
