from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from pythoniq.framework.illuminate.contracts.support.deferrableProvider import DeferrableProvider
from pythoniq.framework.illuminate.hashing.hashManager import HashManager


class HashServiceProvider(ServiceProvider, DeferrableProvider):
    # Register the service provider.
    def register(self):
        self._app.singleton('hash', lambda app: HashManager(app))

        self._app.singleton('hash.driver', lambda app: app['hash'].driver())

    # Get the services provided by the provider.
    def provides(self):
        return ['hash', 'hash.driver']
