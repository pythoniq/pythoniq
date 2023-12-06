class Looping:
    # The connection name.
    connectionName: str = None

    # The job instance.
    queue: str = None

    # Create a new event instance.
    def __init__(self, connectionName: str, queue: str):
        self.queue = queue
        self.connectionName = connectionName
