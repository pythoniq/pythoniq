class ContextualBindingBuilder:
    # Define the abstract target that depends on the context.
    def needs(self, abstract: str):
        pass

    # Define the implementation for the contextual binding.
    def give(self, implementation: callable | str | list) -> None:
        pass

    # Define tagged services to be used as the implementation for the contextual binding.
    def giveTagged(self, tag: str) -> None:
        pass

    # Specify the configuration item to bind as a primitive.
    def giveConfig(self, key: str, default=None) -> None:
        pass
