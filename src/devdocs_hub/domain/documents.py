from dataclasses import dataclass


@dataclass
class Document:
    id: int | None
    title: str
    source: str
    content: str

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

