from pythoniq.framework.illuminate.support.interactsWithTime import InteractsWithTime
from pythoniq.framework.illuminate.contracts.cache.repository import Repository
from pythoniq.framework.illuminate.support.helpers import tap


class RateLimiter(InteractsWithTime):
    # The cache store implementation.
    _cache: Repository = None

    # The configured limit object resolvers.
    _limiters: dict = {}

    # Create a new rate limiter instance.
    def __init__(self, cache: Repository):
        self._cache = cache

    # Register a named limiter configuration.
    def for_(self, name: str, callback: callable):
        self._limiters[name] = callback

        return self

    # Get the given named rate limiter.
    def limiter(self, name: str) -> callable:
        return self._limiters[name] or None

    # Attempts to execute a callback if it's not limited.
    def attempt(self, key: str, maxAttempts: int, callback: callable, decaySeconds: int = 0):
        if self._tooManyAttempts(key, maxAttempts):
            return False

        result = callback()
        if result is None:
            result = True

        return tap(result, lambda: self._hit(key, decaySeconds))

    # Determine if the given key has been "accessed" too many times.
    def _tooManyAttempts(self, key: str, maxAttempts: int) -> bool:
        if self.attempts(key) >= maxAttempts:
            if self._cache.has(self.cleanRateLimiterKey(key) + ':timer'):
                return True

            self.resetAttempts(key)

        return False

    # Increment the counter for a given key for a given decay time.
    def _hit(self, key: str, decaySeconds: int = 60):
        key = self.cleanRateLimiterKey(key)

        self._cache.add(key + ':timer', self._availableAt(decaySeconds), decaySeconds)

        added = self._cache.add(key, 0, decaySeconds)

        hits = int(self._cache.increment(key))

        if not added and hits == 1:
            self._cache.put(key, 1, decaySeconds)

        return hits

    # Get the number of attempts for the given key.
    def attempts(self, key: str) -> any:
        key = self.cleanRateLimiterKey(key)

        return self._cache.get(key, 0)

    # Reset the number of attempts for the given key.
    def resetAttempts(self, key: str):
        self._cache.forget(self.cleanRateLimiterKey(key))

        self._cache.forget(key)

    # Get the number of retries left for the given key.
    def remaining(self, key: str, maxAttempts: int) -> int:
        key = self.cleanRateLimiterKey(key)

        attempts = self.attempts(key)

        return maxAttempts - attempts

    # Get the number of retries left for the given key.
    def retriesLeft(self, key: str, maxAttempts: int) -> int:
        return self.remaining(key, maxAttempts)

    # Clear the hits and lockout timer for the given key.
    def clear(self, key: str):
        key = self.cleanRateLimiterKey(key)

        self.resetAttempts(key)

        self._cache.forget(key + ':timer')

    # Get the number of seconds until the "key" is accessible again.
    def availableIn(self, key: str) -> int:
        key = self.cleanRateLimiterKey(key)

        return max(0, int(self._cache.get(key + ':timer')) - self._currentTime())

    # Clean the rate limiter key from unicode characters.
    def cleanRateLimiterKey(self, key: str) -> str:
        return str(key)
