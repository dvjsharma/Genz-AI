class RuntimeError(Exception):
    """
    Custom exception for runtime errors.
    """

    def __init__(self, message="A runtime error occurred"):
        self.message = message
        super().__init__(self.message)
