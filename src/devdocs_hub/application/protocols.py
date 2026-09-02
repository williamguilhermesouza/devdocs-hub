from dataclasses import dataclass
from typing import Protocol

class RepositoryProtocol[T](Protocol):
    def add(self, item: T) -> T: ...
    def get(self, id: int) -> T | None: ...
    def list(self) -> list[T]: ...
    def delete(self, id: int) -> bool: ...

@dataclass
class Response:
    text: str

    def raise_for_status(self) -> "Response":
        return self

class HttpClientProtocol(Protocol):
    async def get(self, url: str) -> Response: ... 

