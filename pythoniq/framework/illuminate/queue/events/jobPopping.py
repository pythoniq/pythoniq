class JobPopping:
    # The connection name.
    connectionName: str = None

    # Create a new event instance.
    def __init__(self, connectionName: str):
        self.connectionName = connectionName
