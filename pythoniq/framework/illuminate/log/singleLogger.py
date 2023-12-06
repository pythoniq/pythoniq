from pythoniq.framework.illuminate.log.abstractFileLogger import AbstractFileLogger
from pythoniq.framework.illuminate.support.facades.app import App


class SingleLogger(AbstractFileLogger):
    def __init__(self, config: dict = None) -> None:
        if not config.get("path", None):
            raise Exception("Log path not found in configuration")

        super().__init__(config)

    def handle(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        App().make('files').writeStream(self._getLogFilePath(), self._getLogText(level, message), True)

    def _getLogFilePath(self) -> str:
        return self._config['path']
