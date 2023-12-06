from pythoniq.framework.illuminate.bus.batch import Batch


class BatchDispatched:
    # The batch instance.
    batch: Batch = None

    # Create a new event instance.
    def __init__(self, batch: Batch):
        self.batch = batch

