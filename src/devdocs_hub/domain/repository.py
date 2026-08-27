# usually generic repository is not 
# so nice, but i'll use it here
class Repository[T]:
    def __init__(self):
        self.data: dict[int, T] = {}
        self.next_id: int = 0

    def add(self, item: T) -> T:
        self.data[self.next_id] = item
        self.next_id += 1
        return item

    def get(self, id: int) -> T | None:
        return self.data.get(id)

    def list(self) -> list[T]:
        return list(self.data.values())

    def delete(self, id: int) -> bool:
        if id in self.data:
            del self.data[id]
            return True
        
        return False

