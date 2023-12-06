from pythoniq.framework.illuminate.contracts.console.kernel import Kernel as KernelContract
from pythoniq.framework.illuminate.contracts.debug.exceptionHandler import ExceptionHandler
from pythoniq.framework.illuminate.contracts.events.dispatcher import Dispatcher
from pythoniq.framework.illuminate.contracts.foundation.application import Application
from pythoniq.framework.illuminate.foundation.bootstrap.loadEnvironmentVariables import LoadEnvironmentVariables
from pythoniq.framework.illuminate.foundation.bootstrap.loadConfiguration import LoadConfiguration
from pythoniq.framework.illuminate.foundation.bootstrap.registerFacades import RegisterFacades
from pythoniq.framework.illuminate.foundation.bootstrap.registerProviders import RegisterProviders
from pythoniq.framework.illuminate.foundation.bootstrap.bootProviders import BootProviders
from pythoniq.framework.illuminate.console.application import Application as Artisan
from pythoniq.framework.illuminate.foundation.console.closureCommand import ClosureCommand
from pythoniq.framework.illuminate.support.env import Env

import time


class Kernel(KernelContract):
    # The application implementation.
    _app: Application = None

    # The event dispatcher implementation.
    _events: Dispatcher = None

    # The Symfony event dispatcher implementation.
    _symfonyDispatcher = None

    # The Artisan application instance.
    _artisan = None

    # The Artisan commands provided by the application.
    _commands: list = []

    # Indicates if the Closure commands have been loaded.
    _commandsLoaded: bool = False

    # All of the registered command duration handlers.
    _commandLifecycleDurationHandlers: list = []

    # When the currently handled command started.
    _commandStartedAt: float = None

    # The bootstrap classes for the application.
    _bootstrappers: list = [
        LoadEnvironmentVariables,
        LoadConfiguration,

        RegisterFacades,
        RegisterProviders,
        BootProviders,
    ]

    def __init__(self, app: Application, events: Dispatcher):
        self._app = app
        self._events = events

        self._app.booted()

    # Define the application's command schedule.
    def _defineConsoleSchedule(self) -> None:
        # @todo
        return self._app.singleton('schedule', lambda app: None)

    # Get the name of the cache store that should manage scheduling mutexes.
    def _scheduleCache(self) -> str:
        return self._app['config'].get('cache.schedule_store', Env().get('SCHEDULE_CACHE_DRIVER'))

    # Run the console application.
    def handle(self, _input=None, output=None) -> int:
        self.commandStartedAt = time.time()

        try:
            #if _input.getFirstArgument() in ['env:encrypt', 'env:decrypt']:
            if _input in ['env:encrypt', 'env:decrypt']:
                self.bootstrapWithoutBootingProviders()

            self.bootstrap()
        except Exception as e:
            self._reportException(e)

            self._renderException(output, e)

            return 1

    # Terminate the application.
    def terminate(self, input, status: int) -> None:
        self._app.terminate()

        self._commandStartedAt = None

    # Register a callback to be invoked when the command lifecycle duration exceeds a given amount of time.
    def whenCommandLifecycleIsLongerThan(self, threshold: int, handler: callable) -> None:
        self._commandLifecycleDurationHandlers.append((threshold, handler))

    # When the command being handled started.
    def commandStartedAt(self) -> float:
        return self._commandStartedAt

    # Define the application's command schedule.
    def _schedule(self) -> None:
        pass

    # Get the timezone that should be used by default for scheduled events.
    def _scheduleTimezone(self) -> str:
        config = self._app['config']

        return config.get('app.schedule_timezone', config.get('app.timezone'))

    # Register the commands for the application.
    def _commands(self) -> None:
        pass

    # Register a Closure based command with the application.
    def command(self, signature: str, callback: callable) -> None:
        command = ClosureCommand(signature, callback)


    def output(self) -> str:
        self.bootstrap()
        return self.getArtisan().output()

    # Register the given command with the console application.
    def registerCommand(self, command):
        self.getArtisan().add(command)

    # Run an Artisan console command by name.
    def call(self, command: str, parameters: list = None, outputBuffer=None) -> int:
        if command in ['env:encrypt', 'env:decrypt']:
            self.bootstrapWithoutBootingProviders()

        self.bootstrap()

        return self.getArtisan().call(command, parameters, outputBuffer)

    # Queue the given console command.
    def queue(self, command: str, parameters: list = None) -> None:
        return QueueCommand.dispatch([command] + parameters)

    # Get all of the commands registered with the console.
    def all(self) -> list:
        self.bootstrap()
        return self.getArtisan().all()

    # Bootstrap the application for artisan commands.
    def bootstrap(self) -> None:
        if not self._app.hasBeenBootstrapped():
            self._app.bootstrapWith(self._getBootstrappers())

        self._app.loadDeferredProviders()

        if not self._commandsLoaded:
            #self.commands()

            self._commandsLoaded = True

    # Bootstrap the application without booting service providers.
    def bootstrapWithoutBootingProviders(self) -> None:
        bootstrapper = []

        for bootstrap in self._getBootstrappers():
            if bootstrap == BootProviders:
                continue

            bootstrapper.append(bootstrap)

        self._app.bootstrapWith(bootstrapper)

    # Set the Artisan application instance.
    def setArtisan(self, artisan) -> None:
        self._artisan = artisan

        return self

    # Get the bootstrap classes for the application.
    def _getBootstrappers(self) -> list:
        return self._bootstrappers

    # Report the exception to the exception handler.
    def _reportException(self, e):
        self._app[ExceptionHandler].report(e)

    # Render the given exception.
    def _renderException(self, output, e):
        self._app[ExceptionHandler].renderForConsole(output, e)
