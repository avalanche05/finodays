class DealNotFoundError(Exception):
    def __init__(self, message="Deal not found"):
        self.message = message
        super().__init__(self.message)