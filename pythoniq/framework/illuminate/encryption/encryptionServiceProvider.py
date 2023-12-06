from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from pythoniq.framework.illuminate.encryption.encrypter import Encrypter
from pythoniq.framework.illuminate.encryption.missingAppKeyException import MissingAppKeyException
from pythoniq.framework.illuminate.support.helpers import tap
from pythoniq.framework.illuminate.support.str import Str
import base64


class EncryptionServiceProvider(ServiceProvider):
    # Register the service provider.
    def register(self) -> None:
        self._registerEncrypter()
        self._registerSerializableClosureSecurityKey()

    # Register the encrypter.
    def _registerEncrypter(self) -> None:
        def fn(app):
            config = app.make('config').get('app')

            return Encrypter(self._parseKey(config), config['cipher'])

        self._app.singleton('encrypter', fn)

    # Configure Serializable Closure signing for security.
    def _registerSerializableClosureSecurityKey(self) -> None:
        config = self._app.make('config').get('app')

        # raise NotImplementedError

    # Parse the encryption key.
    def _parseKey(self, config: dict) -> str:
        key = self._key(config)
        prefix = 'base64:'
        if Str.startsWith(key, prefix):
            key = base64.b64decode(Str.after(key, prefix))

        return key

    # Extract the encryption key from the given configuration.
    def _key(self, config: dict) -> str:
        def fn(key):
            if not key:
                raise MissingAppKeyException()

        return tap(config['key'], fn)
