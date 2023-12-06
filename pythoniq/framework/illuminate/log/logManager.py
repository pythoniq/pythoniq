from pythoniq.framework.illuminate.support.manager import Manager
from pythoniq.framework.illuminate.contracts.log.logger import Logger as LoggerContract
from pythoniq.framework.illuminate.log.parsesLogConfiguration import ParsesLogConfiguration
from pythoniq.framework.illuminate.log.logger import Logger
from pythoniq.framework.illuminate.support.helpers import with_, tap


class LogManager(Manager, LoggerContract, ParsesLogConfiguration):
    # The context shared across channels and stacks.
    _sharedContext: dict = {}

    # The standard date format to use when writing logs.
    _dateFormat = 'Y-m-d H:i:s'

    # Get the default driver name.
    def getDefaultDriver(self) -> str:
        return self._config.get('logging.default', 'local')

    # Set the default driver name.
    def setDefaultDriver(self, name: str) -> None:
        return self._config.set('logging.default', name)

    # Get the log connection configuration.
    def _configurationFor(self, name: str) -> dict:
        return self._config.get('logging.channels.' + name, {})

    # Get a log driver instance.
    def driver(self, driver: str | None = None) -> LoggerContract:
        return self._get(self._parseDriver(driver))

    # Get a log channel instance.
    def channel(self, channel: str | None = None):
        return self.driver(channel)

    # Parse the driver name.
    def _parseDriver(self, driver: str | None = None) -> str:
        driver = driver or self.getDefaultDriver()

        if self._app.runningUnitTests():
            return driver or 'null'

        return driver

    # Build an on-demand log channel.
    def build(self, config: dict) -> LoggerContract:
        self._drivers.pop('ondemand', None)

        return self._get('ondemand', config)

    # Create a new, on-demand aggregate logger instance.
    def stack(self, channels: list, channel: str | None = None) -> str | None:
        return (Logger(self.createStackDriver({"channels": channels, "channel": channel}), self._app['events'])) \
            .withContext(self._sharedContext)

    # Attempt to get the log from the local cache.
    def _get(self, name: str, config: dict | None = None) -> LoggerContract:
        try:
            if name in self._drivers:
                return self._drivers[name]

            def fn(logger):
                self._drivers[name] = self._tap(name, Logger(logger, self._app['events'])) \
                    .withContext(self._sharedContext)

                return self._drivers[name]

            return with_(self._resolve(name, config), fn)
        except:
            def fn(logger):
                logger.emergency('Unable to create configured logger. Using emergency logger.')

            return tap(self.createEmergencyLogger(), fn)

    # Apply the configured taps for the logger.
    def _tap(self, name: str, logger: Logger) -> Logger:
        array = self._configurationFor(name).get('tap', [])
        for tap in array:
            [cls, arguments] = self._parseTap(tap)

            self._app.make(cls).__call__(logger, *arguments)

        return logger

    # Parse the given tap class string into a class name and arguments string.
    def _parseTap(self, tap: str) -> list[str]:
        if ':' in tap:
            return tap.split(':', 2)

        return [tap, '']

    # Drivers

    # Create a custom log driver instance.
    def _createCustomDriver(self, config: dict) -> LoggerContract:
        via = config['via']
        factory = callable(via) and via or self._app.make(via)

        return factory(config)

    # Create an emergency log handler to avoid white screens of death.
    def createEmergencyLogger(self) -> LoggerContract:
        from pythoniq.framework.illuminate.log.singleLogger import SingleLogger
        config = self._configurationFor('emergency')

        if 'driver' not in config:
            config['driver'] = 'single'

        if 'path' not in config:
            config['path'] = self._app.storagePath() + '/logs/pythoniq.log'

        return SingleLogger(config)

    # Create an aggregate log driver instance.
    def createStackDriver(self, config: dict) -> LoggerContract:
        from pythoniq.framework.illuminate.log.stackLogger import StackLogger

        if isinstance(config['channels'], str):
            config['channels'] = config['channels'].split(',')

        loggers = []
        for channel in config['channels']:
            loggers.append(self.channel(channel))

        return StackLogger(loggers, config)

    # Create an instance of the single file log driver.
    def createPrintDriver(self, config: dict) -> LoggerContract:
        from pythoniq.framework.illuminate.log.printLogger import PrintLogger

        return PrintLogger(config)

    # Create an instance of the single file log driver.
    def createSingleDriver(self, config: dict) -> LoggerContract:
        from pythoniq.framework.illuminate.log.singleLogger import SingleLogger

        return SingleLogger(config)

    # Create an instance of the daily file log driver.
    def createDailyDriver(self, config: dict) -> LoggerContract:
        from pythoniq.framework.illuminate.log.dailyLogger import DailyLogger

        return DailyLogger(config)

    # Create an instance of the daily file log driver.
    def createPartitionDriver(self, config: dict) -> LoggerContract:
        from pythoniq.framework.illuminate.log.partitionLogger import PartitionLogger

        return PartitionLogger(config)

    # Create an instance of the Slack log driver.
    def createSyslogDriver(self, config: dict) -> LoggerContract:
        raise NotImplementedError

    # Create an instance of the "error log" log driver.
    def createErrorlogDriver(self, config: dict) -> LoggerContract:
        raise NotImplementedError

    # Create an instance of any handler available in Monolog.
    def createMonologDriver(self, config: dict) -> LoggerContract:
        raise NotImplementedError

    # Prepare the handlers for usage by Monolog.
    def _prepareHandlers(self, handlers: dict):
        for key, handler in handlers.items():
            handlers[key] = self._prepareHandler(handler)

        return handlers

    # Prepare the handler for usage by Monolog.
    def _prepareHandler(self, handler: any, config: dict):
        raise NotImplementedError

    # Share context across channels and stacks.
    def shareContext(self, context: dict):
        for channel in context.values():
            channel.withContext(context)

        self._sharedContext.update(context)

        return self

    # The context shared across channels and stacks.
    def sharedContext(self) -> dict:
        return self._sharedContext

    # Flush the shared context.
    def flushSharedContext(self):
        self._sharedContext = {}
        return self

    # Get fallback log channel name.
    def getFallbackChannelName(self) -> str:
        return self._app.bound('env') and self._app.environment() or 'production'

    # Unset the given channel instance.
    def forgetChannel(self, driver: str | None = None) -> None:
        driver = self._parseDriver(driver)

        self._drivers.pop(driver, None)

    # Get all of the resolved log channels.
    def getChannels(self) -> dict:
        return self.getDrivers()

    # Methods

    # System is unusable.
    def emergency(self, message: str, context: dict = {}) -> None:
        self.driver().emergency(message, context)

    # Action must be taken immediately.
    # Example: Entire website down, database unavailable, etc. This should trigger the SMS alerts and wake you up.
    def alert(self, message: str, context: dict = {}) -> None:
        self.driver().alert(message, context)

    # Critical conditions.
    # Example: Entire website down, database unavailable, etc. This should trigger the SMS alerts and wake you up.
    def critical(self, message: str, context: dict = {}) -> None:
        self.driver().critical(message, context)

    #  Runtime errors that do not require immediate action but should typically be logged and monitored.
    def error(self, message: str, context: dict = {}) -> None:
        self.driver().error(message, context)

    # Exceptional occurrences that are not errors.
    # Example: Use of deprecated APIs, poor use of an API, undesirable things that are not necessarily wrong.
    def warning(self, message: str, context: dict = {}) -> None:
        self.driver().warning(message, context)

    # Normal but significant events.
    def notice(self, message: str, context: dict = {}) -> None:
        self.driver().notice(message, context)

    # Interesting events.
    # Example: User logs in, SQL logs.
    def info(self, message: str, context: dict = {}) -> None:
        self.driver().info(message, context)

    # Detailed debug information.
    def debug(self, message: str, context: dict = {}) -> None:
        self.driver().debug(message, context)

    # Logs with an arbitrary level.
    def log(self, level: any, message: str, context: dict = {}) -> None:
        self.driver().log(level, message, context)
