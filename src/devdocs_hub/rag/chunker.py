from devdocs_hub.domain.documents import Document
from devdocs_hub.db.core import Chunk


class Chunker:
    def __init__(self, max_words: int = 400, overlap_words: int = 80):
        self.max_words = max_words
        self.overlap_words = overlap_words

    def chunk_document(
        self,
        content: Document,
        max_words: int | None = None,
        overlap_words: int | None = None,
    ) -> list[Chunk]:
        if not max_words:
            max_words = self.max_words
        if not overlap_words:
            overlap_words = self.overlap_words

        words_count = content.word_count()

        if words_count <= max_words:
            return [
                Chunk(
                    document_id=content.id,
                    position=0,
                    content=content.content,
                    embedding_id=None,
                )
            ]

        position = 0
        cursor = 0
        chunks = []
        words = content.content.split()

        while True:
            chunk_end = min(words_count, cursor + max_words)
            chunk_content = " ".join(words[cursor:chunk_end])
            chunk = Chunk(
                document_id=content.id,
                position=position,
                content=chunk_content,
                embedding_id=None,
            )
            chunks.append(chunk)

            if cursor + max_words >= words_count:
                break

            position += 1
            cursor += max_words
            cursor -= overlap_words

        return chunks
