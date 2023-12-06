from pythoniq.framework.illuminate.hashing.abstractHasher import AbstractHasher

import hashlib
import binascii


class Md5Hasher(AbstractHasher):
    # Hash the given value.
    def make(self, value: str, options: dict = None) -> bytes:
        value = str(value).encode('utf-8')

        return binascii.hexlify(hashlib.md5(value).digest())
