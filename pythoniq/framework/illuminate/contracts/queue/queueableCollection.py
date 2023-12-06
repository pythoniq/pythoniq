class QueueableCollection:
    # Get the type of the entities being queued.
    def getQueueableClass(self) -> str:
        pass

    # Get the identifiers for all of the entities.
    def getQueueableIds(self) -> list:
        pass

    # Get the relationships of the entities being queued.
    def getQueueableRelations(self) -> list:
        pass

    # Get the connection of the entities being queued.
    def getQueueableConnection(self) -> str:
        pass
