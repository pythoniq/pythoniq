from pythoniq.framework.illuminate.support.manager import Manager
from pythoniq.framework.illuminate.contracts.hashing.hasher import Hasher as HasherContract


class HashManager(Manager, HasherContract):
    # Get the default driver name.
    def getDefaultDriver(self) -> str:
        return self._config.get('hashing.default', 'sha256')

    # Set the default driver name.
    def setDefaultDriver(self, name: str) -> None:
        return self._config.set('hashing.default', name)

    # Get the log connection configuration.
    def _configurationFor(self, name: str) -> dict:
        return self._config.get('hashing.drivers.' + name, {})

    # Get a filesystem instance.
    def hasher(self, name: str = None) -> HasherContract:
        return self.driver(name)

    # Drivers

    # Create an instance of the Sha256 hash Driver.
    def createSha256Driver(self, config: dict) -> HasherContract:
        from pythoniq.framework.illuminate.hashing.sha256Hasher import Sha256Hasher

        return Sha256Hasher(config)

    # Create an instance of the Sha1 hash Driver.
    def createSha1Driver(self, config: dict) -> HasherContract:
        from pythoniq.framework.illuminate.hashing.sha1Hasher import Sha1Hasher

        return Sha1Hasher(config)

    # Create an instance of the MD5 hash Driver.
    def createMd5Driver(self, config: dict) -> HasherContract:
        from pythoniq.framework.illuminate.hashing.md5Hasher import Md5Hasher

        return Md5Hasher(config)

    # Methods

    # Get information about the given hashed value.
    def info(self, hashedValue: str) -> dict:
        return self.driver().info(hashedValue)

    # Hash the given value.
    def make(self, value: str, options: dict = None) -> str:
        return self.driver().make(value, options)

    # Check the given plain value against a hash.
    def check(self, value: str, hashedValue: str, options: dict = None) -> bool:
        return self.driver().check(value, hashedValue, options)

    # Check if the given hash has been hashed using the given options.
    def needsRehash(self, hashedValue: str, options: dict = None) -> bool:
        return self.driver().needsRehash(hashedValue, options)

    # Determine if a given string is already hashed.
    def isHashed(self, value: str) -> bool:
        return self.driver().isHashed(value)
