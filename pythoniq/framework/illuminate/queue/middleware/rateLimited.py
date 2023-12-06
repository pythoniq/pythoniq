from pythoniq.framework.illuminate.cache.rateLimiter import RateLimiter
from pythoniq.framework.illuminate.container.container import Container


class RateLimited:
    # The rate limiter instance.
    _limiter: RateLimiter = None

    # The name of the rate limiter.
    _limiterName: str = None

    # Indicates if the job should be released if the limit is exceeded.
    shouldRelease: bool = True

    # Create a new middleware instance.
    def __init__(self, limiterName: str):
        self._limiter = Container.getInstance().make(RateLimiter)
