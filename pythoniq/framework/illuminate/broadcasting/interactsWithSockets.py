class InteractsWithSockets:
    # The socket ID for the user that raised the event.
    socket: str | None = None

    # Exclude the current user from receiving the broadcast.
    def dontBroadcastToCurrentUser(self):
        raise NotImplementedError

        return self

    # Broadcast the event to everyone.
    def broadcastToEveryone(self):
        self.socket = None

        return self

