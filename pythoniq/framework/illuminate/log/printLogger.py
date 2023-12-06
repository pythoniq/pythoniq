from pythoniq.framework.illuminate.log.abstractLogger import AbstractLogger


class PrintLogger(AbstractLogger):
    _colors = {
        'debug': '\033[1m',
        'info': '\033[94m',
        'notice': '\x1b[1;33m',
        'warning': '\x1b[2;33m',
        'error': '\033[33m',
        'critical': '\033[3;33m',
        'alert': '\033[91m',
        'emergency': '\033[1;91m',
    }

    def handle(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        print(self.getColor(level) + message + '\033[0m')

    def getColor(self, level) -> str:
        return self._colors.get(level, '\033[0m')
