from pythoniq.framework.illuminate.foundation.helpers import dispatch


class DispatchesJobs:
    # Dispatch a job to its appropriate handler.
    def dispatch(self, job: any):
        return dispatch(job)

    # Dispatch a job to its appropriate handler in the current process.
    # Queueable jobs will be dispatched to the "sync" queue.
