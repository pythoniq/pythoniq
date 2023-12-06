from pythoniq.framework.illuminate.cache.rateLimiter import RateLimiter
from pythoniq.framework.illuminate.contracts.container.container import Container


class ThrottlesExceptions:
    # The developer specified key that the rate limiter should use.
    _key: str = None

    # Indicates whether the throttle key should use the job's UUID.
    _byJob: bool = False

    # The maximum number of attempts allowed before rate limiting applies.
    _maxAttempts: int = None

    # The number of minutes until the maximum attempts are reset.
    _decayMinutes: int = None

    # The number of minutes to wait before retrying the job after an exception.
    _retryAfterMinutes: int = 0

    # The callback that determines if rate limiting should apply.
    _whenCallback: callable = None

    # The prefix of the rate limiter key.
    _prefix: str = 'pythoniq:throttle:'

    # The rate limiter instance.
    _limiter: RateLimiter = None

    # Create a new middleware instance.
    def __init__(self, maxAttempts: int = 10, decayMinutes: int = 10):
        self._maxAttempts = maxAttempts
        self._decayMinutes = decayMinutes

    # Process the job.
    def handle(self, job: any, next: callable):
        self._limiter = Container.getInstance().make(RateLimiter)

        jobKey = self._getKey(job)

        if self._limiter.attempt(jobKey, self._maxAttempts):
            return job.release(self._getTimeUntilNextRetry(jobKey))

        try:
            next(job)

            self._limiter.clear(jobKey)
        except Exception as e:
            if self._whenCallback and not self._whenCallback(e):
                raise e

            self._limiter._hit(jobKey, self._decayMinutes * 60)

            return job.release(self._retryAfterMinutes * 60)

    # Specify a callback that should determine if rate limiting behavior should apply.
    def when(self, callback: callable):
        self._whenCallback = callback

        return self

    # Set the prefix of the rate limiter key.
    def withPrefix(self, prefix: str):
        self._prefix = prefix

        return self

    # Specify the number of minutes a job should be delayed when it is released
    # (before it has reached its max exceptions).
    def backoff(self, backoff: int):
        self._retryAfterMinutes = backoff

        return self

    # Get the cache key associated for the rate limiter.
    def _getKey(self, job: any) -> str:
        if self._key:
            return self._prefix + self._key

        if self._byJob:
            return self._prefix + job.job.uuid()

        # @todo: implement this
        # return $this->prefix.md5(get_class($job));
        return self._prefix + job.getJobId() + ':' + job.getUuid()

    # Set the value that the rate limiter should be keyed by.
    def by(self, key: str):
        self._key = key

        return self

    # Indicate that the throttle key should use the job's UUID.
    def byJob(self):
        self._byJob = True

        return self

    # Get the number of seconds that should elapse before the job is retried.
    def _getTimeUntilNextRetry(self, jobKey: str) -> int:
        return self._limiter.availableIn(jobKey) + 3
