from pythoniq.framework.illuminate.cache.rateLimiting.unlimited import Unlimited


class Limit:
    # The rate limit signature key.
    key: any = None

    # The maximum number of attempts allowed within the given number of minutes.
    maxAttempts: int = None

    # The number of minutes until the rate limit is reset.
    decayMinutes: int = None

    # The response generator callback.
    responseCallback: callable = None

    # Create a new limit instance.
    def __init__(self, key: any = '', maxAttempts: int = 60, decayMinutes: int = 1):
        self.key = key
        self.maxAttempts = maxAttempts
        self.decayMinutes = decayMinutes

    # Create a new rate limit.
    @classmethod
    def perMinute(cls, maxAttempts: int):
        return cls('', maxAttempts)

    # Create a new rate limit using minutes as decay time.
    @classmethod
    def perMinutes(cls, maxAttempts: int, decayMinutes: int):
        return cls('', maxAttempts, decayMinutes)

    # Create a new rate limit using hours as decay time.
    @classmethod
    def perHour(cls, maxAttempts: int, decayMinutes: int = 1):
        return cls('', maxAttempts, decayMinutes * 60)

    # Create a new rate limit using days as decay time.
    @classmethod
    def perDay(cls, maxAttempts: int, decayMinutes: int = 1):
        return cls('', maxAttempts, decayMinutes * 1440)

    # Create a new unlimited rate limit.
    @classmethod
    def none(cls):
        return Unlimited()

    # Set the key of the rate limit.
    def by(self, key: any):
        self.key = key

        return self

    # Set the callback that should generate the response when the limit is exceeded.
    def response(self, callback: callable):
        self.responseCallback = callback

        return self
