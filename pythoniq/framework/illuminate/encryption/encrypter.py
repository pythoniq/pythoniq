from pythoniq.framework.illuminate.contracts.encryption.decryptException import DecryptException
from pythoniq.framework.illuminate.contracts.encryption.encrypter import Encrypter as EncrypterContract
from pythoniq.framework.illuminate.contracts.encryption.stringEncrypter import StringEncrypter
from pythoniq.framework.illuminate.support.str import Str

import base64
import json
import uos


class Encrypter(EncrypterContract, StringEncrypter):
    # The encryption key.
    _key: str = None

    # The algorithm used for encryption.
    _cipher: str = None

    # The array of created "drivers".
    _drivers: dict = {}

    # The supported cipher algorithms and their properties.
    _supportedCiphers: dict = {
        'aes-128-cbc': {'size': 16, 'aead': False, 'driver': 'aesCbc'},
        'aes-256-cbc': {'size': 32, 'aead': False, 'driver': 'aesCbc'},
        'aes-128-ecb': {'size': 16, 'aead': False, 'driver': 'aesEcb'},
    }

    # Create a new encrypter instance.
    def __init__(self, key: str, cipher: str = 'aes-256-cbc') -> None:
        if not Encrypter.supported(key, cipher):
            ciphers = ', '.join(Encrypter._supportedCiphers.keys())

            raise RuntimeError(f"Unsupported cipher or incorrect key length. Supported ciphers are: {ciphers}.")

        self._key = key
        self._cipher = cipher

    # Get the default driver name.
    def getDefaultDriver(self) -> str:
        return Encrypter._supportedCiphers[self._cipher.lower()]['driver']

    # Get a driver instance.
    def driver(self, driver: str = None) -> any:
        driver = driver or self.getDefaultDriver()

        if not driver:
            raise RuntimeError('Unable to resolve NULL driver for [{}]'.format(self.__class__.__name__))

        # If the given driver has not been created before, we will create the instances
        # here and cache it so we can return it next time very quickly. If there is
        # already a driver created by this name, we'll just return that instance.
        if driver not in self._drivers:
            self._drivers[driver] = self._createDriver(driver)

        return self._drivers[driver]

    # Create a new driver instance.
    def _createDriver(self, driver: str) -> any:
        # First, we will determine if a custom driver creator exists for the given driver and
        # if it does not we will check for a creator method for the driver. Custom creator
        # callbacks allow developers to build their own "drivers" easily using Closures.

        method = 'create' + Str().studly(driver) + 'Driver'

        if hasattr(self, method):
            return getattr(self, method)()

        raise RuntimeError('Driver [{}] not supported.'.format(driver))

    # Create an instance of the AES - ECB encryption driver.
    def createAesEcbDriver(self) -> any:
        from pythoniq.framework.illuminate.encryption.aesEcbEncrypter import AesEcbEncrypter
        return AesEcbEncrypter(self._key, Encrypter._supportedCiphers[self._cipher.lower()]['size'])

    # Create an instance of the AES - CBC encryption driver.
    def createAesCbcDriver(self) -> any:
        from pythoniq.framework.illuminate.encryption.aesCbcEncrypter import AesCbcEncrypter
        return AesCbcEncrypter(self._key, Encrypter._supportedCiphers[self._cipher.lower()]['size'])

    # Determine if the given key and cipher combination is valid.
    @staticmethod
    def supported(key: str, cipher: str) -> bool:
        if cipher.lower() not in Encrypter._supportedCiphers:
            return False

        return len(key) == Encrypter._supportedCiphers[cipher.lower()]['size']

    # Create a new encryption key for the given cipher.
    @staticmethod
    def generateKey(cipher: str) -> bytes:
        return uos.urandom(Encrypter._supportedCiphers[cipher.lower()]['size'])

    # Encrypt the given value.
    def encrypt(self, value: str, serialize: bool = True) -> str:
        return self.driver().encrypt(value, serialize)

    # Encrypt a string without serialization.
    def encryptString(self, value: str) -> str:
        return self.encrypt(value, False)

    # Decrypt the given value.
    def decrypt(self, payload: str, unserialize: bool = True) -> str:
        return self.driver().decrypt(payload, unserialize)

    # Decrypt the given string without unserialization.
    def decryptString(self, payload: str) -> str:
        return self.decrypt(payload, False)

    # Create a MAC for the given value.
    def hash(self, iv: str, value: any) -> str:
        raise NotImplementedError

    # Get the JSON array from the given payload.
    def getJsonPayload(self, payload: str) -> dict:
        payload = json.loads(base64.b64decode(payload))

        # If the payload is not valid JSON or does not have the proper keys set we will
        # assume it is invalid and bail out of the routine since we will not be able
        # to decrypt the given value. We'll also check the MAC for this encryption.
        if not self._validPayload(payload):
            raise DecryptException('The payload is invalid.')

        if not self._supportedCiphers[self._cipher.lower()]['aead'] and not self._validMac(payload):
            raise DecryptException('The MAC is invalid.')

        return payload

    # Verify that the encryption payload is valid.
    def _validPayload(self, payload: any) -> bool:
        if not isinstance(payload, dict):
            return False

        for item in ['iv', 'value', 'mac']:
            if not item in payload or not isinstance(payload[item], str):
                return False

        if tag in payload and not isinstance(payload['tag'], str):
            return False

        return True

    # Determine if the MAC for the given payload is valid.
    def _validMac(self, payload: dict) -> bool:
        raise NotImplementedError

    # Ensure the given tag is a valid tag given the selected cipher.
    def _ensureTagIsValid(self, tag: str) -> None:
        if self._supportedCiphers[self._cipher.lower()]['aead'] and len(tag) != 16:
            raise DecryptException('The only supported authenticated cipher tag length is 16 bytes.')

        if not self._supportedCiphers[self._cipher.lower()]['aead'] and len(tag) != 16:
            raise DecryptException('The only supported cipher tag length is 16 bytes.')

    # Get the encryption key that the encrypter is currently using.
    def getKey(self) -> str:
        return self._key

