class ExceptionHandler:
    def report(self, e: Exception):
        pass

    def shouldReport(self, e: Exception) -> bool:
        pass

    def render(self, request, e: Exception):
        pass

    def renderForConsole(self, output, e: Exception) -> None:
        pass
