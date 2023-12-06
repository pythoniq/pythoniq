class Response:
    _index: int = 0
    _value: str = None
    _data: [] = None

    def __init__(self, value: str):
        self._value = value
        self._data = self._value.split('\r\n')

    def data(self) -> []:
        return self._data

    def beforeItem(self) -> str:
        return self._data[self._index - 2]

    def afterItem(self) -> str:
        return self._data[self._index]

    def getIndex(self) -> int:
        return self._index

    def count(self) -> int:
        return len(self._data)

    def item(self) -> str:
        return self._data[self._index]

    def __iter__(self):
        return self

    def __next__(self):
        if self._index >= len(self._data):
            raise StopIteration

        self._index += 1

        return self._data[self._index - 1]

