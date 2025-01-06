class ValueError(Exception):
    """
    Custom exception for value errors.
    """

    def __init__(self, message="A value error occurred"):
        self.message = message
        super().__init__(self.message)
