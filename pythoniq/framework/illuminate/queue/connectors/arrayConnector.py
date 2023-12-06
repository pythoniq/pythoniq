from pythoniq.framework.illuminate.queue.connectors.connectorInterface import ConnectorInterface
from pythoniq.framework.illuminate.queue.queue import Queue
from pythoniq.framework.illuminate.queue.arrayQueue import ArrayQueue


class ArrayConnector(ConnectorInterface):
    # Establish a queue connection.
    def connect(self, config) -> Queue:
        return ArrayQueue()
