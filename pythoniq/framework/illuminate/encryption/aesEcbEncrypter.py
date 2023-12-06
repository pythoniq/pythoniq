from pythoniq.framework.illuminate.encryption.abstractEncrypter import AbstractEncrypter

from ucryptolib import aes


class AesEcbEncrypter(AbstractEncrypter):
    def getCipher(self) -> aes:
        return aes(self.getKey(), 1)

    # Encrypt the given value.
    def encrypt(self, value: str, serialize: bool = True) -> bytes:
        if serialize is False:
            pass

        return self.getCipher().encrypt(self.textPad(value))

    # Encrypt a string without serialization.
    def encryptString(self, value: str) -> str:
        return self.encrypt(value, False)

    # Decrypt the given value.
    def decrypt(self, payload: str, unserialize: bool = True) -> bytes | None:
        if unserialize is False:
            pass

        return self.getCipher().decrypt(payload)

    # Decrypt the given string without unserialization.
    def decryptString(self, payload: str) -> str:
        return self.decrypt(payload, False).decode('utf-8')
