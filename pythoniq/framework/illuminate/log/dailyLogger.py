from pythoniq.framework.illuminate.log.abstractFileLogger import AbstractFileLogger
from pythoniq.framework.illuminate.support.facades.app import App
from pythoniq.framework.illuminate.support.str import Str

import time


class DailyLogger(AbstractFileLogger):
    _isOldLogClear: bool = False

    def handle(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        App().make('files').writeStream(self._getLogFilePath(), self._getLogText(level, message), True)

        self._clearOldLogs()

    def _getLogFilePath(self) -> str:
        date = time.localtime()
        path = (
                self._logFileDirName + '/' + self._logFileName + '.'
                + "%04d-%02d-%02d" % (date[0], date[1], date[2]) +
                '.' + self._logFileExtension
        )

        if path != self._logFilePath:
            self._isOldLogClear = True

        self._logFilePath = path
        return self._logFilePath

    def _oldLogFiles(self) -> list:
        logFiles = []
        for logFile in App().make('files').files(self._logFileDirName):
            logFile = Str.of(logFile)

            # Format: laravel.2021-09-01.log
            if logFile.startsWith(self._logFileName + '.') and logFile.endsWith('.' + self._logFileExtension):
                # Format: 2021-09-01
                date = self._findDate(logFile)
                try:
                    isinstance(int(date), int)
                except:
                    if date != '':
                        logFiles.append(logFile.value())

        return logFiles

    def _findDate(self, logFile) -> str:
        return Str.of(logFile).ltrim(self._logFileName + '.').rtrim('.' + self._logFileExtension).value()

    def _clearOldLogs(self) -> None:
        if not self._isOldLogClear:
            return

        oldLogFiles = self._oldLogFiles()[0:self._getConfigDays() * -1]
        for logFile in oldLogFiles:
            App().make('files').delete(self._logFileDirName + '/' + logFile)

        self._isOldLogClear = False

    def _getConfigDays(self) -> int:
        return self._config.get('days', 7)
