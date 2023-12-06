from pythoniq.framework.illuminate.contracts.bus.dispatcher import Dispatcher
from pythoniq.framework.illuminate.foundation.bus.pendingClosureDispatch import PendingClosureDispatch
from pythoniq.framework.illuminate.foundation.bus.pendingDispatch import PendingDispatch
from pythoniq.framework.illuminate.queue.callQueuedClosure import CallQueuedClosure
from pythoniq.framework.illuminate.support.facades.app import App


# Dispatch a job to its appropriate handler.
def dispatch(job: any) -> PendingDispatch:
    return callable(job) and PendingClosureDispatch(CallQueuedClosure.create(job)) or PendingDispatch(job)


# Dispatch a command to its appropriate handler in the current process.
# Queueable jobs will be dispatched to the "sync" queue.
def dispatch_sync(job: any, handler: any) -> any:
    return App().make(Dispatcher).dispatchSync(job, handler)
