class NotEnoughCfa(Exception):
    def __init__(self, message="User have not enough free cfa to create this offer"):
        self.message = message
        super().__init__(self.message)


class OfferNotFoundError(Exception):
    def __init__(self, message="Offer not founded"):
        self.message = message
        super().__init__(self.message)


class BuyOfferError(Exception):
    def __init__(self, message="Buy offer error"):
        self.message = message
        super().__init__(self.message)


class OfferCountNotEnough(Exception):
    def __init__(self, message="Offer count not enough"):
        self.message = message
        super().__init__(self.message)


class CancelOfferError(Exception):
    def __init__(self, message="Cancel offer error"):
        self.message = message
        super().__init__(self.message)
