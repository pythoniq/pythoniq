import time


class InteractsWithTime:
    # Get the number of seconds until the given DateTime.
    def _secondsUntil(self, delay: int) -> int:
        if delay < 1672531200:
            return delay

        return max(0, delay - self._currentTime())

    # Get the "available at" UNIX timestamp.
    def _availableAt(self, delay: int) -> int:
        if delay < 1672531200:
            return self._currentTime() + delay
        
        return delay

    # If the given value is an interval, convert it to a DateTime instance.
    def _parseDateInterval(self, delay: int) -> int:
        if delay < 1672531200:
            return self._currentTime() + delay

        return delay

    # Get the current system time as a UNIX timestamp.
    def _currentTime(self) -> int:
        return int(time.time())
