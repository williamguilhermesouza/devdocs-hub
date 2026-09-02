
# usually generic repository is not 
# so nice, but i'll use it here
class InMemoryRepository[T]:
    def __init__(self):
        self._data: dict[int, T] = {}
        self._next_id: int = 0

    def add(self, item: T) -> T:
        self._data[self._next_id] = item
        self._next_id += 1
        return item

    def get(self, id: int) -> T | None:
        return self._data.get(id)

    def list(self) -> list[T]:
        return list(self._data.values())

    def delete(self, id: int) -> bool:
        if id in self._data:
            del self._data[id]
            return True
        
        return False

    def get_next_id(self) -> int:
        return self._next_id

