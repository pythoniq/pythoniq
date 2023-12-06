from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from app.libraries.osos.ososManager import OsosManager


class OsosServiceProvider(ServiceProvider):
    # Register the service provider.
    def register(self):
        self._app.singleton('osos', lambda app: OsosManager(app))

    def boot(self):
        pass
