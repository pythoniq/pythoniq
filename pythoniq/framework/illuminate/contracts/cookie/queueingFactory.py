from pythoniq.framework.illuminate.contracts.cookie.factory import Factory as CookieFactory


class QueueingFactory(CookieFactory):
    # Queue a cookie to send with the next response.
    def queue(self, *args: tuple) -> None:
        pass

    # Remove a cookie from the queue.
    def unqueue(self, *args: tuple) -> None:
        pass

    # Get the cookies which have been queued for the next request.
    def getQueuedCookies(self) -> dict:
        pass
