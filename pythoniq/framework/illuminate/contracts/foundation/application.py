from pythoniq.framework.illuminate.container.container import Container
from pythoniq.framework.illuminate.contracts.foundation.cachesConfiguration import CachesConfiguration
from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider


class Application(Container, CachesConfiguration):
    # Get the version number of the application.
    def version(self) -> str:
        pass

    # Get the base path of the Laravel installation.
    def basePath(self, path: str = '') -> str:
        pass

    # Get the path to the bootstrap directory.
    def bootstrapPath(self, path: str = '') -> str:
        pass

    # Get the path to the application configuration files.
    def configPath(self, path: str = '') -> str:
        pass

    # Get the path to the database directory.
    def databasePath(self, path: str = '') -> str:
        pass

    # Get the path to the language files.
    def langPath(self, path: str = '') -> str:
        pass

    # Get the path to the public directory.
    def publicPath(self, path: str = '') -> str:
        pass

    # Get the path to the resources directory.
    def resourcePath(self, path: str = '') -> str:
        pass

    # Get the path to the storage directory.
    def storagePath(self, path: str = '') -> str:
        pass

    # Get or check the current application environment.
    def environment(self, **environments) -> str | bool:
        pass

    # Determine if the application is running in the console.
    def runningInConsole(self) -> bool:
        pass

    # Determine if the application is running unit tests.
    def runningUnitTests(self) -> bool:
        pass

    # Determine if the application is running with debug mode enabled.
    def hasDebugModeEnabled(self) -> bool:
        pass

    # Get an instance of the maintenance mode manager implementation.
    def maintenanceMode(self):
        pass

    # Determine if the application is currently down for maintenance.
    def isDownForMaintenance(self) -> bool:
        pass

    # Register all of the configured providers.
    def registerConfiguredProviders(self) -> None:
        pass

    # Register a service provider with the application.
    def register(self, provider: ServiceProvider, force: bool = False) -> ServiceProvider:
        pass

    # Register a deferred provider and service.
    def registerDeferredProvider(self, provider: str, service: str | None = None) -> None:
        pass

    # Resolve a service provider instance from the class name.
    def resolveProvider(self, provider: str) -> ServiceProvider:
        pass

    # Boot the application's service providers.
    def boot(self) -> None:
        pass

    # Register a new boot listener.
    def booting(self, callback: callable) -> None:
        pass

    # Register a new "booted" listener.
    def booted(self, callback: callable) -> None:
        pass

    # Run the given array of bootstrap classes.
    def bootstrapWith(self, bootstrappers: list) -> None:
        pass

    # Get the current application locale.
    def getLocale(self) -> str:
        pass

    # Get the application namespace.
    def getNamespace(self) -> str:
        pass

    # Get the registered service provider instances if any exist.
    def getProviders(self, provider: ServiceProvider | None) -> list:
        pass

    # Determine if the application has been bootstrapped before.
    def hasBeenBootstrapped(self) -> bool:
        pass

    # Load and boot all of the remaining deferred providers.
    def loadDeferredProviders(self) -> None:
        pass

    # Set the current application locale.
    def setLocale(self, locale: str) -> None:
        pass

    # Determine if middleware has been disabled for the application.
    def shouldSkipMiddleware(self) -> bool:
        pass

    # Register a terminating callback with the application.
    def terminating(self, callback: callable):
        pass

    # Terminate the application.
    def terminate(self) -> None:
        pass

    def environmentFile(self):
        pass

    def environmentPath(self):
        pass

    def loadEnvironmentFrom(self, file):
        pass
