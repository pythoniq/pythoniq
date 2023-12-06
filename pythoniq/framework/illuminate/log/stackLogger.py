from pythoniq.framework.illuminate.log.abstractLogger import AbstractLogger
from pythoniq.framework.illuminate.contracts.log.logger import Logger as LoggerContract


class StackLogger(AbstractLogger):
    # The logger configuration.
    _config: dict = None

    # The underlying logger implementation.
    _loggers: [LoggerContract] = None

    def __init__(self, loggers: [LoggerContract], config: dict = None):
        super().__init__(config)
        self._loggers = loggers

    def _writeLog(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        for logger in self._loggers:
            getattr(logger, level)(message, context)
