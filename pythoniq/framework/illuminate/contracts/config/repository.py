class Repository:
    # Determine if the given configuration value exists.
    def has(self, key: str) -> bool:
        pass

    # Get the specified configuration value.
    def get(self, key: str, default: any = None) -> any:
        pass

    # Get all of the configuration items for the application.
    def all(self) -> dict:
        pass

    # Set a given configuration value.
    def set(self, key: str, value: any = None) -> None:
        pass

    # Forget a given configuration value.
    def forget(self, keys: str) -> None:
        pass

    # Prepend a value onto an array configuration value.
    def prepend(self, key: str, value: any) -> None:
        pass

    # Push a value onto an array configuration value.
    def push(self, key: str, value: any) -> None:
        pass
