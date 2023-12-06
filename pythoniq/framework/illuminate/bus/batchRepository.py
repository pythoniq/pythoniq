from pythoniq.framework.illuminate.bus.batch import Batch
from pythoniq.framework.illuminate.bus.updatedBatchJobCounts import UpdatedBatchJobCounts


class BatchRepository:
    # Retrieve a list of batches.
    def get(self, ids: list[int]) -> list[dict]:
        pass

    # Retrieve information about an existing batch.
    def find(self, batchId: int) -> dict:
        pass

    # Store a new pending batch.
    def store(self, batch) -> Batch:
        pass

    # Increment the total number of jobs within the batch.
    def incrementTotalJobs(self, batchId: int, amount: int = 1) -> None:
        pass

    # Decrement the total number of jobs within the batch.
    def decrementPendingJobs(self, batchId: str, jobId: str) -> UpdatedBatchJobCounts:
        pass

    # Increment the total number of failed jobs for the batch.
    def incrementFailedJobs(self, batchId: int, jobId: int = 1) -> UpdatedBatchJobCounts:
        pass

    # Mark the batch that has the given ID as finished.
    def markAsFinished(self, batchId: int) -> None:
        pass

    # Cancel the batch that has the given ID.
    def cancel(self, batchId: int) -> None:
        pass

    # Delete the batch that has the given ID.
    def delete(self, batchId: int) -> None:
        pass

    # Execute the given Closure within a storage specific transaction.
    def transaction(self, callback: callable):
        pass

