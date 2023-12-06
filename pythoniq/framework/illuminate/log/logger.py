from pythoniq.framework.illuminate.contracts.events.dispatcher import Dispatcher
from pythoniq.framework.illuminate.log.events.messageLogged import MessageLogged
from pythoniq.framework.illuminate.support.traits.conditionable import Conditionable
from pythoniq.framework.illuminate.contracts.log.logger import Logger as LoggerContract


class Logger(LoggerContract, Conditionable):
    # The underlying logger implementation.
    _logger: LoggerContract = None

    # The event dispatcher instance.
    _dispatcher: Dispatcher | None = None

    # Any context to be added to logs.
    _context: dict = {}

    def __init__(self, logger: LoggerContract, dispatcher: Dispatcher | None = None):
        self._logger = logger
        self._dispatcher = dispatcher

    # Log an emergency message to the logs.
    def emergency(self, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog('emergency', message, context)

    # Log an alert message to the logs.
    def alert(self, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog('alert', message, context)

    # Log a critical message to the logs.
    def critical(self, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog('critical', message, context)

    # Log an error message to the logs.
    def error(self, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog('error', message, context)

    # Log a warning message to the logs.
    def warning(self, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog('warning', message, context)

    # Log a notice to the logs.
    def notice(self, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog('notice', message, context)

    # Log a notice to the logs.
    def info(self, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog('info', message, context)

    # Log an informational message to the logs.
    def debug(self, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog('debug', message, context)

    # Log a message to the logs.
    def log(self, level: any, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog(level, message, context)

    # Dynamically pass log calls into the writer.
    def write(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog(level, message, context)

    # Write a message to the log.
    def _writeLog(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        _context = self._context.copy()
        _context.update(context)

        message = self._formatMessage(message)
        context = _context
        getattr(self._logger, level)(message, context)

        self._fireLogEvent(level, message, context)

    # Add context to all future logs.
    def withContext(self, context: dict = {}):
        self._context.update(context)

        return self

    # Flush the existing context array.
    def withoutContext(self):
        self._context = {}

        return self

    # Register a new callback handler for when a log event is triggered.
    def listen(self, callback: callable) -> None:
        if self._dispatcher is None:
            raise RuntimeError('Events dispatcher has not been set.')

        self._dispatcher.listen(MessageLogged, callback)

    # Fires a log event.
    def _fireLogEvent(self, level: str, message: str, context: dict):
        # If the event dispatcher is set, we will pass along the parameters to the
        # log listeners. These are useful for building profilers or other tools
        # that aggregate all of the log messages for a given "request" cycle.
        if self._dispatcher is not None:
            self._dispatcher.dispatch(MessageLogged(level, message, context))

    # Format the parameters for the logger.
    def _formatMessage(self, message: list | dict | str) -> str:
        if isinstance(message, list):
            return str(message)
        elif isinstance(message, dict):
            return str(message)

        return str(message)

    #  Get the underlying logger implementation.
    def getLogger(self) -> LoggerContract:
        return self._logger

    # Get the event dispatcher instance.
    def getEventDispatcher(self) -> Dispatcher:
        return self._dispatcher

    # Set the event dispatcher instance.
    def setEventDispatcher(self, dispatcher: Dispatcher):
        self._dispatcher = dispatcher

    # Dynamically proxy method calls to the underlying logger.
    def __getattr__(self, method):
        def _missing(*args):
            return getattr(self.logger, method)(args)

        return _missing
