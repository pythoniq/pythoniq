class Hasher:
    # Get information about the given hashed value.
    def info(self, hashedValue: str) -> dict:
        pass

    # Hash the given value.
    def make(self, value: str, options: dict = None) -> str:
        pass

    # Check the given plain value against a hash.
    def check(self, value: str, hashedValue: str, options: dict = None) -> bool:
        pass

    # Check if the given hash has been hashed using the given options.
    def needsRehash(self, hashedValue: str, options: dict = None) -> bool:
        pass
