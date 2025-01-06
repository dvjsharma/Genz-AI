class InvalidInputError(Exception):
    """
    Custom exception for invalid input.
    """

    def __init__(self, message="Invalid input provided"):
        self.message = message
        super().__init__(self.message)
