class AbstractEncrypter:
    # The encryption key.
    _key: str = None

    def __init__(self, key: str, size: int = 16):
        self._key = key
        self._size = size

    def getKey(self) -> str:
        return self._key

    def textPad(self, text) -> str:
        if len(text) > self._size:
            return text + b'\x00' * ((self._size - (len(text) % self._size)) % self._size)

        return text + ' ' * (self._size - len(text) % self._size)
