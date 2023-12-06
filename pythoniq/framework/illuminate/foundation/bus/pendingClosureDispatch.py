class PendingClosureDispatch:
    # Add a callback to be executed if the job fails.
    def catch(self, callback: callable):
        self.job.onFailure(callback)

        return self
