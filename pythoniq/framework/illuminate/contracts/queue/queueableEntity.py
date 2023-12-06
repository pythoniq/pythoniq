class QueueableEntity:
    # Get the queueable identity for the entity.
    def getQueueableId(self) -> any:
        pass

    # Get the relationships for the entity.
    def getQueueableRelations(self) -> list:
        pass

    # Get the connection of the entity.
    def getQueueableConnection(self) -> str:
        pass
