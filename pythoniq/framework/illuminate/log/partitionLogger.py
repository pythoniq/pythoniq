from pythoniq.framework.illuminate.log.abstractFileLogger import AbstractFileLogger
from pythoniq.framework.illuminate.support.facades.app import App
from pythoniq.framework.illuminate.support.str import Str


class PartitionLogger(AbstractFileLogger):
    _partNo: int = None
    _lineCount: int = 0
    _logFiles: list = []
    _isOldLogClear: bool = False

    def handle(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        if self._partNo is None:
            self._partNoFind()

        self._lineCount += 1
        App().make('files').writeStream(self._getLogFilePath(), self._getLogText(level, message), True)

        self._clearOldLogs()

    def _getLogFilePath(self) -> str:
        self._partNoIncrement()
        path = self._logFileDirName + '/' + self._logFileName + '.' + str(self._partNo) + '.' + self._logFileExtension

        if path != self._logFilePath:
            self._logFiles.append(path)
            self._isOldLogClear = True

        self._logFilePath = path
        return self._logFilePath

    def _partNoFind(self) -> None:
        self._oldLogFiles()
        if len(self._logFiles) == 0:
            self._partNo = 1
            return

        lastFile = self._logFiles[-1]

        self._partNo = int(self._findPartNo(lastFile))
        self._lineCount = len(App().make('files').lines(self._logFileDirName + '/' + lastFile)) + 1
        self._partNoIncrement()

    def _partNoIncrement(self) -> None:
        if self._lineCount > self._getConfigLines():
            self._partNo += 1
            self._lineCount = 1

    def _oldLogFiles(self) -> None:
        logFiles = []
        for logFile in App().make('files').files(self._logFileDirName):
            logFile = Str.of(logFile)

            # Format: laravel.1.log
            if logFile.startsWith(self._logFileName + '.') and logFile.endsWith('.' + self._logFileExtension):
                # Format: 1
                part = self._findPartNo(logFile)
                try:
                    isinstance(int(part), int)
                    logFiles.append(logFile.value())
                except:
                    pass

        self._logFiles = sorted(logFiles, key=self._findPartNo)

    def _findPartNo(self, logFile) -> int:
        return int(Str.of(logFile).ltrim(self._logFileName + '.').rtrim('.' + self._logFileExtension).value())

    def _clearOldLogs(self) -> None:
        if not self._isOldLogClear:
            return

        for logFile in self._logFiles[0:self._getConfigFiles() * -1]:
            App().make('files').delete(logFile)
            self._logFiles.remove(logFile)

        self._isOldLogClear = False

    def _getConfigLines(self) -> int:
        return self._config.get('lines', 1000)

    def _getConfigFiles(self) -> int:
        return self._config.get('files', 3)

