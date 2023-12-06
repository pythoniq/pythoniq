from app.libraries.gsm.commands.response import Response


class ResponseParserContract:
    _response: Response = None

    @staticmethod
    def parse(value) -> list:
        pass

    @staticmethod
    def commandParse(value) -> dict:
        pass

    def response(self) -> Response:
        return self._response

