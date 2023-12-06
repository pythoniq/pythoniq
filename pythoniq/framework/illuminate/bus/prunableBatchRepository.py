from pythoniq.framework.illuminate.bus.batchRepository import BatchRepository


class PrunableBatchRepository(BatchRepository):
    # Prune all of the entries older than the given date.
    def prune(self, date: int):
        pass

