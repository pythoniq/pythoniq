import json
import os


class EventCache:
    @staticmethod
    def save(path: str, configs: dict) -> None:
        with open(path, 'w') as outfile:
            json.dump(configs, outfile)

    @staticmethod
    def load(path: str) -> dict:
        with open(path, "r") as file:
            return json.loads(file.read())

    @staticmethod
    def clear(path: str) -> None:
        os.remove(path)
