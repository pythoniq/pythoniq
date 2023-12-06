from pythoniq.framework.illuminate.container.container import Container
from pythoniq.framework.illuminate.contracts.foundation.application import Application as ApplicationContract
from pythoniq.framework.illuminate.contracts.foundation.cachesConfiguration import CachesConfiguration
from pythoniq.framework.illuminate.contracts.foundation.maintenanceMode import \
    MaintenanceMode as MaintenanceModeContract
from pythoniq.framework.illuminate.contracts.console.kernel import Kernel as ConsoleKernelContract
from pythoniq.framework.illuminate.support.helpers import _import_
from pythoniq.framework.illuminate.support.serviceProvider import ServiceProvider
from pythoniq.framework.illuminate.events.eventServiceProvider import EventServiceProvider
from pythoniq.framework.illuminate.log.logServiceProvider import LogServiceProvider
from pythoniq.framework.illuminate.foundation.bootstrap.loadEnvironmentVariables import LoadEnvironmentVariables
from pythoniq.framework.illuminate.foundation.environmentDetector import EnvironmentDetector
from pythoniq.framework.illuminate.foundation.events.localeUpdated import LocaleUpdated
from pythoniq.framework.illuminate.contracts.cache.repository import Repository as CacheContract
from pythoniq.framework.illuminate.contracts.config.repository import Repository as ConfigContract
from pythoniq.framework.illuminate.contracts.encryption.encrypter import Encrypter as EncrypterContract
from pythoniq.framework.illuminate.contracts.events.dispatcher import Dispatcher as EventContract
from pythoniq.framework.illuminate.contracts.filesystem.filesystem import Filesystem as StorageContract
from pythoniq.framework.illuminate.contracts.pipeline.pipeline import Pipeline as PipelineContract
from pythoniq.framework.illuminate.contracts.hashing.hasher import Hasher as HasherContract
from pythoniq.framework.illuminate.contracts.log.logger import Logger as LoggerContract
from pythoniq.framework.illuminate.contracts.queue.queue import Queue as QueueContract
from pythoniq.framework.illuminate.contracts.monitor.monitor import Monitor as MonitorContract
from pythoniq.framework.illuminate.collections.helpers import value
from pythoniq.framework.illuminate.support.env import Env
from lib.helpers import is_file, is_dir
from lib.printr import print_r

import time
import gc


class Application(Container, ApplicationContract, CachesConfiguration):
    # The Pythoniq framework version.
    VERSION = '0.0.0'

    # The base path for the Laravel installation.
    _basePath: str = '/'

    _startedAt: float = None

    # Indicates if the application has been bootstrapped before.
    _hasBeenBootstrapped: bool = False

    # Indicates if the application has "booted".
    _booted: bool = False

    # The array of booting callbacks.
    _bootingCallbacks: list = []

    # The array of booted callbacks.
    _bootedCallbacks: list = []

    # The array of terminating callbacks.
    _terminatingCallbacks: list = []

    # All of the registered service providers.
    _serviceProviders: list = []

    # The names of the loaded service providers.
    _loadedProviders: list = []

    # The deferred services and their providers.
    _deferredServices: list = []

    # The custom application path defined by the developer.
    _bootstrapPath: str | None = None

    # The custom application path defined by the developer.
    _appPath: str | None = None

    # The custom configuration path defined by the developer.
    _configPath: str | None = None

    # The custom database path defined by the developer.
    _databasePath: str | None = None

    # The custom language path defined by the developer.
    _langPath: str | None = None

    # The custom public path defined by the developer.
    _publicPath: str | None = None

    # The custom storage path defined by the developer.
    _storagePath: str | None = None

    # The custom environment path defined by the developer.
    _environmentPath: str | None = None

    # The environment file to load during bootstrapping.
    _environmentFile: str = '.env'

    # Indicates if the application has been bootstrapped.
    _isRunningInConsole: bool | None = None

    # The application namespace.
    _namespace: str | None = None

    # The prefixes of absolute cache paths for use during normalization.
    _absoluteCachePathPrefixes: list = ['/', '\\']

    def __init__(self, basePath: str = None):
        self._startedAt = time.time()

        if basePath:
            self.setBasePath(basePath)

        self._registerBaseBindings()
        self._registerBaseServiceProviders()
        self.registerCoreContainerAliases()

    # Get the version number of the application.
    def version(self) -> str:
        return self.VERSION

    # Register the basic bindings into the container.
    def _registerBaseBindings(self) -> None:
        # self.setInstance(self)

        self.instance('app', self)
        self.instance(Container, self)
        # self.singleton(Mix)  # Get the path to a versioned Mix file.
        # self.singleton(PackageManifest)

    # Register all of the base service providers.
    def _registerBaseServiceProviders(self) -> None:
        print_r('Register all of the base service providers. Provider: ' + 'EventServiceProvider')
        self.register(EventServiceProvider(self))

        print_r('Register all of the base service providers. Provider: ' + 'LogServiceProvider')
        self.register(LogServiceProvider(self))

    # Run the given array of bootstrap classes.
    def bootstrapWith(self, bootstrappers: list) -> None:
        self._hasBeenBootstrapped = True

        for bootstrapper in bootstrappers:
            # self['events'].dispatch('bootstrapping: ' + bootstrapper, [self])

            print_r('Run the given array of bootstrap classes. Service: ' + bootstrapper.__name__)
            self.make(bootstrapper).bootstrap(self)

            # self['events'].dispatch('bootstrapped: ' + bootstrapper, [self])

    # Register a callback to run after loading the environment.
    def afterLoadingEnvironment(self, callback: callable) -> None:
        self.afterBootstrapping(LoadEnvironmentVariables, callback)

    # Register a callback to run before a bootstrapper.
    def beforeBootstrapping(self, bootstrapper: str | object, callback: callable) -> None:
        self['events'].dispatch('bootstrapping: ' + bootstrapper, callback)

    # Register a callback to run after a bootstrapper.
    def afterBootstrapping(self, bootstrapper: str | object, callback: callable) -> None:
        self['events'].dispatch('bootstrapped: ' + bootstrapper, callback)

    # Determine if the application has been bootstrapped before.
    def hasBeenBootstrapped(self) -> bool:
        return self._hasBeenBootstrapped

    # Set the base path for the application.
    def setBasePath(self, basePath: str):
        if not is_dir(basePath):
            raise Exception('Application base path "' + basePath + '" does not exist or is not a directory.')

        self._basePath = basePath.rstrip('/')

        self._bindPathsInContainer()

        return self

    # Set the started at for the application.
    def setStartedAt(self, startedAt: float) -> None:
        self._startedAt = startedAt

    # Bind all of the application paths in the container.
    def _bindPathsInContainer(self) -> None:
        self.instance('path', self.path())
        self.instance('path.base', self.basePath())
        self.instance('path.config', self.configPath())
        self.instance('path.database', self.databasePath())
        self.instance('path.public', self.publicPath())
        self.instance('path.resources', self.resourcePath())
        self.instance('path.storage', self.storagePath())

        def fn():
            directory = self.basePath('.pythoniq')
            if is_dir(directory):
                return directory
            return self.basePath('bootstrap')

        self.useBootstrapPath(value(fn))

        def fn():
            directory = self.resourcePath('lang')
            if is_dir(directory):
                return directory
            return self.basePath('lang')

        self.useLangPath(value(fn))

    # Get the path to the application "app" directory.
    def path(self, path: str = '') -> str:
        return self.joinPaths(self._appPath or self.basePath('app'), path)

    # Set the application directory.
    def useAppPath(self, path: str):
        self._appPath = path

        self.instance('path', path)

        return self

    # Get the base path of the Laravel installation.
    def basePath(self, path: str = '') -> str:
        return self.joinPaths(self._basePath, path)

    # Get the start at of the Laravel installation.
    def startedAt(self) -> float:
        return self._startedAt

    # Get the path to the bootstrap directory.
    def bootstrapPath(self, path: str = '') -> str:
        return self.joinPaths(self._bootstrapPath, path)

    # Set the bootstrap file directory.
    def useBootstrapPath(self, path: str):
        self._bootstrapPath = path

        self.instance('app.bootstrap', path)

        return self

    # Get the path to the application configuration files.
    def configPath(self, path: str = '') -> str:
        return self.joinPaths(self._configPath or self.basePath('config'), path)

    # Set the configuration directory.
    def useConfigPath(self, path: str):
        self._configPath = path

        self.instance('path.config', path)

        return self

    # Get the path to the database directory.
    def databasePath(self, path: str = '') -> str:
        return self.joinPaths(self._databasePath or self.basePath('database'), path)

    # Set the database directory.
    def useDatabasePath(self, path: str):
        self._databasePath = path

        self.instance('path.database', path)

        return self

    # Get the path to the language files.
    def langPath(self, path: str = '') -> str:
        return self.joinPaths(self._langPath, path)

    # Set the language file directory.
    def useLangPath(self, path: str):
        self._langPath = path

        self.instance('path.lang', path)

        return self

    # Get the path to the public / web directory.
    def publicPath(self, path: str = '') -> str:
        return self.joinPaths(self._publicPath or self.basePath('public'), path)

    # Set the public / web directory.
    def usePublicPath(self, path: str):
        self._publicPath = path

        self.instance('path.public', path)

        return self

    # Get the path to the storage directory.
    def storagePath(self, path: str = '') -> str:
        return self.joinPaths(self._storagePath or self.basePath('storage'), path)

    # Set the storage directory.
    def useStoragePath(self, path: str):
        self._storagePath = path

        self.instance('path.storage', path)

        return self

    # Get the path to the resources directory.
    def resourcePath(self, path: str = '') -> str:
        return self.joinPaths(self._storagePath or self.basePath('resources'), path)

    # Get the path to the views directory.
    def viewPath(self, path: str = '') -> str:
        viewPath = self['config'].get('view.paths')[0]
        return self.joinPaths(viewPath, path)

    # Join the given paths together.
    def joinPaths(self, basePath: str, path: str = '') -> str:
        if path != '':
            return basePath + '/' + path.lstrip('/')

        return basePath

    # Get the path to the environment file directory.
    def environmentPath(self) -> str:
        if self._environmentPath:
            return self._environmentPath

        return self._basePath

    # Set the directory for the environment file.
    def useEnvironmentPath(self, path: str):
        self._environmentPath = path

        return self

    # Set the environment file to be loaded during bootstrapping.
    def loadEnvironmentFrom(self, file: str):
        self._environmentFile = file

        return self

    # Get the environment file the application is using.
    def environmentFile(self) -> str:
        return self._environmentFile or '.env'

    # Get the fully qualified path to the environment file.
    def environmentFilePath(self) -> str:
        return self.environmentPath() + '/' + self.environmentFile()

    # Get or check the current application environment.
    def environment(self, *environments: []) -> str | bool:
        if len(environments) > 0:
            return self.env in environments

        return self['env']

    # Determine if the application is in the local environment.
    def isLocal(self) -> bool:
        return self['env'] == 'local'

    # Determine if the application is in the production environment.
    def isProduction(self) -> bool:
        return self['env'] == 'production'

    # @todo checking
    # Detect the application's current environment.
    def detectEnvironment(self, callback: callable) -> str:
        self['env'] = (EnvironmentDetector()).detect(callback, None)
        return self['env']

    #  Determine if the application is running in the console.
    def runningInConsole(self) -> bool:
        if self._isRunningInConsole is None:
            self._isRunningInConsole = Env.get('APP_RUNNING_IN_CONSOLE')

        return self._isRunningInConsole

    # Determine if the application is running unit tests.
    def runningUnitTests(self) -> bool:
        return False

    # Determine if the application is running with debug mode enabled.
    def hasDebugModeEnabled(self) -> bool:
        return bool(self['config'].get('app.debug'))

    # Register all of the configured providers.
    def registerConfiguredProviders(self) -> None:
        providers = self.make('config').get('app.providers', [])

        for key, provider in enumerate(providers):
            providers[key] = _import_(provider)

        for provider in providers:
            print_r('Register all of the configured providers.. Service: ' + provider.__name__ + '')
            self.register(provider(self))

        self.addDeferredServices(providers)

        """
        @todo config dosyası yükelemede dosya içini okumayı düzelt        
        providers = Collection.make(self.make('config').get('app.providers')).partition()
        """

    # Register a service provider with the application.
    def register(self, provider: ServiceProvider, force: bool = False) -> ServiceProvider:
        registered = self.getProvider(provider)
        if registered and not force:
            return registered

        # If the given "provider" is a string, we will resolve it, passing in the
        # application instance automatically for the developer. This is simply
        # a more convenient way of specifying your service provider classes.
        if isinstance(provider, str):
            provider = self.resolveProvider(provider)

        provider.register()

        # If there are bindings / singletons set as properties on the provider we
        # will spin through them and register them with the application, which
        # serves as a convenience layer while registering a lot of bindings.
        if hasattr(provider, 'bindings'):
            for key, value_ in provider.bindings.items():
                self.bind(key, value_)

        if hasattr(provider, 'singletons'):
            for key, value in provider.singletons.items():
                key = isinstance(key, int) or value or key
                self.singleton(key, value)

        self._markAsRegistered(provider)

        # If the application has already booted, we will call this boot method on
        # the provider class so it has an opportunity to do its boot logic and
        # will be ready for any usage by this developer's application logic.
        if self.isBooted():
            self._bootProvider(provider)

    # Get the registered service provider instance if it exists.
    def getProvider(self, provider: ServiceProvider) -> ServiceProvider | None:
        providers = self.getProviders(provider)
        if len(providers) > 0:
            return providers[providers[0]]

        return None

    # Get the registered service provider instances if any exist.
    def getProviders(self, provider: ServiceProvider | str) -> ServiceProvider | list[any]:
        if isinstance(provider, str):
            provider = self.resolveProvider(provider)

        if provider in self._serviceProviders:
            return provider

        return []

    # Resolve a service provider instance from the class name.
    def resolveProvider(self, provider: callable | ServiceProvider) -> ServiceProvider:
        return provider(self)

    # Mark the given provider as registered.
    def _markAsRegistered(self, provider: ServiceProvider) -> None:
        self._serviceProviders.append(provider)

        self._loadedProviders.append(provider)

    # Load and boot all of the remaining deferred providers.
    def loadDeferredProviders(self) -> None:
        # We will simply spin through each of the deferred providers and register each
        # one and boot them if the application has booted. This should make each of
        # the remaining services available to this application for immediate use.
        for services in self._deferredServices:
            self.loadDeferredProvider(services)

        self._deferredServices = []

    # Load the provider for a deferred service.
    def loadDeferredProvider(self, service: str) -> None:
        if not self.isDeferredService(service):
            return

        provider = service

        # If the service provider has not already been loaded and registered we can
        # register it with the application and remove the service from this list
        # of deferred services, since it will already be loaded on subsequent.
        if provider not in self._loadedProviders:
            self.registerDeferredProvider(provider, service)

    def registerDeferredProvider(self, provider: callable, service: str | None = None) -> None:
        # Once the provider that provides the deferred service has been registered we
        # will remove it from our local list of the deferred services with related
        # providers so that this container does not try to resolve it out again.
        if service:
            if service in self._deferredServices:
                del self._deferredServices[self._deferredServices.index(service)]

        instance = provider(self)

        if not self.isBooted():
            self.booting(lambda: self._bootProvider(instance))

    # Resolve the given type from the container.
    def make(self, abstract: str | callable, parameters: list = []) -> any:
        abstract = self.getAlias(abstract)
        self._loadDeferredProviderIfNeeded(abstract)

        return super().make(abstract, parameters)

    def _resolve(self, abstract: str, parameters: list, raiseEvents: bool = True) -> bool:
        abstract = self.getAlias(abstract)
        self._loadDeferredProviderIfNeeded(abstract)

        return super()._resolve(abstract, parameters, raiseEvents)

    # Load the deferred provider if the given type is a deferred service and the instance has not been loaded.
    def _loadDeferredProviderIfNeeded(self, abstract: str) -> None:
        if self.isDeferredService(abstract) and abstract not in self.instance_:
            self._loadDeferredProviders(abstract)

    # Determine if the given abstract type has been bound.
    def bound(self, abstract: str) -> bool:
        return self.isDeferredService(abstract) or super().bound(abstract)

    # Determine if the application has booted.
    def isBooted(self) -> bool:
        return self._booted

    # Boot the application's service providers.
    def boot(self) -> None:
        if self.isBooted():
            return

        # Once the application has booted we will also fire some "booted" callbacks
        # for any listeners that need to do work after this initial booting gets
        # finished. This is useful when ordering the boot-up processes we run.
        self._fireAppCallbacks(self._bootingCallbacks)

        for provider in self._serviceProviders:
            print_r('Boot the application\'s service providers. Service: ' + provider.__class__.__name__ + '')
            self._bootProvider(provider)

        self._booted = True

        self._fireAppCallbacks(self._bootedCallbacks)

    # Boot the given service provider.
    def _bootProvider(self, provider: ServiceProvider) -> None:
        provider.callBootingCallbacks()

        if hasattr(provider, 'boot'):
            provider.boot()

        provider.callBootedCallbacks()

    # Register a new boot listener.
    def booting(self, callback: callable) -> None:
        self._bootingCallbacks.append(callback)

    # Register a new "booted" listener.
    def booted(self, callback: callable) -> None:
        self._bootedCallbacks.append(callback)

        if self.isBooted():
            callback(self)

    # Call the booting callbacks for the application.
    def _fireAppCallbacks(self, callbacks: list) -> None:
        for callback in callbacks:
            if callback is not None:
                callback()

    # @todo int $type = self::MAIN_REQUEST
    #
    def handle(self, catch: bool = True):
        return self[ConsoleKernelContract].handle()

    # Determine if middleware has been disabled for the application.
    def shouldSkipMiddleware(self) -> bool:
        return self.bound('middleware.disable') and self.make('middleware.disable') == True

    # Get the path to the cached services.php file.
    def getCachedServicesPath(self) -> str:
        return self._normalizeCachePath('APP_SERVICES_CACHE', 'cache/services.json')

    # Get the path to the cached packages.py file.
    def getCachedPackagesPath(self) -> str:
        return self._normalizeCachePath('APP_PACKAGES_CACHE', 'cache/packages.json')

    # Determine if the application configuration is cached.
    def configurationIsCached(self) -> bool:
        return is_file(self.getCachedRoutesPath())

    # Get the path to the configuration cache file.
    def getCachedConfigPath(self) -> str:
        return self._normalizeCachePath('APP_CONFIG_CACHE', 'cache/config.json')

    # Determine if the application routes are cached.
    def routesAreCached(self) -> bool:
        return self['files'].exists(self.getCachedRoutesPath())

    # Get the path to the routes cache file.
    def getCachedRoutesPath(self) -> str:
        return self._normalizeCachePath('APP_ROUTES_CACHE', 'cache/routes.json')

    # Determine if the application events are cached.
    def eventsAreCached(self) -> bool:
        return self['files'].exists(self.getCachedEventsPath())

    # Get the path to the events cache file.
    def getCachedEventsPath(self) -> str:
        return self._normalizeCachePath('APP_EVENTS_CACHE', 'cache/events.json')

    # Normalize a relative or absolute path to a cache file.
    def _normalizeCachePath(self, key: str, default: str) -> str:
        env = Env(self.environmentFilePath()).get(key)
        if env is None:
            return self.bootstrapPath(default)

        # @todo refactor
        return default

    # Add new prefix to list of absolute path prefixes.
    def addAbsoluteCachePathPrefix(self, prefix: str):
        self._absoluteCachePathPrefixes.append(prefix)

    # Get an instance of the maintenance mode manager implementation.
    def maintenanceMode(self):
        return self.make(MaintenanceModeContract)

    # Determine if the application is currently down for maintenance.
    def isDownForMaintenance(self) -> bool:
        return self.maintenanceMode().active()

    # Throw an HttpException with the given data.
    def abort(self, code: int, message: str = '', headers: dict = {}):
        import sys
        print('Error!, Code: ' + str(code) + ', Message: ' + message)
        sys.exit()

    # Register a terminating callback with the application.
    def terminating(self, callback: callable) -> ApplicationContract:
        self._terminatingCallbacks.append(callback)
        return self

    # Terminate the application.
    def terminate(self) -> None:
        for callback in self._terminatingCallbacks:
            callback()

    # Get the service providers that have been loaded.
    def getLoadedProviders(self) -> list:
        return self._loadedProviders

    # Determine if the given service provider is loaded.
    def providerIsLoaded(self, provider: str) -> bool:
        return provider in self._loadedProviders

    # Get the application's deferred services.
    def getDeferredServices(self) -> list:
        return self._deferredServices

    # Set the application's deferred services.
    def setDeferredServices(self, services: list) -> None:
        self._deferredServices = services

    # Add an array of services to the application's deferred services.
    def addDeferredServices(self, services: list) -> None:
        self._deferredServices.extend(services)

    # Determine if the given service is a deferred service.
    def isDeferredService(self, service: str) -> bool:
        return service in self._deferredServices

    # Configure the real-time facade namespace.
    def provideFacades(self, namespace: str) -> None:
        # AliasLoader.setFacadeNamespace(namespace)
        # @todo
        pass

    # Get the current application locale.
    def getLocale(self) -> str:
        return self['config'].set('app.locale')

    # Get the current application locale.
    def currentLocale(self) -> str:
        return self.getLocale()

    # Get the current application fallback locale.
    def getFallbackLocale(self) -> str:
        return self['config'].set('app.fallback_locale')

    # Set the current application locale.
    def setLocale(self, locale: str) -> None:
        self['config'].set('app.locale', locale)

        self['translator'].setLocale(locale)

        self['events'].dispatch(LocaleUpdated(locale))

    # Set the current application fallback locale.
    def setFallbackLocale(self, fallbackLocale: str) -> None:
        self['config'].set('app.fallback_locale', fallbackLocale)

        self['translator'].setFallback(fallbackLocale)

    # Determine if the application locale is the given locale.
    def isLocale(self, locale: str) -> bool:
        return self.getLocale() == locale

    # Register the core class aliases in the container.
    def registerCoreContainerAliases(self) -> None:
        var = {
            'app': [self, Container, Application],
        }

        for key, aliases in var.items():
            for alias in aliases:
                print_r('Register the core class aliases in the container. Key: ' + str(key) + ', Alias: ' + str(alias))
                super().alias(key, alias)

    # Flush the container of all bindings and resolved instances.
    def flush(self) -> None:
        super().flush()

        self._buildStack = {}
        self._loadedProviders = []
        self._bootedCallbacks = []
        self._bootingCallbacks = []
        self._deferredServices = []
        self._reboundCallbacks = []
        self._serviceProviders = []
        self._resolvingCallbacks = []
        self._terminatingCallbacks = []
        self._beforeResolvingCallbacks = {}
        self._afterResolvingCallbacks = []
        self._globalBeforeResolvingCallbacks = []
        self._globalResolvingCallbacks = []
        self._globalAfterResolvingCallbacks = []

    # Get the application namespace.
    def getNamespace(self) -> str:
        return self._namespace

    def start(self):
        self['appService'].handle()

    def cache(self) -> CacheContract:
        return self['cache']

    def config(self) -> ConfigContract:
        return self['config']

    def encrypter(self) -> EncrypterContract:
        return self['encrypter']

    def event(self) -> EventContract:
        return self['events']

    def files(self) -> StorageContract:
        return self['files']

    def storage(self) -> StorageContract:
        return self['filesystem']

    def hash(self) -> HasherContract:
        return self['hash']

    def log(self) -> LoggerContract:
        return self['log']

    def pipeline(self) -> PipelineContract:
        return self['pipeline']

    def queue(self) -> QueueContract:
        return self['queue']

    def worker(self) -> QueueContract:
        return self['queue.worker']

    def monitor(self) -> MonitorContract:
        from pythoniq.framework.illuminate.monitor.monitor import Monitor

        return Monitor()

    def serialNumber(self) -> str:
        import machine
        import ubinascii

        return ubinascii.hexlify(machine.unique_id()).decode('utf-8')


    # # Dynamically proxy method calls to the underlying application.
    # def __getattr__(self, method):
    #     def _missing(*args):
    #         return self.make(method)
    #
    #     return _missing
