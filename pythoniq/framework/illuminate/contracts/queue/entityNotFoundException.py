class EntityNotFoundException(Exception):
    # Create a new exception instance.
    def __init__(self, type_: str, id_: any = None):
        id_ = str(id_)

        Exception(f"Queueable entity [{type_}] not found for ID [{id_}].")
