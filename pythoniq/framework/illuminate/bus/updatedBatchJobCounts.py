class UpdatedBatchJobCounts:
    # The number of pending jobs remaining for the batch.
    pendingJobs: int = None

    # The number of failed jobs that belong to the batch.
    failedJobs: int = None

    # Create a new batch job counts object.
    def __init__(self, pendingJobs: int = 0, failedJobs: int = 0):
        self.pendingJobs = pendingJobs
        self.failedJobs = failedJobs

    # Determine if all jobs have run exactly once.
    def allJobsHaveRanExactlyOnce(self):
        return (self.pendingJobs - self.failedJobs) == 0

