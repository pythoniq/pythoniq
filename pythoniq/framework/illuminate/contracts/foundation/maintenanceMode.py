class MaintenanceMode:
    # Take the application down for maintenance.
    def activate(self, payload: dict) -> None:
        pass

    # Take the application out of maintenance.
    def deactive(self) -> None:
        pass

    # Determine if the application is currently down for maintenance.
    def active(self) -> bool:
        pass

    # Get the data array which was provided when the application was placed into maintenance.
    def data(self) -> dict:
        pass
