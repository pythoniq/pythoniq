from pythoniq.framework.illuminate.encryption.abstractEncrypter import AbstractEncrypter

import uos
from ucryptolib import aes


class AesCbcEncrypter(AbstractEncrypter):
    _iv: bytes = None

    def getCipher(self):
        return aes(self.getKey(), 2, self._getIv())

    # Encrypt the given value.
    def encrypt(self, value: str, serialize: bool = True) -> bytes:
        if serialize is False:
            pass

        return self._getIv() + self.getCipher().encrypt(self.textPad(value))

    # Encrypt a string without serialization.
    def encryptString(self, value: str) -> str:
        return self.encrypt(value, False).decode()

    # Decrypt the given value.
    def decrypt(self, payload: str, unserialize: bool = True) -> bytes | None:
        if unserialize is False:
            pass

        return self.getCipher().decrypt(payload)[self._size:]

    # Decrypt the given string without unserialization.
    def decryptString(self, payload: str) -> str:
        return self.decrypt(payload, False).decode()

    def _getIv(self) -> bytes:
        if self._iv is None:
            self._iv = uos.urandom(self._size)

        return self._iv
