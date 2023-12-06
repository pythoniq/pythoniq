class Pipeline:
    # Set the traveler object being sent on the pipeline.
    def send(self, traveler: any):
        pass

    # Set the traveler object being sent on the pipeline.
    def through(self, stops: any):
        pass

    # Set the method to call on the stops.
    def via(self, method: str):
        pass

    # Run the pipeline with a final destination callback.
    def then(self, destination: callable):
        pass
