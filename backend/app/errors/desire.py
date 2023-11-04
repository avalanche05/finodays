class NotEnoughCfa(Exception):
    def __init__(self, message="User have not enough free cfa to create this offer"):
        self.message = message
        super().__init__(self.message)


class DesireNotFoundError(Exception):
    def __init__(self, message="Desire not founded"):
        self.message = message
        super().__init__(self.message)


class SellDesireError(Exception):
    def __init__(self, message="Sell desire error"):
        self.message = message
        super().__init__(self.message)


class CancelDesireError(Exception):
    def __init__(self, message="Cancel desire error"):
        self.message = message
        super().__init__(self.message)


class DesireCountNotEnough(Exception):
    def __init__(self, message="Desire count not enough"):
        self.message = message
        super().__init__(self.message)
