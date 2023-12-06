from pythoniq.framework.illuminate.contracts.log.logger import Logger as LoggerContract
from pythoniq.framework.illuminate.log.levels import Levels
import time


class AbstractLogger(LoggerContract, Levels):
    # The logger configuration.
    _config: dict = None

    def __init__(self, config: dict = None):
        self._config = config or {}

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

    # Interesting events.
    # Example: User logs in, SQL logs.
    def info(self, message: str, context: dict) -> None:
        self._writeLog('info', message, context)

    # Log an informational message to the logs.
    def debug(self, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog('debug', message, context)

    def log(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog(level, message, context)

    def write(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        self._writeLog(level, message, context)

    def _writeLog(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        if self._isHandle(level):
            self.handle(level, message, context)

    def handle(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        raise NotImplementedError

    def getLevel(self, level) -> int:
        severity = self._levels.get(level, None)

        if severity is None:
            raise ValueError(f'Invalid log level: {level}')

        return severity

    def _isHandle(self, level) -> bool:
        return self.getLevel(level) >= self.getLevel(self._config.get('level', 'debug'))

    def _getLogText(self, level, message) -> str:
        return '[' + self._getDateTimeText() + '] ' + level.upper() + ': ' + message + "\n"

    def _getDateTimeText(self) -> str:
        date = time.localtime()
        return "%04d-%02d-%02d %02d:%02d:%02d" % (date[0], date[1], date[2], date[3], date[4], date[5])
