from pythoniq.framework.illuminate.cache.rateLimiting.limit import Limit


class GlobalLimit(Limit):
    # Create a new limit instance.
    def __init__(self, maxAttempts: int, decayMinutes: int = 1):
        super().__init__('', maxAttempts, decayMinutes)
