from pythoniq.framework.illuminate.support.helpers import tap
from pythoniq.framework.illuminate.support.higherOrderTapProxy import HigherOrderTapProxy


class Tappable:
    # Call the given Closure with this instance then return the instance.
    def tap(self, callback: callable = None) -> HigherOrderTapProxy:
        return tap(self, callback)
