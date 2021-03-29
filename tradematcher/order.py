class Order:
    def __init__(self, user, price, quantity):
        self.user = user
        self.price = price
        self.quantity = quantity

class Bid(Order):
    pass

class Offer(Order):
    pass

