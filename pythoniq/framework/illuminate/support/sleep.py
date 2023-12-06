from pythoniq.framework.illuminate.support.traits.macroable import Macroable
import time


class Sleep(Macroable):
    # The fake sleep callbacks.
    _fakeSleepCallbacks: dict = {}

    # The total duration to sleep.
    duration: int = None

    # The pending duration to sleep.
    _pending: int | float | None = None

    # Indicates that all sleeping should be faked.
    _fake: bool = False

    # The sequence of sleep durations encountered while faking.
    _sequence: list = []

    # Indicates if the instance should sleep.
    _shouldSleep: bool = True

    # Create a new sleep instance.
    def __init__(self, duration: int | float | None = None):
        self.duration = duration

    # Sleep for the given duration.
    @classmethod
    def for_(cls, duration: int | float | None = None):
        return cls(duration)

    # Sleep until the given timestamp.
    @classmethod
    def until(cls, timestamp: int | float):
        if isinstance(timestamp, int):
            timestamp = float(timestamp)

        return cls(timestamp - time.time())

    # Sleep for the given number of microseconds.
    @classmethod
    def usleep(cls, microseconds: int):
        return cls(microseconds / 1000000)