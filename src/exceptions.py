class RelationException(Exception):
    def __init__(self, action: str):
        super().__init__(
            f"Column cannot be {action}d. At least one relation is pointing at selected column!"
        )


class AlreadyExists(Exception):
    pass
