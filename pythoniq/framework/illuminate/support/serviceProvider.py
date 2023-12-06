from pythoniq.framework.illuminate.contracts.support.deferrableProvider import DeferrableProvider
from pythoniq.framework.illuminate.support.defaultProviders import DefaultProviders

namespace = 'pythoniq.framework.illuminate.support.serviceProvider'


class ServiceProvider:
    # The application instance.
    _app = None

    # All of the registered booting callbacks.
    _bootingCallbacks: list = []

    # All of the registered booted callbacks.
    _bootedCallbacks: list = []

    # Create a new service provider instance.
    def __init__(self, app):
        self._app = app

    # Register any application services.
    def register(self):
        pass

    # Register a booting callback to be run before the "boot" method is called.
    def booting(self, callback):
        self._bootingCallbacks.append(callback)

    # Register a booted callback to be run after the "boot" method is called.
    def booted(self, callback):
        self._bootedCallbacks.append(callback)

    # Call the registered booting callbacks.
    def callBootingCallbacks(self):
        index = 0

        while index < len(self._bootingCallbacks):
            self._app.call(self._bootingCallbacks[index])
            del self._bootingCallbacks[index]
            index += 1

    # Call the registered booted callbacks.
    def callBootedCallbacks(self):
        index = 0

        while index < len(self._bootedCallbacks):
            self._app.call(self._bootedCallbacks[index])
            del self._bootedCallbacks[index]
            index += 1

    # Get the services provided by the provider.
    def provides(self):
        return []

    # Get the events that trigger this service provider to register.
    def when(self):
        return []

    # Determine if the provider is deferred.
    def isDeferred(self) -> bool:
        return issubclass(self, DeferrableProvider)

    # Get the default providers for a Laravel application.
    @staticmethod
    def defaultProviders() -> DefaultProviders:
        return DefaultProviders()
