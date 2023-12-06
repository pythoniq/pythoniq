from pythoniq.framework.illuminate.cache.rateLimiting.globalLimit import GlobalLimit


class Unlimited(GlobalLimit):
    # Create a new limit instance.
    def __init__(self):
        super().__init__(1024)
