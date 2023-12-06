class FailedJobProviderInterface:
    # Log a failed job into storage.
    def log(self, connection: str, queue: str, payload: dict, exception: Exception) -> str | int | None:
        pass

    # Get a list of all of the failed jobs.
    def all(self) -> list:
        pass

    # Get a single failed job.
    def find(self, id_: any) -> dict | None:
        pass

    # Delete a single failed job from storage.
    def forget(self, id_: any) -> bool:
        pass

    # Flush all of the failed jobs from storage.
    def flush(self) -> None:
        pass
