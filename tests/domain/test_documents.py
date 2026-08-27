from hypothesis import given
from hypothesis import strategies as st
from pytest import raises

from devdocs_hub.domain.documents import Document


class TestDocuments:
    def test_create(self):
        document = Document(id=0, title='Doc01', source='citation', content='lorem ipsum')
        assert document != None

    @given(st.text())
    def test_word_count(self, text: str):
        wc = len(text.split())
        document = Document(id=0, title='Doc01', source='citation', content=text)
        assert wc == document.word_count()

    def test_empty_content(self):
        document = Document(id=0, title='Doc01', source='citation', content='')
        assert document.word_count() == 0
        assert document.is_empty()

    def test_empty_title_raises(self):
        with raises(ValueError):
            Document(id=0, title='', source='citation', content='')



