from user import User


class Order:
    def __init__(self, user, price, quantity):
        # type: (User, int, int)->None
        self.user = user
        self.price = price
        self.quantity = quantity

    @staticmethod
    def from_user(user):
        # type: (User)->Order
        raise Exception("Not overwritten")

    def __str__(self):
        return "Price: %s, QTY: %s"%(self.price, self.quantity) 
    def __repr__(self):
        return str(self)


class Bid(Order):

    @staticmethod
    def user_can_bid(user):
        return user.bid_quantity>0 and user.cash>=user.bid_quantity*user.bid_price

    @staticmethod
    def from_user(user):
        # type: (User)->Bid
        return Bid(user, user.bid_price, user.bid_quantity)


class Offer(Order):
    @staticmethod
    def user_can_offer(user):
        return user.offer_quantity>0 and user.holding>=user.offer_quantity

    @staticmethod
    def from_user(user):
        # type: (User)->Offer
        return Offer(user, user.offer_price, user.offer_quantity)
