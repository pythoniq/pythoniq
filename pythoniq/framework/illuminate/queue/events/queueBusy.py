class QueueBusy:
    # The connection name.
    connection: str = None

    # The queue name.
    queue: str = None

    # The size of the queue.
    size: int = None

    # Create a new event instance.
    def __init__(self, connection: str, queue: str, size: int):
        self.connection = connection
        self.queue = queue
        self.size = size
