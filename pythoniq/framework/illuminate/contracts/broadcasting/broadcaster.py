from pythoniq.framework.illuminate.broadcasting.broadcastException import BroadcastException


class Broadcaster:
    # Authenticate the incoming request for a given channel.
    def auth(self, request) -> any:
        pass

    # Return the valid authentication response.
    def validAuthenticationResponse(self, request, result: any) -> any:
        pass

    # Broadcast the given event.
    def broadcast(self, channels: list, event: str, payload: dict = {}) -> BroadcastException:
        pass
