from pythoniq.framework.illuminate.support.str import Str


class JobName:
    # Parse the given job name into a class / method array.
    @staticmethod
    def parse(job: str) -> list:
        return Str.parseCallback(job, 'fire')

    # Get the resolved name of the queued job class.
    @staticmethod
    def resolve(name: str, payload: dict) -> str:
        if 'displayName' in payload:
            return payload['displayName']

        return name
