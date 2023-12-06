class Encrypter:
    # Encrypt the given value.
    def encrypt(self, value: str, serialize: bool = True) -> str:
        pass

    # Decrypt the given value.
    def decrypt(self, payload: str, unserialize: bool = True) -> str:
        pass

    # Get the encryption key that the encrypter is currently using.
    def getKey(self) -> str:
        pass
