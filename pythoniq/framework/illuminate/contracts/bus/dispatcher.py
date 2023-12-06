class Dispatcher:
    # Dispatch a command to its appropriate handler.
    def dispatch(self, command: any) -> any:
        pass

    # Dispatch a command to its appropriate handler in the current process.
    # Queueable jobs will be dispatched to the "sync" queue.
    def dispatchSync(self, command: any, handler: any = None) -> any:
        pass

    # Dispatch a command to its appropriate handler in the current process.
    def dispatchNow(self, command: any, handler: any = None) -> any:
        pass

    # Determine if the given command has a handler.
    def hasCommandHandler(self, command: any) -> bool:
        pass

    # Retrieve the handler for a command.
    def getCommandHandler(self, command: any) -> bool | any:
        pass

    # Set the pipes commands should be piped through before dispatching.
    def pipeThrough(self, pipes: list):
        pass

    # Map a command to a handler.
    def map(self, map_: dict):
        pass
