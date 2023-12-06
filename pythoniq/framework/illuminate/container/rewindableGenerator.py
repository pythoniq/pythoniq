class RewindableGenerator:
    _index = 0

    # The generator callback.
    _generator: callable = None

    # The number of tagged services.
    _count: callable | int = None

    def __init__(self, generator: callable, count: callable | int):
        self._generator = generator
        self._count = count

    # Get an iterator from the generator.
    def getIterator(self):
        return self._generator()

    # Get the total number of tagged services.
    def count(self) -> int:
        count = self._count
        if callable(count):
            self._count = count()

        return self._count

    def __iter__(self):
        return self.getIterator()

