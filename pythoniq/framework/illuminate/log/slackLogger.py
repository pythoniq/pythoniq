from pythoniq.framework.illuminate.log.abstractLogger import AbstractLogger

import urequests


class SlackLogger(AbstractLogger):
    def __init__(self, config: dict = None) -> None:
        if not config.get("url", None):
            raise Exception("Log url not found in configuration")

        super().__init__(config)

    def handle(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        if self._config.get('url', None):
            self._sendMessage(level.upper() + ': ' + message)

    def _sendMessage(self, message):
        data = '{"text":"%(message)s"}' % {'message': message}
        try:
            urequests.post(self._config.get('url'), data=data, headers={'content-type': 'application/json'})
        finally:
            return
