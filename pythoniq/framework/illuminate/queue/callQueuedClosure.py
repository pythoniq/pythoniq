from pythoniq.framework.illuminate.contracts.queue.shouldQueue import ShouldQueue
from pythoniq.framework.illuminate.bus.batchable import Batchable
from pythoniq.framework.illuminate.foundation.bus.dispatchable import Dispatchable
from pythoniq.framework.illuminate.queue.interactsWithQueue import InteractsWithQueue
from pythoniq.framework.illuminate.bus.queueable import Queueable


class CallQueuedClosure(ShouldQueue, Batchable, Dispatchable, InteractsWithQueue, Queueable):
    # The serializable Closure instance.
    _closure: callable = None

    # The callbacks that should be executed on failure.
    def __init__(self):
        # The serializable Closure instance.
        closure: callable = None