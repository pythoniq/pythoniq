from pythoniq.framework.illuminate.log.abstractLogger import AbstractLogger


class IftttLogger(AbstractLogger):
    def __init__(self, config: dict = None) -> None:
        if not config.get("url", None):
            raise Exception("Log url not found in configuration")

        super().__init__(config)

    def handle(self, level: str, message: list | dict | str, context: dict = {}) -> None:
        pass
