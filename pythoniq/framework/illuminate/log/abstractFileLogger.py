from pythoniq.framework.illuminate.log.abstractLogger import AbstractLogger
from pythoniq.framework.illuminate.support.str import Str


class AbstractFileLogger(AbstractLogger):
    _logFilePath: str = None
    _logFileDirName: str = None
    _logFileName: str = None
    _logFileExtension: str = None

    def __init__(self, config: dict = None) -> None:
        if not config.get("path", None):
            raise Exception("Log path not found in configuration")

        super().__init__(config)

        self._parsePath()

    def _parsePath(self) -> None:
        path = Str.of(self._config['path'])
        self._logFileDirName = path.dirname().value()
        self._logFileName = path.name().value()
        self._logFileExtension = path.extension().value()
