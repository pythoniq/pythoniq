from app.libraries.osos.ososContract import OsosContract
from pythoniq.framework.illuminate.contracts.config.repository import Repository as ConfigContract
from pythoniq.framework.illuminate.config.repository import Repository as Config


class AbstractOsos(OsosContract):
    _config: ConfigContract = None

    # Create a new gsm instance.
    def __init__(self, config: dict):
        self._config = Config(config)
