import json


class JobRetryRequested:
    # The job instance.
    job: callable | str | object = None

    # The decoded job payload.
    payload: dict = None

    # Create a new event instance.
    def __init__(self, job: callable | str | object):
        self.job = job

    # The job payload.
    def payload(self) -> dict:
        if self.payload is None:
            self.payload = json.load(self.job.payload)

        return self.payload
