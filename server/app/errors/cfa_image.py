class CfaImageNotFoundError(Exception):
    def __init__(self, message="Cfa Image not found"):
        self.message = message
        super().__init__(self.message)