class Monitor:
    # Register a callback to be executed on every iteration through the queue loop.
    def looping(self, callback: callable) -> None:
        pass

    # Register a callback to be executed when a job fails after the maximum amount of retries.
    def failing(self, callback: any) -> None:
        pass

    # Register a callback to be executed when a daemon queue is stopping.
    def stopping(self, callback: any) -> None:
        pass
