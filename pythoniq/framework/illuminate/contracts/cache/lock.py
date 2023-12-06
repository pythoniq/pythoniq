class Lock:
    # Attempt to acquire the lock.
    def get(self, callback: callable = None) -> any:
        pass

    # Attempt to acquire the lock for the given number of seconds.
    def block(self, seconds: int, callback: callable = None) -> any:
        pass

    # Release the lock.
    def release(self) -> bool:
        pass

    # Returns the current owner of the lock.
    def owner(self) -> str:
        pass

    # Releases this lock in disregard of ownership.
    def forceRelease(self) -> None:
        pass
