class SkipIfBatchCancelled:
    # Process the job.
    def handle(self, job: any, next: callable):
        if hasattr(job, 'batch') and job.batch().cancelled():
            return

        return next(job)
