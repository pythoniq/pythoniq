from pythoniq.framework.illuminate.contracts.hashing.hasher import Hasher as HasherContract


class AbstractHasher(HasherContract):
    _config: dict = None

    # Create a new hasher instance.
    def __init__(self, config: dict):
        self._config = config

    # Get information about the given hashed value.
    def info(self, hashedValue: str) -> dict:
        raise NotImplementedError()

    # Check the given plain value against a hash.
    def check(self, value: str, hashedValue: str, options: dict = None) -> bool:
        if hashedValue == '' or hashedValue is None or len(hashedValue) == 0:
            return False

        return self.make(value, options) == hashedValue
